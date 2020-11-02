_F='type'
_E='code'
_D='sequence_number'
_C='resource_id'
_B='minor_opcode'
_A='major_opcode'
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
	_fields=rq.Struct(rq.Card8(_F),rq.Card8(_E),rq.Card16(_D),rq.Card32(_C),rq.Card16(_B),rq.Card8(_A),rq.Pad(21))
	def __init__(A,display,data):A._data,data=A._fields.parse_binary(data,display,rawdict=1)
	def __str__(A):
		B=[]
		for C in (_E,_C,_D,_A,_B):B.append('{0} = {1}'.format(C,A._data[C]))
		return '{0}: {1}'.format(A.__class__,', '.join(B))
class XResourceError(XError):_fields=rq.Struct(rq.Card8(_F),rq.Card8(_E),rq.Card16(_D),rq.Resource(_C),rq.Card16(_B),rq.Card8(_A),rq.Pad(21))
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
class CatchError(object):
	def __init__(A,*B):A.error_types=B;A.error=None;A.request=None
	def __call__(A,error,request):
		C=request;B=error
		if A.error_types:
			for D in A.error_types:
				if isinstance(B,D):A.error=B;A.request=C;return 1
			return 0
		else:A.error=B;A.request=C;return 1
	def get_error(A):return A.error
	def get_request(A):return A.request
	def reset(A):A.error=None;A.request=None