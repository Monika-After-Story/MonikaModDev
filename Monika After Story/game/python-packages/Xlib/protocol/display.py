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

# *** This file has been minified using python-minifier

_O='pixmap_formats'
_N='roots'
_M='vendor'
_L='auth_prot_data'
_K='auth_prot_name'
_J='protocol_minor'
_I='protocol_major'
_H='allowed_depths'
_G='visuals'
_F='depth'
_E='reason_length'
_D='status'
_C='additional_length'
_B='unsupported type: {}'
_A=None
import errno,math,select,socket,struct,sys
from six import PY3,byte2int,indexbytes
from ..  import error
from ..support import lock,connect
from .  import rq
from .  import event
if PY3:
	class bytesview:
		def __init__(E,data,offset=0,size=_A):
			C=size;B=offset;A=data
			if C is _A:C=len(A)-B
			if isinstance(A,bytes):D=memoryview(A)
			elif isinstance(A,bytesview):D=A.view
			else:raise TypeError(_B.format(type(A)))
			E.view=D[B:B+C]
		def __len__(A):return len(A.view)
		def __getitem__(B,key):
			A=key
			if isinstance(A,slice):return bytes(B.view[A])
			return B.view[A]
else:
	def bytesview(data,offset=0,size=_A):
		C=offset;B=size;A=data
		if not isinstance(A,(bytes,buffer)):raise TypeError(_B.format(type(A)))
		if B is _A:B=len(A)-C
		return buffer(A,C,B)
class Display:
	extension_major_opcodes={};error_classes=error.xerror_class.copy();event_classes=event.event_class.copy()
	def __init__(A,display=_A):
		L=b'';B,E,F,G,I=connect.get_display(display);A.display_name=B;A.default_screen=I;A.socket=connect.get_socket(B,E,F,G);J,K=connect.get_auth(A.socket,B,E,F,G);A.socket_error_lock=lock.allocate_lock();A.socket_error=_A;A.event_queue_read_lock=lock.allocate_lock();A.event_queue_write_lock=lock.allocate_lock();A.event_queue=[];A.request_queue_lock=lock.allocate_lock();A.request_serial=1;A.request_queue=[];A.send_recv_lock=lock.allocate_lock();A.send_active=0;A.recv_active=0;A.event_waiting=0;A.event_wait_lock=lock.allocate_lock();A.request_waiting=0;A.request_wait_lock=lock.allocate_lock();C=A.socket.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF);C=math.pow(2,math.floor(math.log(C,2)));A.recv_buffer_size=int(C);A.sent_requests=[];A.recv_packet_len=0;A.data_send=L;A.data_recv=L;A.data_sent_bytes=0;A.resource_id_lock=lock.allocate_lock();A.resource_ids={};A.last_resource_id=0;A.error_handler=_A;A.big_endian=struct.unpack('BB',struct.pack('H',256))[0]
		if A.big_endian:H=66
		else:H=108
		D=ConnectionSetupRequest(A,byte_order=H,protocol_major=11,protocol_minor=0,auth_prot_name=J,auth_prot_data=K)
		if D.status!=1:raise error.DisplayConnectionError(A.display_name,D.reason)
		A.info=D;A.default_screen=min(A.default_screen,len(A.info.roots)-1)
	def get_default_screen(A):return A.default_screen
	def flush(A):A.check_for_error();A.send_recv_lock.acquire();A.send_and_recv(flush=1)
	def close(A):A.flush();A.close_internal('client')
	def allocate_resource_id(A):
		A.resource_id_lock.acquire()
		try:
			B=A.last_resource_id
			while B in A.resource_ids:
				B=B+1
				if B>A.info.resource_id_mask:B=0
				if B==A.last_resource_id:raise error.ResourceIDError('out of resource ids')
			A.resource_ids[B]=_A;A.last_resource_id=B;return A.info.resource_id_base|B
		finally:A.resource_id_lock.release()
	def free_resource_id(A,rid):
		A.resource_id_lock.acquire()
		try:
			B=rid&A.info.resource_id_mask
			if rid-B!=A.info.resource_id_base:return _A
			try:del A.resource_ids[B]
			except KeyError:pass
		finally:A.resource_id_lock.release()
	def get_resource_class(A,class_name,default=_A):return A.resource_classes.get(class_name,default)
	def check_for_error(A):
		A.socket_error_lock.acquire();B=A.socket_error;A.socket_error_lock.release()
		if B:raise B
	def send_request(A,request,wait_for_response):
		B=request
		if A.socket_error:raise A.socket_error
		A.request_queue_lock.acquire();B._serial=A.request_serial;A.request_serial=(A.request_serial+1)%65536;A.request_queue.append((B,wait_for_response));C=len(A.request_queue);A.request_queue_lock.release()
	def close_internal(A,whom):A.request_queue=_A;A.sent_requests=_A;A.event_queue=_A;A.data_send=_A;A.data_recv=_A;A.socket.close();A.socket_error_lock.acquire();A.socket_error=error.ConnectionClosedError(whom);A.socket_error_lock.release()
	def send_and_recv(A,flush=_A,event=_A,request=_A,recv=_A):
		V='server: %s';I=event;G=recv;F=request;D=flush
		if(D or F is not _A)and A.send_active or(I or G)and A.recv_active:
			if I:
				E=A.event_wait_lock
				if not A.event_waiting:A.event_waiting=1;E.acquire()
			elif F is not _A:
				E=A.request_wait_lock
				if not A.request_waiting:A.request_waiting=1;E.acquire()
			A.send_recv_lock.release()
			if D or G:return
			E.acquire();E.release();return
		if not A.recv_active:H=1;A.recv_active=1
		else:H=0
		J=_A;C=0
		while 1:
			if C or not A.send_active:
				A.request_queue_lock.acquire()
				for (L,S) in A.request_queue:
					A.data_send=A.data_send+L._binary
					if S:A.sent_requests.append(L)
				del A.request_queue[:];A.request_queue_lock.release()
				if A.data_send:A.send_active=1;C=1
				else:A.send_active=0;C=0
			A.send_recv_lock.release()
			if not(C or H):break
			if D and J is _A:J=A.data_sent_bytes+len(A.data_send)
			try:
				if C:M=[A.socket]
				else:M=[]
				if G or D:N=0
				else:N=_A
				T,U,W=select.select([A.socket],M,[],N)
			except select.error as B:
				if isinstance(B,OSError):O=B.errno
				else:O=B[0]
				if O!=errno.EINTR:raise
				A.send_recv_lock.acquire();continue
			if U:
				try:P=A.socket.send(A.data_send)
				except socket.error as B:A.close_internal(V%B);raise A.socket_error
				A.data_send=A.data_send[P:];A.data_sent_bytes=A.data_sent_bytes+P
			Q=0
			if T:
				if H:
					try:K=A.recv_packet_len-len(A.data_recv);K=max(A.recv_buffer_size,K);R=A.socket.recv(K)
					except socket.error as B:A.close_internal(V%B);raise A.socket_error
					if not R:A.close_internal('server');raise A.socket_error
					A.data_recv=bytes(A.data_recv)+R;Q=A.parse_response(F)
				else:A.send_recv_lock.acquire();A.send_active=0;A.send_recv_lock.release();return
			if D and J>=A.data_sent_bytes:break
			if I and A.event_queue:break
			if F is not _A and Q:break
			if G:break
			A.send_recv_lock.acquire()
		A.send_recv_lock.acquire()
		if C:A.send_active=0
		if H:A.recv_active=0
		if A.event_waiting:A.event_waiting=0;A.event_wait_lock.release()
		if A.request_waiting:A.request_waiting=0;A.request_wait_lock.release()
		A.send_recv_lock.release()
	def parse_response(A,request):
		D=request
		if D==-1:return A.parse_connection_setup()
		C=0
		while 1:
			if A.data_recv:B=byte2int(A.data_recv)
			if A.recv_packet_len:
				if len(A.data_recv)<A.recv_packet_len:return C
				if B==1:C=A.parse_request_response(D)or C;continue
				elif B&127==35:A.parse_event_response(B);continue
				else:raise AssertionError(B)
			if len(A.data_recv)<32:return C
			if B==0:C=A.parse_error_response(D)or C
			elif B==1 or B&127==35:E=int(struct.unpack('=L',A.data_recv[4:8])[0]);A.recv_packet_len=32+E*4
			else:A.parse_event_response(B)
	def parse_error_response(A,request):
		D=indexbytes(A.data_recv,1);E=A.error_classes.get(D,error.XError);B=E(A,A.data_recv[:32]);A.data_recv=bytesview(A.data_recv,32);C=A.get_waiting_request(B.sequence_number)
		if C and C._set_error(B):
			if isinstance(C,rq.ReplyRequest):
				A.send_recv_lock.acquire()
				if A.request_waiting:A.request_waiting=0;A.request_wait_lock.release()
				A.send_recv_lock.release()
			return request==B.sequence_number
		else:
			if A.error_handler:rq.call_error_handler(A.error_handler,B,_A)
			else:A.default_error_handler(B)
			return 0
	def default_error_handler(A,err):sys.stderr.write('X protocol error:\n%s\n'%err)
	def parse_request_response(A,request):
		B=A.get_waiting_replyrequest();C=struct.unpack('=H',A.data_recv[2:4])[0]
		if C!=B._serial:raise RuntimeError("Expected reply for request %s, but got %s.  Can't happen!"%(B._serial,C))
		B._parse_response(A.data_recv[:A.recv_packet_len]);A.data_recv=bytesview(A.data_recv,A.recv_packet_len);A.recv_packet_len=0;A.send_recv_lock.acquire()
		if A.request_waiting:A.request_waiting=0;A.request_wait_lock.release()
		A.send_recv_lock.release();return B.sequence_number==request
	def parse_event_response(A,etype):
		B=etype;B=B&127
		if B==35:E=A.recv_packet_len
		else:E=32
		C=A.event_classes.get(B,event.AnyEvent)
		if type(C)==dict:
			D=A.data_recv[1]
			if type(D)==str:D=ord(D)
			C=C[D]
		F=C(display=A,binarydata=A.data_recv[:E])
		if B==35:A.recv_packet_len=0
		A.data_recv=bytesview(A.data_recv,E)
		if hasattr(F,'sequence_number'):A.get_waiting_request((F.sequence_number-1)%65536)
		A.event_queue_write_lock.acquire();A.event_queue.append(F);A.event_queue_write_lock.release();A.send_recv_lock.acquire()
		if A.event_waiting:A.event_waiting=0;A.event_wait_lock.release()
		A.send_recv_lock.release()
	def get_waiting_request(A,sno):
		B=sno
		if not A.sent_requests:return _A
		if A.sent_requests[0]._serial>A.request_serial:
			I=A.request_serial+65536
			if B<A.request_serial:B=B+65536
		else:
			I=A.request_serial
			if B>A.request_serial:B=B-65536
		if B<A.sent_requests[0]._serial:return _A
		E=_A;F=len(A.sent_requests);G=0;H=0
		for D in range(0,len(A.sent_requests)):
			C=A.sent_requests[D]._serial+G
			if C<H:G=65536;C=C+G
			H=C
			if B==C:E=A.sent_requests[D];F=D+1;break
			elif B<C:E=_A;F=D;break
		del A.sent_requests[:F];return E
	def get_waiting_replyrequest(A):
		for B in range(0,len(A.sent_requests)):
			if hasattr(A.sent_requests[B],'_reply'):C=A.sent_requests[B];del A.sent_requests[:B+1];return C
		else:raise RuntimeError("Request reply to unknown request.  Can't happen!")
	def parse_connection_setup(A):
		B=A.sent_requests[0]
		while 1:
			if B._data:
				C=B._data[_C]*4
				if len(A.data_recv)<C:return 0
				if B._data[_D]!=1:B._data['reason']=A.data_recv[:B._data[_E]]
				else:D,E=B._success_reply.parse_binary(A.data_recv[:C],A,rawdict=1);B._data.update(D)
				del A.sent_requests[0];A.data_recv=A.data_recv[C:];return 1
			else:
				if len(A.data_recv)<8:return 0
				B._data,E=B._reply.parse_binary(A.data_recv[:8],A,rawdict=1);A.data_recv=A.data_recv[8:]
PixmapFormat=rq.Struct(rq.Card8(_F),rq.Card8('bits_per_pixel'),rq.Card8('scanline_pad'),rq.Pad(5))
VisualType=rq.Struct(rq.Card32('visual_id'),rq.Card8('visual_class'),rq.Card8('bits_per_rgb_value'),rq.Card16('colormap_entries'),rq.Card32('red_mask'),rq.Card32('green_mask'),rq.Card32('blue_mask'),rq.Pad(4))
Depth=rq.Struct(rq.Card8(_F),rq.Pad(1),rq.LengthOf(_G,2),rq.Pad(4),rq.List(_G,VisualType))
Screen=rq.Struct(rq.Window('root'),rq.Colormap('default_colormap'),rq.Card32('white_pixel'),rq.Card32('black_pixel'),rq.Card32('current_input_mask'),rq.Card16('width_in_pixels'),rq.Card16('height_in_pixels'),rq.Card16('width_in_mms'),rq.Card16('height_in_mms'),rq.Card16('min_installed_maps'),rq.Card16('max_installed_maps'),rq.Card32('root_visual'),rq.Card8('backing_store'),rq.Card8('save_unders'),rq.Card8('root_depth'),rq.LengthOf(_H,1),rq.List(_H,Depth))
class ConnectionSetupRequest(rq.GetAttrData):
	_request=rq.Struct(rq.Set('byte_order',1,(66,108)),rq.Pad(1),rq.Card16(_I),rq.Card16(_J),rq.LengthOf(_K,2),rq.LengthOf(_L,2),rq.Pad(2),rq.String8(_K),rq.String8(_L));_reply=rq.Struct(rq.Card8(_D),rq.Card8(_E),rq.Card16(_I),rq.Card16(_J),rq.Card16(_C));_success_reply=rq.Struct(rq.Card32('release_number'),rq.Card32('resource_id_base'),rq.Card32('resource_id_mask'),rq.Card32('motion_buffer_size'),rq.LengthOf(_M,2),rq.Card16('max_request_length'),rq.LengthOf(_N,1),rq.LengthOf(_O,1),rq.Card8('image_byte_order'),rq.Card8('bitmap_format_bit_order'),rq.Card8('bitmap_format_scanline_unit'),rq.Card8('bitmap_format_scanline_pad'),rq.Card8('min_keycode'),rq.Card8('max_keycode'),rq.Pad(4),rq.String8(_M),rq.List(_O,PixmapFormat),rq.List(_N,Screen))
	def __init__(A,display,*C,**D):B=display;A._binary=A._request.to_binary(*C,**D);A._data=_A;B.request_queue.append((A,1));B.send_recv_lock.acquire();B.send_and_recv(request=-1)
