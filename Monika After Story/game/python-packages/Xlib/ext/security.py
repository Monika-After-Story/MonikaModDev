'\nA partial implementation of the SECURITY extension.  Support for the\nSecurityAuthorizationRevoked event is not implemented.\n'
_H='auth_data_return'
_G='major_version'
_F='auth_proto'
_E='authid'
_D='auth_data'
_C='sequence_number'
_B='minor_version'
_A='opcode'
from Xlib.protocol import rq
extname='SECURITY'
SecurityClientTrusted=0
SecurityClientUntrusted=1
SecurityAuthorizationRevokedMask=1
AUTHID=rq.Card32
class QueryVersion(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(0),rq.RequestLength(),rq.Card16(_G),rq.Card16(_B));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_C),rq.ReplyLength(),rq.Card16(_G),rq.Card16(_B),rq.Pad(20))
def query_version(self):return QueryVersion(display=self.display,opcode=self.display.get_extension_major(extname),major_version=1,minor_version=0)
class SecurityGenerateAuthorization(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(1),rq.RequestLength(),rq.LengthOf(_F,2),rq.LengthOf(_D,2),rq.Card32('value_mask'),rq.String8(_F),rq.Binary(_D),rq.List('values',rq.Card32Obj));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_C),rq.ReplyLength(),AUTHID(_E),rq.LengthOf(_H,2),rq.Pad(18),rq.Binary(_H))
def generate_authorization(self,auth_proto,auth_data='',timeout=None,trust_level=None,group=None,event_mask=None):
	F=event_mask;E=group;D=trust_level;C=timeout;A=0;B=[]
	if C is not None:A|=1;B.append(C)
	if D is not None:A|=2;B.append(D)
	if E is not None:A|=4;B.append(E)
	if F is not None:A|=8;B.append(F)
	return SecurityGenerateAuthorization(display=self.display,opcode=self.display.get_extension_major(extname),value_mask=A,auth_proto=auth_proto,auth_data=auth_data,values=B)
class SecurityRevokeAuthorization(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(2),rq.RequestLength(),AUTHID(_E))
def revoke_authorization(self,authid):return SecurityRevokeAuthorization(display=self.display,opcode=self.display.get_extension_major(extname),authid=authid)
def init(disp,info):B='display';A=disp;A.extension_add_method(B,'security_query_version',query_version);A.extension_add_method(B,'security_generate_authorization',generate_authorization);A.extension_add_method(B,'security_revoke_authorization',revoke_authorization)