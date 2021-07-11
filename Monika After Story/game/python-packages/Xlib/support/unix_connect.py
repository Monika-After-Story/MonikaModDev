# Xlib.support.unix_connect -- Unix-type display connection functions
#
#    Copyright (C) 2000,2002 Peter Liljenberg <petli@ctrl-c.liu.se>
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

import re
import os
import platform
import socket

# FCNTL is deprecated from Python 2.2, so only import it if we doesn't
# get the names we need.  Furthermore, FD_CLOEXEC seems to be missing
# in Python 2.2.

import fcntl

if hasattr(fcntl, 'F_SETFD'):
    F_SETFD = fcntl.F_SETFD
    if hasattr(fcntl, 'FD_CLOEXEC'):
        FD_CLOEXEC = fcntl.FD_CLOEXEC
    else:
        FD_CLOEXEC = 1
else:
    from FCNTL import F_SETFD, FD_CLOEXEC


from Xlib import error, xauth


SUPPORTED_PROTOCOLS = (None, 'tcp', 'unix')

# Darwin funky socket.
uname = platform.uname()
if (uname[0] == 'Darwin') and ([int(x) for x in uname[2].split('.')] >= [9, 0]):
    SUPPORTED_PROTOCOLS += ('darwin',)
    DARWIN_DISPLAY_RE = re.compile(r'^/private/tmp/[-:a-zA-Z0-9._]*:(?P<dno>[0-9]+)(\.(?P<screen>[0-9]+))?$')

DISPLAY_RE = re.compile(r'^((?P<proto>tcp|unix)/)?(?P<host>[-:a-zA-Z0-9._]*):(?P<dno>[0-9]+)(\.(?P<screen>[0-9]+))?$')


def get_display(display):
    # Use $DISPLAY if display isn't provided
    if display is None:
        display = os.environ.get('DISPLAY', '')

    re_list = [(DISPLAY_RE, {})]

    if 'darwin' in SUPPORTED_PROTOCOLS:
        re_list.insert(0, (DARWIN_DISPLAY_RE, {'protocol': 'darwin'}))

    for re, defaults in re_list:
        m = re.match(display)
        if m is not None:
            protocol, host, dno, screen = [
                m.groupdict().get(field, defaults.get(field))
                for field in ('proto', 'host', 'dno', 'screen')
            ]
            break
    else:
        raise error.DisplayNameError(display)

    if protocol == 'tcp' and not host:
        # Host is mandatory when protocol is TCP.
        raise error.DisplayNameError(display)

    dno = int(dno)
    if screen:
        screen = int(screen)
    else:
        screen = 0

    return display, protocol, host, dno, screen


def _get_tcp_socket(host, dno):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 6000 + dno))
    return s

def _get_unix_socket(address):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(address)
    return s

def get_socket(dname, protocol, host, dno):
    assert protocol in SUPPORTED_PROTOCOLS
    try:
        # Darwin funky socket.
        if protocol == 'darwin':
            s = _get_unix_socket(dname)

        # TCP socket, note the special case: `unix:0.0` is equivalent to `:0.0`.
        elif (protocol is None or protocol != 'unix') and host and host != 'unix':
            s = _get_tcp_socket(host, dno)

        # Unix socket.
        else:
            address = '/tmp/.X11-unix/X%d' % dno
            if not os.path.exists(address):
                # Use abstract address.
                address = '\0' + address
            try:
                s = _get_unix_socket(address)
            except socket.error:
                if not protocol and not host:
                    # If no protocol/host was specified, fallback to TCP.
                    s = _get_tcp_socket(host, dno)
                else:
                    raise
    except socket.error as val:
        raise error.DisplayConnectionError(dname, str(val))

    # Make sure that the connection isn't inherited in child processes.
    fcntl.fcntl(s.fileno(), F_SETFD, FD_CLOEXEC)

    return s


def new_get_auth(sock, dname, protocol, host, dno):
    assert protocol in SUPPORTED_PROTOCOLS
    # Translate socket address into the xauth domain
    if protocol == 'darwin':
        family = xauth.FamilyLocal
        addr = socket.gethostname()

    elif protocol == 'tcp':
        family = xauth.FamilyInternet

        # Convert the prettyprinted IP number into 4-octet string.
        # Sometimes these modules are too damn smart...
        octets = sock.getpeername()[0].split('.')
        addr = bytearray(int(x) for x in octets)
    else:
        family = xauth.FamilyLocal
        addr = socket.gethostname().encode()

    try:
        au = xauth.Xauthority()
    except error.XauthError:
        return b'', b''

    while 1:
        try:
            return au.get_best_auth(family, addr, dno)
        except error.XNoAuthError:
            pass

        # We need to do this to handle ssh's X forwarding.  It sets
        # $DISPLAY to localhost:10, but stores the xauth cookie as if
        # DISPLAY was :10.  Hence, if localhost and not found, try
        # again as a Unix socket.
        if family == xauth.FamilyInternet and addr == b'\x7f\x00\x00\x01':
            family = xauth.FamilyLocal
            addr = socket.gethostname().encode()
        else:
            return b'', b''


def old_get_auth(sock, dname, host, dno):
    # Find authorization cookie
    auth_name = auth_data = b''

    try:
        # We could parse .Xauthority, but xauth is simpler
        # although more inefficient
        data = os.popen('xauth list %s 2>/dev/null' % dname).read()

        # If there's a cookie, it is of the format
        #      DISPLAY SCHEME COOKIE
        # We're interested in the two last parts for the
        # connection establishment
        lines = data.split('\n')
        if len(lines) >= 1:
            parts = lines[0].split(None, 2)
            if len(parts) == 3:
                auth_name = parts[1]
                hexauth = parts[2]
                auth = b''

                # Translate hexcode into binary
                for i in range(0, len(hexauth), 2):
                    auth = auth + chr(int(hexauth[i:i+2], 16))

                auth_data = auth
    except os.error:
        pass

    return auth_name, auth_data

get_auth = new_get_auth
