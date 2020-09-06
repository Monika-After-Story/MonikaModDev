import re,socket
from Xlib import error
display_re=re.compile('^([-a-zA-Z0-9._]*):([0-9]+)(\\.([0-9]+))?$')
def get_display(display):
	G='localhost';B=display
	if B is None:return':0.0',None,G,0,0
	C=display_re.match(B)
	if not C:raise error.DisplayNameError(B)
	E=B;D=C.group(1)
	if not D:D=G
	F=int(C.group(2));A=C.group(4)
	if A:A=int(A)
	else:A=0
	return E,None,D,F,A
def get_socket(dname,protocol,host,dno):
	try:A=socket.socket(socket.AF_INET,socket.SOCK_STREAM);A.connect((host,6000+dno))
	except socket.error as B:raise error.DisplayConnectionError(dname,str(B))
	return A
def get_auth(sock,dname,host,dno):return'',''