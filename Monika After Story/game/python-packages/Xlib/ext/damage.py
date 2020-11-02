_I='repair'
_H='major_version'
_G='sequence_number'
_F='level'
_E='minor_version'
_D='parts'
_C='drawable'
_B='damage'
_A='opcode'
from Xlib import X
from Xlib.protocol import rq,structs
from Xlib.xobject import resource
from Xlib.error import XError
extname='DAMAGE'
DamageNotifyCode=0
BadDamageCode=0
class BadDamageError(XError):0
DamageReportRawRectangles=0
DamageReportDeltaRectangles=1
DamageReportBoundingBox=2
DamageReportNonEmpty=3
DamageReportLevel=DamageReportRawRectangles,DamageReportDeltaRectangles,DamageReportBoundingBox,DamageReportNonEmpty
DAMAGE=rq.Card32
class QueryVersion(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(0),rq.RequestLength(),rq.Card32(_H),rq.Card32(_E));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_G),rq.ReplyLength(),rq.Card32(_H),rq.Card32(_E),rq.Pad(16))
def query_version(self):return QueryVersion(display=self.display,opcode=self.display.get_extension_major(extname),major_version=1,minor_version=1)
class DamageCreate(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(1),rq.RequestLength(),DAMAGE(_B),rq.Drawable(_C),rq.Set(_F,1,DamageReportLevel),rq.Pad(3))
def damage_create(self,level):A=self;B=A.display.allocate_resource_id();DamageCreate(display=A.display,opcode=A.display.get_extension_major(extname),damage=B,drawable=A.id,level=level);return B
class DamageDestroy(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(2),rq.RequestLength(),DAMAGE(_B))
def damage_destroy(self,damage):B=damage;A=self;DamageDestroy(display=A.display,opcode=A.display.get_extension_major(extname),damage=B);A.display.free_resource_id(B)
class DamageSubtract(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(3),rq.RequestLength(),DAMAGE(_B),rq.Card32(_I),rq.Card32(_D))
def damage_subtract(self,damage,repair=X.NONE,parts=X.NONE):DamageSubtract(display=self.display,opcode=self.display.get_extension_major(extname),damage=damage,repair=repair,parts=parts)
class DamageAdd(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(4),rq.RequestLength(),rq.Card32(_I),rq.Card32(_D))
def damage_add(self,repair,parts):DamageAdd(display=self.display,opcode=self.display.get_extension_major(extname),repair=repair,parts=parts)
class DamageNotify(rq.Event):_code=None;_fields=rq.Struct(rq.Card8('type'),rq.Card8(_F),rq.Card16(_G),rq.Drawable(_C),DAMAGE(_B),rq.Card32('timestamp'),rq.Object('area',structs.Rectangle),rq.Object('drawable_geometry',structs.Rectangle))
def init(disp,info):B='display';A=disp;A.extension_add_method(B,'damage_query_version',query_version);A.extension_add_method(_C,'damage_create',damage_create);A.extension_add_method(B,'damage_destroy',damage_destroy);A.extension_add_method(B,'damage_subtract',damage_subtract);A.extension_add_method(_C,'damage_add',damage_add);A.extension_add_event(info.first_event+DamageNotifyCode,DamageNotify);A.add_extension_error(code=BadDamageCode,err=BadDamageError)