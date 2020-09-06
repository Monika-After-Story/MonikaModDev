_K='client_info'
_J='minor_version'
_I='last'
_H='major_version'
_G='first'
_F='sequence_number'
_E='element_header'
_D='ranges'
_C='clients'
_B='context'
_A='opcode'
from Xlib import X
from Xlib.protocol import rq
extname='RECORD'
FromServerTime=1
FromClientTime=2
FromClientSequence=4
CurrentClients=1
FutureClients=2
AllClients=3
FromServer=0
FromClient=1
ClientStarted=2
ClientDied=3
StartOfData=4
EndOfData=5
Record_Range8=rq.Struct(rq.Card8(_G),rq.Card8(_I))
Record_Range16=rq.Struct(rq.Card16(_G),rq.Card16(_I))
Record_ExtRange=rq.Struct(rq.Card8('major_range_first'),rq.Card8('major_range_last'),rq.Card16('minor_range_first'),rq.Card16('minor_range_last'))
Record_Range=rq.Struct(rq.Object('core_requests',Record_Range8),rq.Object('core_replies',Record_Range8),rq.Object('ext_requests',Record_ExtRange),rq.Object('ext_replies',Record_ExtRange),rq.Object('delivered_events',Record_Range8),rq.Object('device_events',Record_Range8),rq.Object('errors',Record_Range8),rq.Bool('client_started'),rq.Bool('client_died'))
Record_ClientInfo=rq.Struct(rq.Card32('client_resource'),rq.LengthOf(_D,4),rq.List(_D,Record_Range))
class RawField(rq.ValueField):
	'A field with raw data, stored as a string';structcode=None
	def pack_value(A,val):return val,len(val),None
	def parse_binary_value(A,data,display,length,format):return data,''
class GetVersion(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(0),rq.RequestLength(),rq.Card16(_H),rq.Card16(_J));_reply=rq.Struct(rq.Pad(2),rq.Card16(_F),rq.ReplyLength(),rq.Card16(_H),rq.Card16(_J),rq.Pad(20))
def get_version(self,major,minor):return GetVersion(display=self.display,opcode=self.display.get_extension_major(extname),major_version=major,minor_version=minor)
class CreateContext(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(1),rq.RequestLength(),rq.Card32(_B),rq.Card8(_E),rq.Pad(3),rq.LengthOf(_C,4),rq.LengthOf(_D,4),rq.List(_C,rq.Card32Obj),rq.List(_D,Record_Range))
def create_context(self,datum_flags,clients,ranges):A=self;B=A.display.allocate_resource_id();CreateContext(display=A.display,opcode=A.display.get_extension_major(extname),context=B,element_header=datum_flags,clients=clients,ranges=ranges);return B
class RegisterClients(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(2),rq.RequestLength(),rq.Card32(_B),rq.Card8(_E),rq.Pad(3),rq.LengthOf(_C,4),rq.LengthOf(_D,4),rq.List(_C,rq.Card32Obj),rq.List(_D,Record_Range))
def register_clients(self,context,element_header,clients,ranges):RegisterClients(display=self.display,opcode=self.display.get_extension_major(extname),context=context,element_header=element_header,clients=clients,ranges=ranges)
class UnregisterClients(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(3),rq.RequestLength(),rq.Card32(_B),rq.LengthOf(_C,4),rq.List(_C,rq.Card32Obj))
def unregister_clients(self,context,clients):UnregisterClients(display=self.display,opcode=self.display.get_extension_major(extname),context=context,clients=clients)
class GetContext(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(4),rq.RequestLength(),rq.Card32(_B));_reply=rq.Struct(rq.Pad(2),rq.Card16(_F),rq.ReplyLength(),rq.Card8(_E),rq.Pad(3),rq.LengthOf(_K,4),rq.Pad(16),rq.List(_K,Record_ClientInfo))
def get_context(self,context):return GetContext(display=self.display,opcode=self.display.get_extension_major(extname),context=context)
class EnableContext(rq.ReplyRequest):
	_request=rq.Struct(rq.Card8(_A),rq.Opcode(5),rq.RequestLength(),rq.Card32(_B));_reply=rq.Struct(rq.Pad(1),rq.Card8('category'),rq.Card16(_F),rq.ReplyLength(),rq.Card8(_E),rq.Bool('client_swapped'),rq.Pad(2),rq.Card32('id_base'),rq.Card32('server_time'),rq.Card32('recorded_sequence_number'),rq.Pad(8),RawField('data'))
	def __init__(A,callback,*B,**C):A._callback=callback;rq.ReplyRequest.__init__(A,*B,**C)
	def _parse_response(A,data):
		B,C=A._reply.parse_binary(data,A._display);A._callback(B)
		if B.category==StartOfData:A.sequence_number=B.sequence_number
		if B.category==EndOfData:A._response_lock.acquire();A._data=B;A._response_lock.release()
		else:A._display.sent_requests.insert(0,A)
def enable_context(self,context,callback):EnableContext(callback=callback,display=self.display,opcode=self.display.get_extension_major(extname),context=context)
class DisableContext(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(6),rq.RequestLength(),rq.Card32(_B))
def disable_context(self,context):DisableContext(display=self.display,opcode=self.display.get_extension_major(extname),context=context)
class FreeContext(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(7),rq.RequestLength(),rq.Card32(_B))
def free_context(self,context):B=context;A=self;FreeContext(display=A.display,opcode=A.display.get_extension_major(extname),context=B);A.display.free_resource_id(B)
def init(disp,info):B='display';A=disp;A.extension_add_method(B,'record_get_version',get_version);A.extension_add_method(B,'record_create_context',create_context);A.extension_add_method(B,'record_register_clients',register_clients);A.extension_add_method(B,'record_unregister_clients',unregister_clients);A.extension_add_method(B,'record_get_context',get_context);A.extension_add_method(B,'record_enable_context',enable_context);A.extension_add_method(B,'record_disable_context',disable_context);A.extension_add_method(B,'record_free_context',free_context)