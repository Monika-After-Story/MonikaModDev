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

# *** This file has been minified using python-minifier

_E='unix'
_D='tcp'
_C='darwin'
_B=None
_A=b''
import re,os,platform,socket,fcntl
if hasattr(fcntl,'F_SETFD'):
	F_SETFD=fcntl.F_SETFD
	if hasattr(fcntl,'FD_CLOEXEC'):FD_CLOEXEC=fcntl.FD_CLOEXEC
	else:FD_CLOEXEC=1
else:from FCNTL import F_SETFD,FD_CLOEXEC
from Xlib import error,xauth
SUPPORTED_PROTOCOLS=_B,_D,_E
uname=platform.uname()
if uname[0]=='Darwin'and[int(A)for A in uname[2].split('.')]>=[9,0]:SUPPORTED_PROTOCOLS+=_C,;DARWIN_DISPLAY_RE=re.compile('^/private/tmp/[-:a-zA-Z0-9._]*:(?P<dno>[0-9]+)(\\.(?P<screen>[0-9]+))?$')
DISPLAY_RE=re.compile('^((?P<proto>tcp|unix)/)?(?P<host>[-:a-zA-Z0-9._]*):(?P<dno>[0-9]+)(\\.(?P<screen>[0-9]+))?$')
def get_display(display):
	A=display
	if A is _B:A=os.environ.get('DISPLAY','')
	D=[(DISPLAY_RE,{})]
	if _C in SUPPORTED_PROTOCOLS:D.insert(0,(DARWIN_DISPLAY_RE,{'protocol':_C}))
	for (H,I) in D:
		E=H.match(A)
		if E is not _B:F,G,C,B=[E.groupdict().get(A,I.get(A))for A in('proto','host','dno','screen')];break
	else:raise error.DisplayNameError(A)
	if F==_D and not G:raise error.DisplayNameError(A)
	C=int(C)
	if B:B=int(B)
	else:B=0
	return A,F,G,C,B
def _get_tcp_socket(host,dno):A=socket.socket(socket.AF_INET,socket.SOCK_STREAM);A.connect((host,6000+dno));return A
def _get_unix_socket(address):A=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM);A.connect(address);return A
def get_socket(dname,protocol,host,dno):
	F=dname;E=dno;B=host;A=protocol;assert A in SUPPORTED_PROTOCOLS
	try:
		if A==_C:C=_get_unix_socket(F)
		elif(A is _B or A!=_E)and B and B!=_E:C=_get_tcp_socket(B,E)
		else:
			D='/tmp/.X11-unix/X%d'%E
			if not os.path.exists(D):D='\x00'+D
			try:C=_get_unix_socket(D)
			except socket.error:
				if not A and not B:C=_get_tcp_socket(B,E)
				else:raise
	except socket.error as G:raise error.DisplayConnectionError(F,str(G))
	fcntl.fcntl(C.fileno(),F_SETFD,FD_CLOEXEC);return C
def new_get_auth(sock,dname,protocol,host,dno):
	C=protocol;assert C in SUPPORTED_PROTOCOLS
	if C==_C:A=xauth.FamilyLocal;B=socket.gethostname()
	elif C==_D:A=xauth.FamilyInternet;D=sock.getpeername()[0].split('.');B=bytearray((int(A)for A in D))
	else:A=xauth.FamilyLocal;B=socket.gethostname().encode()
	try:E=xauth.Xauthority()
	except error.XauthError:return _A,_A
	while 1:
		try:return E.get_best_auth(A,B,dno)
		except error.XNoAuthError:pass
		if A==xauth.FamilyInternet and B==b'\x7f\x00\x00\x01':A=xauth.FamilyLocal;B=socket.gethostname().encode()
		else:return _A,_A
def old_get_auth(sock,dname,host,dno):
	C=D=_A
	try:
		H=os.popen('xauth list %s 2>/dev/null'%dname).read();E=H.split('\n')
		if len(E)>=1:
			A=E[0].split(_B,2)
			if len(A)==3:
				C=A[1];F=A[2];B=_A
				for G in range(0,len(F),2):B=B+chr(int(F[G:G+2],16))
				D=B
	except os.error:pass
	return C,D
get_auth=new_get_auth
