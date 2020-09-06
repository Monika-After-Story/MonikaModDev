import os,struct
from Xlib import X,error
FamilyInternet=X.FamilyInternet
FamilyDECnet=X.FamilyDECnet
FamilyChaos=X.FamilyChaos
FamilyLocal=256
class Xauthority(object):
	def __init__(F,filename=None):
		E='>H';D=filename
		if D is None:D=os.environ.get('XAUTHORITY')
		if D is None:
			try:D=os.path.join(os.environ['HOME'],'.Xauthority')
			except KeyError:raise error.XauthError('$HOME not set, cannot find ~/.Xauthority')
		try:
			with open(D,'rb')as H:C=H.read()
		except IOError as I:raise error.XauthError('could not read from {0}: {1}'.format(D,I))
		F.entries=[];A=0
		try:
			while A<len(C):
				J,=struct.unpack(E,C[A:A+2]);A=A+2;B,=struct.unpack(E,C[A:A+2]);A=A+B+2;K=C[A-B:A];B,=struct.unpack(E,C[A:A+2]);A=A+B+2;L=C[A-B:A];B,=struct.unpack(E,C[A:A+2]);A=A+B+2;M=C[A-B:A];B,=struct.unpack(E,C[A:A+2]);A=A+B+2;G=C[A-B:A]
				if len(G)!=B:break
				F.entries.append((J,K,L,M,G))
		except struct.error:print 'Xlib.xauth: warning, failed to parse part of xauthority file {0}, aborting all further parsing'.format(D)
		if len(F.entries)==0:print'Xlib.xauth: warning, no xauthority details available'
	def __len__(A):return len(A.entries)
	def __getitem__(A,i):return A.entries[i]
	def get_best_auth(F,family,address,dispno,types=('MIT-MAGIC-COOKIE-1',)):
		'Find an authentication entry matching FAMILY, ADDRESS and\n        DISPNO.\n\n        The name of the auth scheme must match one of the names in\n        TYPES.  If several entries match, the first scheme in TYPES\n        will be choosen.\n\n        If an entry is found, the tuple (name, data) is returned,\n        otherwise XNoAuthError is raised.\n        ';C=dispno;B=address;A=family;G=str(C).encode();D={}
		for (H,I,J,K,L) in F.entries:
			if H==A and I==B and G==J:D[K]=L
		for E in types:
			try:return E,D[E]
			except KeyError:pass
		raise error.XNoAuthError((A,B,C))