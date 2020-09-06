_d='root_x'
_c='root_y'
_b='target'
_a='selection'
_Z='mode'
_Y='event_x'
_X='event_y'
_W='major_event'
_V='minor_event'
_U='atom'
_T='child'
_S='root'
_R='requestor'
_Q='property'
_P='count'
_O='border_width'
_N='data'
_M='parent'
_L='detail'
_K='override'
_J='state'
_I='height'
_H='width'
_G='time'
_F='x'
_E='event'
_D='y'
_C='window'
_B='sequence_number'
_A='type'
from ..  import X
from .  import rq
class AnyEvent(rq.Event):_code=None;_fields=rq.Struct(rq.Card8(_A),rq.Card8(_L),rq.Card16(_B),rq.FixedBinary(_N,28))
class KeyButtonPointer(rq.Event):_code=None;_fields=rq.Struct(rq.Card8(_A),rq.Card8(_L),rq.Card16(_B),rq.Card32(_G),rq.Window(_S),rq.Window(_C),rq.Window(_T,(X.NONE,)),rq.Int16(_d),rq.Int16(_c),rq.Int16(_Y),rq.Int16(_X),rq.Card16(_J),rq.Card8('same_screen'),rq.Pad(1))
class KeyPress(KeyButtonPointer):_code=X.KeyPress
class KeyRelease(KeyButtonPointer):_code=X.KeyRelease
class ButtonPress(KeyButtonPointer):_code=X.ButtonPress
class ButtonRelease(KeyButtonPointer):_code=X.ButtonRelease
class MotionNotify(KeyButtonPointer):_code=X.MotionNotify
class EnterLeave(rq.Event):_code=None;_fields=rq.Struct(rq.Card8(_A),rq.Card8(_L),rq.Card16(_B),rq.Card32(_G),rq.Window(_S),rq.Window(_C),rq.Window(_T,(X.NONE,)),rq.Int16(_d),rq.Int16(_c),rq.Int16(_Y),rq.Int16(_X),rq.Card16(_J),rq.Card8(_Z),rq.Card8('flags'))
class EnterNotify(EnterLeave):_code=X.EnterNotify
class LeaveNotify(EnterLeave):_code=X.LeaveNotify
class Focus(rq.Event):_code=None;_fields=rq.Struct(rq.Card8(_A),rq.Card8(_L),rq.Card16(_B),rq.Window(_C),rq.Card8(_Z),rq.Pad(23))
class FocusIn(Focus):_code=X.FocusIn
class FocusOut(Focus):_code=X.FocusOut
class Expose(rq.Event):_code=X.Expose;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_C),rq.Card16(_F),rq.Card16(_D),rq.Card16(_H),rq.Card16(_I),rq.Card16(_P),rq.Pad(14))
class GraphicsExpose(rq.Event):_code=X.GraphicsExpose;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Drawable('drawable'),rq.Card16(_F),rq.Card16(_D),rq.Card16(_H),rq.Card16(_I),rq.Card16(_V),rq.Card16(_P),rq.Card8(_W),rq.Pad(11))
class NoExpose(rq.Event):_code=X.NoExpose;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Drawable(_C),rq.Card16(_V),rq.Card8(_W),rq.Pad(21))
class VisibilityNotify(rq.Event):_code=X.VisibilityNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_C),rq.Card8(_J),rq.Pad(23))
class CreateNotify(rq.Event):_code=X.CreateNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_M),rq.Window(_C),rq.Int16(_F),rq.Int16(_D),rq.Card16(_H),rq.Card16(_I),rq.Card16(_O),rq.Card8(_K),rq.Pad(9))
class DestroyNotify(rq.Event):_code=X.DestroyNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_E),rq.Window(_C),rq.Pad(20))
class UnmapNotify(rq.Event):_code=X.UnmapNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_E),rq.Window(_C),rq.Card8('from_configure'),rq.Pad(19))
class MapNotify(rq.Event):_code=X.MapNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_E),rq.Window(_C),rq.Card8(_K),rq.Pad(19))
class MapRequest(rq.Event):_code=X.MapRequest;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_M),rq.Window(_C),rq.Pad(20))
class ReparentNotify(rq.Event):_code=X.ReparentNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_E),rq.Window(_C),rq.Window(_M),rq.Int16(_F),rq.Int16(_D),rq.Card8(_K),rq.Pad(11))
class ConfigureNotify(rq.Event):_code=X.ConfigureNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_E),rq.Window(_C),rq.Window('above_sibling',(X.NONE,)),rq.Int16(_F),rq.Int16(_D),rq.Card16(_H),rq.Card16(_I),rq.Card16(_O),rq.Card8(_K),rq.Pad(5))
class ConfigureRequest(rq.Event):_code=X.ConfigureRequest;_fields=rq.Struct(rq.Card8(_A),rq.Card8('stack_mode'),rq.Card16(_B),rq.Window(_M),rq.Window(_C),rq.Window('sibling',(X.NONE,)),rq.Int16(_F),rq.Int16(_D),rq.Card16(_H),rq.Card16(_I),rq.Card16(_O),rq.Card16('value_mask'),rq.Pad(4))
class GravityNotify(rq.Event):_code=X.GravityNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_E),rq.Window(_C),rq.Int16(_F),rq.Int16(_D),rq.Pad(16))
class ResizeRequest(rq.Event):_code=X.ResizeRequest;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_C),rq.Card16(_H),rq.Card16(_I),rq.Pad(20))
class Circulate(rq.Event):_code=None;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_E),rq.Window(_C),rq.Pad(4),rq.Card8('place'),rq.Pad(15))
class CirculateNotify(Circulate):_code=X.CirculateNotify
class CirculateRequest(Circulate):_code=X.CirculateRequest
class PropertyNotify(rq.Event):_code=X.PropertyNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_C),rq.Card32(_U),rq.Card32(_G),rq.Card8(_J),rq.Pad(15))
class SelectionClear(rq.Event):_code=X.SelectionClear;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Card32(_G),rq.Window(_C),rq.Card32(_U),rq.Pad(16))
class SelectionRequest(rq.Event):_code=X.SelectionRequest;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Card32(_G),rq.Window('owner'),rq.Window(_R),rq.Card32(_a),rq.Card32(_b),rq.Card32(_Q),rq.Pad(4))
class SelectionNotify(rq.Event):_code=X.SelectionNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Card32(_G),rq.Window(_R),rq.Card32(_a),rq.Card32(_b),rq.Card32(_Q),rq.Pad(8))
class ColormapNotify(rq.Event):_code=X.ColormapNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_C),rq.Colormap('colormap',(X.NONE,)),rq.Card8('new'),rq.Card8(_J),rq.Pad(18))
class MappingNotify(rq.Event):_code=X.MappingNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Card8('request'),rq.Card8('first_keycode'),rq.Card8(_P),rq.Pad(25))
class ClientMessage(rq.Event):_code=X.ClientMessage;_fields=rq.Struct(rq.Card8(_A),rq.Format(_N,1),rq.Card16(_B),rq.Window(_C),rq.Card32('client_type'),rq.FixedPropertyData(_N,20))
class KeymapNotify(rq.Event):_code=X.KeymapNotify;_fields=rq.Struct(rq.Card8(_A),rq.FixedList(_N,31,rq.Card8Obj,pad=0))
event_class={X.KeyPress:KeyPress,X.KeyRelease:KeyRelease,X.ButtonPress:ButtonPress,X.ButtonRelease:ButtonRelease,X.MotionNotify:MotionNotify,X.EnterNotify:EnterNotify,X.LeaveNotify:LeaveNotify,X.FocusIn:FocusIn,X.FocusOut:FocusOut,X.KeymapNotify:KeymapNotify,X.Expose:Expose,X.GraphicsExpose:GraphicsExpose,X.NoExpose:NoExpose,X.VisibilityNotify:VisibilityNotify,X.CreateNotify:CreateNotify,X.DestroyNotify:DestroyNotify,X.UnmapNotify:UnmapNotify,X.MapNotify:MapNotify,X.MapRequest:MapRequest,X.ReparentNotify:ReparentNotify,X.ConfigureNotify:ConfigureNotify,X.ConfigureRequest:ConfigureRequest,X.GravityNotify:GravityNotify,X.ResizeRequest:ResizeRequest,X.CirculateNotify:CirculateNotify,X.CirculateRequest:CirculateRequest,X.PropertyNotify:PropertyNotify,X.SelectionClear:SelectionClear,X.SelectionRequest:SelectionRequest,X.SelectionNotify:SelectionNotify,X.ColormapNotify:ColormapNotify,X.ClientMessage:ClientMessage,X.MappingNotify:MappingNotify}