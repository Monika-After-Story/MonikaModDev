_C='tcp'
_B='unix'
_A='darwin'
import re,os,platform,socket,fcntl
if hasattr(fcntl,'F_SETFD'):
	F_SETFD=fcntl.F_SETFD
	if hasattr(fcntl,'FD_CLOEXEC'):FD_CLOEXEC=fcntl.FD_CLOEXEC
	else:FD_CLOEXEC=1
else:from FCNTL import F_SETFD,FD_CLOEXEC
from Xlib import error,xauth
SUPPORTED_PROTOCOLS=None,_C,_B
uname=platform.uname()
if uname[0]=='Darwin'and[int(x)for x in uname[2].split('.')]>=[9,0]:SUPPORTED_PROTOCOLS+=_A,;DARWIN_DISPLAY_RE=re.compile('^/private/tmp/[-:a-zA-Z0-9._]*:(?P<dno>[0-9]+)(\\.(?P<screen>[0-9]+))?$')
DISPLAY_RE=re.compile('^((?P<proto>tcp|unix)/)?(?P<host>[-:a-zA-Z0-9._]*):(?P<dno>[0-9]+)(\\.(?P<screen>[0-9]+))?$')
def get_display(display):
	A=display
	if A is None:A=os.environ.get('DISPLAY','')
	D=[(DISPLAY_RE,{})]
	if _A in SUPPORTED_PROTOCOLS:D.insert(0,(DARWIN_DISPLAY_RE,{'protocol':_A}))
	for (I,J) in D:
		E=I.match(A)
		if E is not None:F,G,C,B=[E.groupdict().get(H,J.get(H))for H in('proto','host','dno','screen')];break
	else:raise error.DisplayNameError(A)
	if F==_C and not G:raise error.DisplayNameError(A)
	C=int(C)
	if B:B=int(B)
	else:B=0
	return A,F,G,C,B
def _get_tcp_socket(host,dno):A=socket.socket(socket.AF_INET,socket.SOCK_STREAM);A.connect((host,6000+dno));return A
def _get_unix_socket(address):A=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM);A.connect(address);return A
def get_socket(dname,protocol,host,dno):
	F=dname;E=dno;B=host;A=protocol;assert A in SUPPORTED_PROTOCOLS
	try:
		if A==_A:C=_get_unix_socket(F)
		elif(A is None or A!=_B)and B and B!=_B:C=_get_tcp_socket(B,E)
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
	if C==_A:A=xauth.FamilyLocal;B=socket.gethostname()
	elif C==_C:A=xauth.FamilyInternet;D=sock.getpeername()[0].split('.');B=bytearray((int(A)for A in D))
	else:A=xauth.FamilyLocal;B=socket.gethostname().encode()
	try:E=xauth.Xauthority()
	except error.XauthError:return'',''
	while 1:
		try:return E.get_best_auth(A,B,dno)
		except error.XNoAuthError:pass
		if A==xauth.FamilyInternet and B=='\x7f\x00\x00\x01':A=xauth.FamilyLocal;B=socket.gethostname().encode()
		else:return'',''
def old_get_auth(sock,dname,host,dno):
	C=D=''
	try:
		H=os.popen('xauth list %s 2>/dev/null'%dname).read();E=H.split('\n')
		if len(E)>=1:
			A=E[0].split(None,2)
			if len(A)==3:
				C=A[1];F=A[2];B=''
				for G in range(0,len(F),2):B=B+chr(int(F[G:G+2],16))
				D=B
	except os.error:pass
	return C,D
get_auth=new_get_auth