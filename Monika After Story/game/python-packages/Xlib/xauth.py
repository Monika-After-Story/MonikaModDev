# Xlib.xauth -- ~/.Xauthority access
#
#    Copyright (C) 2000 Peter Liljenberg <petli@ctrl-c.liu.se>
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

_A=None
import os,struct
from Xlib import X,error
FamilyInternet=X.FamilyInternet
FamilyDECnet=X.FamilyDECnet
FamilyChaos=X.FamilyChaos
FamilyLocal=256
class Xauthority:
	def __init__(F,filename=_A):
		E='>H';D=filename
		if D is _A:D=os.environ.get('XAUTHORITY')
		if D is _A:
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
		except struct.error:print('Xlib.xauth: warning, failed to parse part of xauthority file {0}, aborting all further parsing'.format(D))
		if len(F.entries)==0:print('Xlib.xauth: warning, no xauthority details available')
	def __len__(A):return len(A.entries)
	def __getitem__(A,i):return A.entries[i]
	def get_best_auth(F,family,address,dispno,types=(b'MIT-MAGIC-COOKIE-1',)):
		C=dispno;B=address;A=family;G=str(C).encode();D={}
		for (H,I,J,K,L) in F.entries:
			if H==A and I==B and G==J:D[K]=L
		for E in types:
			try:return E,D[E]
			except KeyError:pass
		raise error.XNoAuthError((A,B,C))
