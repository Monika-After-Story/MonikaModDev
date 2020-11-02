'\nge - Generic Event Extension\n'
_D='major_version'
_C='sequence_number'
_B='ge_event_data'
_A='minor_version'
from Xlib.protocol import rq
extname='Generic Event Extension'
GenericEventCode=35
class GEQueryVersion(rq.ReplyRequest):_request=rq.Struct(rq.Card8('opcode'),rq.Opcode(0),rq.RequestLength(),rq.Card32(_D),rq.Card32(_A));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_C),rq.ReplyLength(),rq.Card32(_D),rq.Card32(_A),rq.Pad(16))
def query_version(self):return GEQueryVersion(display=self.display,opcode=self.display.get_extension_major(extname),major_version=1,minor_version=0)
class GenericEvent(rq.Event):
	_code=GenericEventCode;_fields=rq.Struct(rq.Card8('type'),rq.Card8('extension'),rq.Card16(_C),rq.Card32('length'),rq.Card16('evtype'))
	def __init__(B,binarydata=None,display=None,**G):
		C=display;A=binarydata
		if A:D=A[10:];A=A[:10]
		else:D=''
		rq.Event.__init__(B,binarydata=A,display=C,**G)
		if C:
			E=getattr(C,_B,None)
			if E:
				F=E.get((B.extension,B.evtype),None)
				if F:D,H=F.parse_binary(D,C)
		B._data['data']=D
def add_event_data(self,extension,evtype,estruct):
	A=self
	if not hasattr(A.display,_B):A.display.ge_event_data={}
	A.display.ge_event_data[(extension,evtype)]=estruct
def init(disp,info):B='display';A=disp;A.extension_add_method(B,'ge_query_version',query_version);A.extension_add_method(B,'ge_add_event_data',add_event_data);A.extension_add_event(GenericEventCode,GenericEvent)