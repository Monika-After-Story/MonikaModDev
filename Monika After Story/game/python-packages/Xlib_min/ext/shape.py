_K='ordering'
_J='source_kind'
_I='rectangles'
_H='operation'
_G='destination_kind'
_F='y_offset'
_E='x_offset'
_D='sequence_number'
_C='destination_window'
_B='window'
_A='opcode'
from Xlib.protocol import rq,structs
extname='SHAPE'
OP=rq.Card8
class SO:Set=0;Union=1;Intersect=2;Subtract=3;Invert=4
class SK:Bounding=0;Clip=1;Input=2
class KIND(rq.Set):
	def __init__(A,name):super(KIND,A).__init__(name,1,values=(SK.Bounding,SK.Clip,SK.Input))
class NotifyEventData(rq.Event):_code=None;_fields=rq.Struct(rq.Card8('type'),KIND('shape_kind'),rq.Card16(_D),rq.Window('affected_window'),rq.Int16('extents_x'),rq.Int16('extents_y'),rq.Card16('extents_width'),rq.Card16('extents_height'),rq.Card32('server_time'),rq.Card8('shaped'),rq.Pad(11))
class QueryVersion(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(0),rq.RequestLength());_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_D),rq.ReplyLength(),rq.Card16('major_version'),rq.Card16('minor_version'))
class Rectangles(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(1),rq.RequestLength(),OP(_H),KIND(_G),rq.Card8(_K),rq.Pad(1),rq.Window(_C),rq.Int16(_E),rq.Int16(_F),rq.List(_I,structs.Rectangle,pad=0))
class Mask(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(2),rq.RequestLength(),OP(_H),KIND(_G),rq.Pad(2),rq.Window(_C),rq.Int16(_E),rq.Int16(_F),rq.Pixmap('source_bitmap'))
class Combine(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(3),rq.RequestLength(),OP(_H),KIND(_G),KIND(_J),rq.Pad(1),rq.Window(_C),rq.Int16(_E),rq.Int16(_F),rq.Window('source_window'))
class Offset(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(4),rq.RequestLength(),KIND(_G),rq.Pad(3),rq.Window(_C),rq.Int16(_E),rq.Int16(_F))
class QueryExtents(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(5),rq.RequestLength(),rq.Window(_C));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_D),rq.ReplyLength(),rq.Card8('bounding_shaped'),rq.Card8('clip_shaped'),rq.Pad(2),rq.Int16('bounding_shape_extents_x'),rq.Int16('bounding_shape_extents_y'),rq.Card16('bounding_shape_extents_width'),rq.Card16('bounding_shape_extents_height'),rq.Int16('clip_shape_extents_x'),rq.Int16('clip_shape_extents_y'),rq.Card16('clip_shape_extents_width'),rq.Card16('clip_shape_extents_height'))
class SelectInput(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(6),rq.RequestLength(),rq.Window(_C),rq.Card8('enable'),rq.Pad(3))
class InputSelected(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(7),rq.RequestLength(),rq.Window(_C));_reply=rq.Struct(rq.ReplyCode(),rq.Card8('enabled'),rq.Card16(_D),rq.ReplyLength())
class GetRectangles(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(8),rq.RequestLength(),rq.Window(_B),KIND(_J),rq.Pad(3));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_K),rq.Card16(_D),rq.ReplyLength(),rq.LengthOf(_I,4),rq.Pad(20),rq.List(_I,structs.Rectangle,pad=0))
class Event:Notify=0
def combine(self,operation,destination_kind,source_kind,x_offset,y_offset):A=self;Combine(display=A.display,opcode=A.display.get_extension_major(extname),source_window=A,operation=operation,destination_kind=destination_kind,source_kind=source_kind,x_offset=x_offset,y_offset=y_offset)
def get_rectangles(self,source_kind):A=self;return GetRectangles(display=A.display,opcode=A.display.get_extension_major(extname),window=A,source_kind=source_kind)
def input_selected(self):A=self;return InputSelected(display=A.display,opcode=A.display.get_extension_major(extname),destination_window=A)
def mask(self,operation,destination_kind,x_offset,y_offset,source_bitmap):A=self;Mask(display=A.display,opcode=A.display.get_extension_major(extname),destination_window=A,operation=operation,destination_kind=destination_kind,x_offset=x_offset,y_offset=y_offset,source_bitmap=source_bitmap)
def offset(self,destination_kind,x_offset,y_offset):A=self;Offset(display=A.display,opcode=A.display.get_extension_major(extname),destination_window=A,destination_kind=destination_kind,x_offset=x_offset,y_offset=y_offset)
def query_extents(self):A=self;return QueryExtents(display=A.display,opcode=A.display.get_extension_major(extname),destination_window=A)
def query_version(self):return QueryVersion(display=self.display,opcode=self.display.get_extension_major(extname))
def rectangles(self,operation,destination_kind,ordering,x_offset,y_offset,rectangles):A=self;Rectangles(display=A.display,opcode=A.display.get_extension_major(extname),destination_window=A,operation=operation,destination_kind=destination_kind,ordering=ordering,x_offset=x_offset,y_offset=y_offset,rectangles=rectangles)
def select_input(self,enable):A=self;SelectInput(display=A.display,opcode=A.display.get_extension_major(extname),destination_window=A,enable=enable)
def init(disp,info):A=disp;A.extension_add_method(_B,'shape_combine',combine);A.extension_add_method(_B,'shape_get_rectangles',get_rectangles);A.extension_add_method(_B,'shape_input_selected',input_selected);A.extension_add_method(_B,'shape_mask',mask);A.extension_add_method(_B,'shape_offset',offset);A.extension_add_method(_B,'shape_query_extents',query_extents);A.extension_add_method('display','shape_query_version',query_version);A.extension_add_method(_B,'shape_rectangles',rectangles);A.extension_add_method(_B,'shape_select_input',select_input);A.extension_add_event(info.first_event+Event.Notify,NotifyEventData,'ShapeNotify')