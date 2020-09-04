# -*- coding: utf-8 -*-
#
# Xlib.protocol.display -- core display communication
#
#    Copyright (C) 2000-2002 Peter Liljenberg <petli@ctrl-c.liu.se>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 2.1
# of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
#    Free Software Foundation, Inc.,
#    59 Temple Place,
#    Suite 330,
#    Boston, MA 02111-1307 USA

# Standard modules
import errno
import math
import select
import socket
import struct
import sys

# Python 2/3 compatibility.
from six import PY3, byte2int, indexbytes

# Xlib modules
from .. import error

from ..support import lock, connect

# Xlib.protocol modules
from . import rq
from . import event

if PY3:
    class bytesview(object):
        def __init__(self, data, offset=0, size=None):
            if size is None:
                size = len(data)-offset
            if isinstance(data, bytes):
                view = memoryview(data)
            elif isinstance(data, bytesview):
                view = data.view
            else:
                raise TypeError('unsupported type: {}'.format(type(data)))
            self.view = view[offset:offset+size]

        def __len__(self):
            return len(self.view)

        def __getitem__(self, key):
            if isinstance(key, slice):
                return bytes(self.view[key])
            return self.view[key]

else:
    def bytesview(data, offset=0, size=None):
        if not isinstance(data, (bytes, buffer)):
            raise TypeError('unsupported type: {}'.format(type(data)))
        if size is None:
            size = len(data)-offset
        return buffer(data, offset, size)


class Display(object):
    extension_major_opcodes = {}
    error_classes = error.xerror_class.copy()
    event_classes = event.event_class.copy()

    def __init__(self, display = None):
        name, protocol, host, displayno, screenno = connect.get_display(display)
        self.display_name = name
        self.default_screen = screenno
        self.socket = connect.get_socket(name, protocol, host, displayno)
        auth_name, auth_data = connect.get_auth(self.socket, name,
                                                protocol, host, displayno)
        self.socket_error_lock = lock.allocate_lock()
        self.socket_error = None
        self.event_queue_read_lock = lock.allocate_lock()
        self.event_queue_write_lock = lock.allocate_lock()
        self.event_queue = []
        self.request_queue_lock = lock.allocate_lock()
        self.request_serial = 1
        self.request_queue = []
        self.send_recv_lock = lock.allocate_lock()
        self.send_active = 0
        self.recv_active = 0
        self.event_waiting = 0
        self.event_wait_lock = lock.allocate_lock()
        self.request_waiting = 0
        self.request_wait_lock = lock.allocate_lock()
        buffer_size = self.socket.getsockopt(socket.SOL_SOCKET,
                                             socket.SO_RCVBUF)
        buffer_size = math.pow(2, math.floor(math.log(buffer_size, 2)))
        self.recv_buffer_size = int(buffer_size)
        self.sent_requests = []
        self.recv_packet_len = 0
        self.data_send = b''
        self.data_recv = b''
        self.data_sent_bytes = 0
        self.resource_id_lock = lock.allocate_lock()
        self.resource_ids = {}
        self.last_resource_id = 0
        self.error_handler = None
        self.big_endian = struct.unpack('BB', struct.pack('H', 0x0100))[0]

        if self.big_endian:
            order = 0x42
        else:
            order = 0x6c

        r = ConnectionSetupRequest(self,
                                   byte_order = order,
                                   protocol_major = 11,
                                   protocol_minor = 0,
                                   auth_prot_name = auth_name,
                                   auth_prot_data = auth_data)

        if r.status != 1:
            raise error.DisplayConnectionError(self.display_name, r.reason)

        self.info = r
        self.default_screen = min(self.default_screen, len(self.info.roots) - 1)

    def get_default_screen(self):
        return self.default_screen

    def flush(self):
        self.check_for_error()
        self.send_recv_lock.acquire()
        self.send_and_recv(flush = 1)

    def close(self):
        self.flush()
        self.close_internal('client')

    def allocate_resource_id(self):
        self.resource_id_lock.acquire()
        try:
            i = self.last_resource_id
            while i in self.resource_ids:
                i = i + 1
                if i > self.info.resource_id_mask:
                    i = 0
                if i == self.last_resource_id:
                    raise error.ResourceIDError('out of resource ids')

            self.resource_ids[i] = None
            self.last_resource_id = i
            return self.info.resource_id_base | i
        finally:
            self.resource_id_lock.release()

    def free_resource_id(self, rid):
        self.resource_id_lock.acquire()
        try:
            i = rid & self.info.resource_id_mask

            if rid - i != self.info.resource_id_base:
                return None

            try:
                del self.resource_ids[i]
            except KeyError:
                pass
        finally:
            self.resource_id_lock.release()

    def get_resource_class(self, class_name, default = None):
        return self.resource_classes.get(class_name, default)

    def check_for_error(self):
        self.socket_error_lock.acquire()
        err = self.socket_error
        self.socket_error_lock.release()

        if err:
            raise err

    def send_request(self, request, wait_for_response):
        if self.socket_error:
            raise self.socket_error

        self.request_queue_lock.acquire()

        request._serial = self.request_serial
        self.request_serial = (self.request_serial + 1) % 65536

        self.request_queue.append((request, wait_for_response))
        qlen = len(self.request_queue)

        self.request_queue_lock.release()

    def close_internal(self, whom):
        self.request_queue = None
        self.sent_requests = None
        self.event_queue = None
        self.data_send = None
        self.data_recv = None
        self.socket.close()
        self.socket_error_lock.acquire()
        self.socket_error = error.ConnectionClosedError(whom)
        self.socket_error_lock.release()


    def send_and_recv(self, flush = None, event = None, request = None, recv = None):
        if (((flush or request is not None) and self.send_active)
            or ((event or recv) and self.recv_active)):
            if event:
                wait_lock = self.event_wait_lock
                if not self.event_waiting:
                    self.event_waiting = 1
                    wait_lock.acquire()

            elif request is not None:
                wait_lock = self.request_wait_lock
                if not self.request_waiting:
                    self.request_waiting = 1
                    wait_lock.acquire()

            self.send_recv_lock.release()

            if flush or recv:
                return

            wait_lock.acquire()
            wait_lock.release()

            return

        if not self.recv_active:
            receiving = 1
            self.recv_active = 1
        else:
            receiving = 0

        flush_bytes = None
        sending = 0

        while 1:
            if sending or not self.send_active:
                self.request_queue_lock.acquire()
                for req, wait in self.request_queue:
                    self.data_send = self.data_send + req._binary
                    if wait:
                        self.sent_requests.append(req)

                del self.request_queue[:]
                self.request_queue_lock.release()
                if self.data_send:
                    self.send_active = 1
                    sending = 1
                else:
                    self.send_active = 0
                    sending = 0

            self.send_recv_lock.release()

            if not (sending or receiving):
                break

            if flush and flush_bytes is None:
                flush_bytes = self.data_sent_bytes + len(self.data_send)


            try:
                if sending:
                    writeset = [self.socket]
                else:
                    writeset = []

                if recv or flush:
                    timeout = 0
                else:
                    timeout = None

                rs, ws, es = select.select([self.socket], writeset, [], timeout)

            except select.error as err:
                if isinstance(err, OSError):
                    code = err.errno
                else:
                    code = err[0]
                if code != errno.EINTR:
                    raise

                self.send_recv_lock.acquire()
                continue


            if ws:
                try:
                    i = self.socket.send(self.data_send)
                except socket.error as err:
                    self.close_internal('server: %s' % err)
                    raise self.socket_error

                self.data_send = self.data_send[i:]
                self.data_sent_bytes = self.data_sent_bytes + i


            gotreq = 0
            if rs:
                if receiving:
                    try:
                        count = self.recv_packet_len - len(self.data_recv)
                        count = max(self.recv_buffer_size, count)
                        bytes_recv = self.socket.recv(count)
                    except socket.error as err:
                        self.close_internal('server: %s' % err)
                        raise self.socket_error

                    if not bytes_recv:
                        self.close_internal('server')
                        raise self.socket_error

                    self.data_recv = bytes(self.data_recv) + bytes_recv
                    gotreq = self.parse_response(request)

                else:
                    self.send_recv_lock.acquire()
                    self.send_active = 0
                    self.send_recv_lock.release()

                    return

            if flush and flush_bytes >= self.data_sent_bytes:
                break

            if event and self.event_queue:
                break

            if request is not None and gotreq:
                break

            if recv:
                break

            self.send_recv_lock.acquire()

        self.send_recv_lock.acquire()

        if sending:
            self.send_active = 0
        if receiving:
            self.recv_active = 0

        if self.event_waiting:
            self.event_waiting = 0
            self.event_wait_lock.release()

        if self.request_waiting:
            self.request_waiting = 0
            self.request_wait_lock.release()

        self.send_recv_lock.release()


    def parse_response(self, request):
        if request == -1:
            return self.parse_connection_setup()

        gotreq = 0
        while 1:
            if self.data_recv:
                rtype = byte2int(self.data_recv)

            if self.recv_packet_len:
                if len(self.data_recv) < self.recv_packet_len:
                    return gotreq

                if rtype == 1:
                    gotreq = self.parse_request_response(request) or gotreq
                    continue
                elif rtype & 0x7f == 35:
                    self.parse_event_response(rtype)
                    continue
                else:
                    raise AssertionError(rtype)

            if len(self.data_recv) < 32:
                return gotreq

            if rtype == 0:
                gotreq = self.parse_error_response(request) or gotreq

            elif rtype == 1 or rtype & 0x7f == 35:
                rlen = int(struct.unpack('=L', self.data_recv[4:8])[0])
                self.recv_packet_len = 32 + rlen * 4

            else:
                self.parse_event_response(rtype)


    def parse_error_response(self, request):
        code = indexbytes(self.data_recv, 1)

        estruct = self.error_classes.get(code, error.XError)

        e = estruct(self, self.data_recv[:32])
        self.data_recv = bytesview(self.data_recv, 32)

        req = self.get_waiting_request(e.sequence_number)

        if req and req._set_error(e):
            if isinstance(req, rq.ReplyRequest):
                self.send_recv_lock.acquire()

                if self.request_waiting:
                    self.request_waiting = 0
                    self.request_wait_lock.release()

                self.send_recv_lock.release()

            return request == e.sequence_number

        else:
            if self.error_handler:
                rq.call_error_handler(self.error_handler, e, None)
            else:
                self.default_error_handler(e)

            return 0


    def default_error_handler(self, err):
        sys.stderr.write('X protocol error:\n%s\n' % err)


    def parse_request_response(self, request):
        req = self.get_waiting_replyrequest()

        sno = struct.unpack('=H', self.data_recv[2:4])[0]
        if sno != req._serial:
            raise RuntimeError("Expected reply for request %s, but got %s.  Can't happen!"
                               % (req._serial, sno))

        req._parse_response(self.data_recv[:self.recv_packet_len])

        self.data_recv = bytesview(self.data_recv, self.recv_packet_len)
        self.recv_packet_len = 0

        self.send_recv_lock.acquire()

        if self.request_waiting:
            self.request_waiting = 0
            self.request_wait_lock.release()

        self.send_recv_lock.release()


        return req.sequence_number == request


    def parse_event_response(self, etype):
        etype = etype & 0x7f

        if etype == 35:
            length = self.recv_packet_len
        else:
            length = 32

        estruct = self.event_classes.get(etype, event.AnyEvent)
        if type(estruct) == dict:
            subcode = self.data_recv[1]

            if type(subcode) == str:
                subcode = ord(subcode)

            estruct = estruct[subcode]

        e = estruct(display = self, binarydata = self.data_recv[:length])

        if etype == 35:
            self.recv_packet_len = 0

        self.data_recv = bytesview(self.data_recv, length)

        if hasattr(e, 'sequence_number'):
            self.get_waiting_request((e.sequence_number - 1) % 65536)

        self.event_queue_write_lock.acquire()
        self.event_queue.append(e)
        self.event_queue_write_lock.release()

        self.send_recv_lock.acquire()

        if self.event_waiting:
            self.event_waiting = 0
            self.event_wait_lock.release()

        self.send_recv_lock.release()


    def get_waiting_request(self, sno):
        if not self.sent_requests:
            return None

        if self.sent_requests[0]._serial > self.request_serial:
            last_serial = self.request_serial + 65536
            if sno < self.request_serial:
                sno = sno + 65536

        else:
            last_serial = self.request_serial
            if sno > self.request_serial:
                sno = sno - 65536

        if sno < self.sent_requests[0]._serial:
            return None

        req = None
        reqpos = len(self.sent_requests)
        adj = 0
        last = 0

        for i in range(0, len(self.sent_requests)):
            rno = self.sent_requests[i]._serial + adj

            if rno < last:
                adj = 65536
                rno = rno + adj

            last = rno

            if sno == rno:
                req = self.sent_requests[i]
                reqpos = i + 1
                break
            elif sno < rno:
                req = None
                reqpos = i
                break

        del self.sent_requests[:reqpos]

        return req

    def get_waiting_replyrequest(self):
        for i in range(0, len(self.sent_requests)):
            if hasattr(self.sent_requests[i], '_reply'):
                req = self.sent_requests[i]
                del self.sent_requests[:i + 1]
                return req

        else:
            raise RuntimeError("Request reply to unknown request.  Can't happen!")

    def parse_connection_setup(self):
        r = self.sent_requests[0]

        while 1:
            if r._data:
                alen = r._data['additional_length'] * 4

                if len(self.data_recv) < alen:
                    return 0

                if r._data['status'] != 1:
                    r._data['reason'] = self.data_recv[:r._data['reason_length']]

                else:
                    x, d = r._success_reply.parse_binary(self.data_recv[:alen],
                                                         self, rawdict = 1)
                    r._data.update(x)

                del self.sent_requests[0]

                self.data_recv = self.data_recv[alen:]

                return 1

            else:
                if len(self.data_recv) < 8:
                    return 0

                r._data, d = r._reply.parse_binary(self.data_recv[:8],
                                                   self, rawdict = 1)
                self.data_recv = self.data_recv[8:]


PixmapFormat = rq.Struct( rq.Card8('depth'),
                          rq.Card8('bits_per_pixel'),
                          rq.Card8('scanline_pad'),
                          rq.Pad(5)
                          )

VisualType = rq.Struct ( rq.Card32('visual_id'),
                         rq.Card8('visual_class'),
                         rq.Card8('bits_per_rgb_value'),
                         rq.Card16('colormap_entries'),
                         rq.Card32('red_mask'),
                         rq.Card32('green_mask'),
                         rq.Card32('blue_mask'),
                         rq.Pad(4)
                         )

Depth = rq.Struct( rq.Card8('depth'),
                   rq.Pad(1),
                   rq.LengthOf('visuals', 2),
                   rq.Pad(4),
                   rq.List('visuals', VisualType)
                   )

Screen = rq.Struct( rq.Window('root'),
                    rq.Colormap('default_colormap'),
                    rq.Card32('white_pixel'),
                    rq.Card32('black_pixel'),
                    rq.Card32('current_input_mask'),
                    rq.Card16('width_in_pixels'),
                    rq.Card16('height_in_pixels'),
                    rq.Card16('width_in_mms'),
                    rq.Card16('height_in_mms'),
                    rq.Card16('min_installed_maps'),
                    rq.Card16('max_installed_maps'),
                    rq.Card32('root_visual'),
                    rq.Card8('backing_store'),
                    rq.Card8('save_unders'),
                    rq.Card8('root_depth'),
                    rq.LengthOf('allowed_depths', 1),
                    rq.List('allowed_depths', Depth)
                    )


class ConnectionSetupRequest(rq.GetAttrData):
    _request = rq.Struct( rq.Set('byte_order', 1, (0x42, 0x6c)),
                          rq.Pad(1),
                          rq.Card16('protocol_major'),
                          rq.Card16('protocol_minor'),
                          rq.LengthOf('auth_prot_name', 2),
                          rq.LengthOf('auth_prot_data', 2),
                          rq.Pad(2),
                          rq.String8('auth_prot_name'),
                          rq.String8('auth_prot_data') )

    _reply = rq.Struct ( rq.Card8('status'),
                         rq.Card8('reason_length'),
                         rq.Card16('protocol_major'),
                         rq.Card16('protocol_minor'),
                         rq.Card16('additional_length') )

    _success_reply = rq.Struct( rq.Card32('release_number'),
                                rq.Card32('resource_id_base'),
                                rq.Card32('resource_id_mask'),
                                rq.Card32('motion_buffer_size'),
                                rq.LengthOf('vendor', 2),
                                rq.Card16('max_request_length'),
                                rq.LengthOf('roots', 1),
                                rq.LengthOf('pixmap_formats', 1),
                                rq.Card8('image_byte_order'),
                                rq.Card8('bitmap_format_bit_order'),
                                rq.Card8('bitmap_format_scanline_unit'),
                                rq.Card8('bitmap_format_scanline_pad'),
                                rq.Card8('min_keycode'),
                                rq.Card8('max_keycode'),
                                rq.Pad(4),
                                rq.String8('vendor'),
                                rq.List('pixmap_formats', PixmapFormat),
                                rq.List('roots', Screen),
                                )


    def __init__(self, display, *args, **keys):
        self._binary = self._request.to_binary(*args, **keys)
        self._data = None

        display.request_queue.append((self, 1))

        display.send_recv_lock.acquire()
        display.send_and_recv(request = -1)
