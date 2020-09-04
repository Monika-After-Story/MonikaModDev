# Xlib.error -- basic error classes
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

_G='type'
_F='major_opcode'
_E='minor_opcode'
_D='resource_id'
_C='sequence_number'
_B='code'
_A=None
from .  import X
from .protocol import rq
class DisplayError(Exception):
	def __init__(A,display):A.display=display
	def __str__(A):return'Display error "%s"'%A.display
class DisplayNameError(DisplayError):
	def __str__(A):return'Bad display name "%s"'%A.display
class DisplayConnectionError(DisplayError):
	def __init__(A,display,msg):A.display=display;A.msg=msg
	def __str__(A):return'Can\'t connect to display "%s": %s'%(A.display,A.msg)
class ConnectionClosedError(Exception):
	def __init__(A,whom):A.whom=whom
	def __str__(A):return'Display connection closed by %s'%A.whom
class XauthError(Exception):0
class XNoAuthError(Exception):0
class ResourceIDError(Exception):0
class XError(rq.GetAttrData,Exception):
	_fields=rq.Struct(rq.Card8(_G),rq.Card8(_B),rq.Card16(_C),rq.Card32(_D),rq.Card16(_E),rq.Card8(_F),rq.Pad(21))
	def __init__(A,display,data):A._data,data=A._fields.parse_binary(data,display,rawdict=1)
	def __str__(A):
		B=[]
		for C in (_B,_D,_C,_F,_E):B.append('{0} = {1}'.format(C,A._data[C]))
		return '{0}: {1}'.format(A.__class__,', '.join(B))
class XResourceError(XError):_fields=rq.Struct(rq.Card8(_G),rq.Card8(_B),rq.Card16(_C),rq.Resource(_D),rq.Card16(_E),rq.Card8(_F),rq.Pad(21))
class BadRequest(XError):0
class BadValue(XError):0
class BadWindow(XResourceError):0
class BadPixmap(XResourceError):0
class BadAtom(XError):0
class BadCursor(XResourceError):0
class BadFont(XResourceError):0
class BadMatch(XError):0
class BadDrawable(XResourceError):0
class BadAccess(XError):0
class BadAlloc(XError):0
class BadColor(XResourceError):0
class BadGC(XResourceError):0
class BadIDChoice(XResourceError):0
class BadName(XError):0
class BadLength(XError):0
class BadImplementation(XError):0
xerror_class={X.BadRequest:BadRequest,X.BadValue:BadValue,X.BadWindow:BadWindow,X.BadPixmap:BadPixmap,X.BadAtom:BadAtom,X.BadCursor:BadCursor,X.BadFont:BadFont,X.BadMatch:BadMatch,X.BadDrawable:BadDrawable,X.BadAccess:BadAccess,X.BadAlloc:BadAlloc,X.BadColor:BadColor,X.BadGC:BadGC,X.BadIDChoice:BadIDChoice,X.BadName:BadName,X.BadLength:BadLength,X.BadImplementation:BadImplementation}
class CatchError:
	def __init__(A,*B):A.error_types=B;A.error=_A;A.request=_A
	def __call__(A,error,request):
		C=request;B=error
		if A.error_types:
			for D in A.error_types:
				if isinstance(B,D):A.error=B;A.request=C;return 1
			return 0
		else:A.error=B;A.request=C;return 1
	def get_error(A):return A.error
	def get_request(A):return A.request
	def reset(A):A.error=_A;A.request=_A
