# Xlib.protocol.event -- definitions of core events
#
#    Copyright (C) 2000-2002 Peter Liljenberg <petli@ctrl-c.liu.se>
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

_e='property'
_d='target'
_c='selection'
_b='requestor'
_a='atom'
_Z='major_event'
_Y='minor_event'
_X='mode'
_W='event_y'
_V='event_x'
_U='root_y'
_T='root_x'
_S='child'
_R='root'
_Q='border_width'
_P='count'
_O='override'
_N='parent'
_M='data'
_L='detail'
_K='state'
_J=None
_I='height'
_H='width'
_G='time'
_F='event'
_E='y'
_D='x'
_C='window'
_B='sequence_number'
_A='type'
from ..  import X
from .  import rq
class AnyEvent(rq.Event):_code=_J;_fields=rq.Struct(rq.Card8(_A),rq.Card8(_L),rq.Card16(_B),rq.FixedBinary(_M,28))
class KeyButtonPointer(rq.Event):_code=_J;_fields=rq.Struct(rq.Card8(_A),rq.Card8(_L),rq.Card16(_B),rq.Card32(_G),rq.Window(_R),rq.Window(_C),rq.Window(_S,(X.NONE,)),rq.Int16(_T),rq.Int16(_U),rq.Int16(_V),rq.Int16(_W),rq.Card16(_K),rq.Card8('same_screen'),rq.Pad(1))
class KeyPress(KeyButtonPointer):_code=X.KeyPress
class KeyRelease(KeyButtonPointer):_code=X.KeyRelease
class ButtonPress(KeyButtonPointer):_code=X.ButtonPress
class ButtonRelease(KeyButtonPointer):_code=X.ButtonRelease
class MotionNotify(KeyButtonPointer):_code=X.MotionNotify
class EnterLeave(rq.Event):_code=_J;_fields=rq.Struct(rq.Card8(_A),rq.Card8(_L),rq.Card16(_B),rq.Card32(_G),rq.Window(_R),rq.Window(_C),rq.Window(_S,(X.NONE,)),rq.Int16(_T),rq.Int16(_U),rq.Int16(_V),rq.Int16(_W),rq.Card16(_K),rq.Card8(_X),rq.Card8('flags'))
class EnterNotify(EnterLeave):_code=X.EnterNotify
class LeaveNotify(EnterLeave):_code=X.LeaveNotify
class Focus(rq.Event):_code=_J;_fields=rq.Struct(rq.Card8(_A),rq.Card8(_L),rq.Card16(_B),rq.Window(_C),rq.Card8(_X),rq.Pad(23))
class FocusIn(Focus):_code=X.FocusIn
class FocusOut(Focus):_code=X.FocusOut
class Expose(rq.Event):_code=X.Expose;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_C),rq.Card16(_D),rq.Card16(_E),rq.Card16(_H),rq.Card16(_I),rq.Card16(_P),rq.Pad(14))
class GraphicsExpose(rq.Event):_code=X.GraphicsExpose;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Drawable('drawable'),rq.Card16(_D),rq.Card16(_E),rq.Card16(_H),rq.Card16(_I),rq.Card16(_Y),rq.Card16(_P),rq.Card8(_Z),rq.Pad(11))
class NoExpose(rq.Event):_code=X.NoExpose;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Drawable(_C),rq.Card16(_Y),rq.Card8(_Z),rq.Pad(21))
class VisibilityNotify(rq.Event):_code=X.VisibilityNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_C),rq.Card8(_K),rq.Pad(23))
class CreateNotify(rq.Event):_code=X.CreateNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_N),rq.Window(_C),rq.Int16(_D),rq.Int16(_E),rq.Card16(_H),rq.Card16(_I),rq.Card16(_Q),rq.Card8(_O),rq.Pad(9))
class DestroyNotify(rq.Event):_code=X.DestroyNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_F),rq.Window(_C),rq.Pad(20))
class UnmapNotify(rq.Event):_code=X.UnmapNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_F),rq.Window(_C),rq.Card8('from_configure'),rq.Pad(19))
class MapNotify(rq.Event):_code=X.MapNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_F),rq.Window(_C),rq.Card8(_O),rq.Pad(19))
class MapRequest(rq.Event):_code=X.MapRequest;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_N),rq.Window(_C),rq.Pad(20))
class ReparentNotify(rq.Event):_code=X.ReparentNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_F),rq.Window(_C),rq.Window(_N),rq.Int16(_D),rq.Int16(_E),rq.Card8(_O),rq.Pad(11))
class ConfigureNotify(rq.Event):_code=X.ConfigureNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_F),rq.Window(_C),rq.Window('above_sibling',(X.NONE,)),rq.Int16(_D),rq.Int16(_E),rq.Card16(_H),rq.Card16(_I),rq.Card16(_Q),rq.Card8(_O),rq.Pad(5))
class ConfigureRequest(rq.Event):_code=X.ConfigureRequest;_fields=rq.Struct(rq.Card8(_A),rq.Card8('stack_mode'),rq.Card16(_B),rq.Window(_N),rq.Window(_C),rq.Window('sibling',(X.NONE,)),rq.Int16(_D),rq.Int16(_E),rq.Card16(_H),rq.Card16(_I),rq.Card16(_Q),rq.Card16('value_mask'),rq.Pad(4))
class GravityNotify(rq.Event):_code=X.GravityNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_F),rq.Window(_C),rq.Int16(_D),rq.Int16(_E),rq.Pad(16))
class ResizeRequest(rq.Event):_code=X.ResizeRequest;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_C),rq.Card16(_H),rq.Card16(_I),rq.Pad(20))
class Circulate(rq.Event):_code=_J;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_F),rq.Window(_C),rq.Pad(4),rq.Card8('place'),rq.Pad(15))
class CirculateNotify(Circulate):_code=X.CirculateNotify
class CirculateRequest(Circulate):_code=X.CirculateRequest
class PropertyNotify(rq.Event):_code=X.PropertyNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_C),rq.Card32(_a),rq.Card32(_G),rq.Card8(_K),rq.Pad(15))
class SelectionClear(rq.Event):_code=X.SelectionClear;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Card32(_G),rq.Window(_C),rq.Card32(_a),rq.Pad(16))
class SelectionRequest(rq.Event):_code=X.SelectionRequest;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Card32(_G),rq.Window('owner'),rq.Window(_b),rq.Card32(_c),rq.Card32(_d),rq.Card32(_e),rq.Pad(4))
class SelectionNotify(rq.Event):_code=X.SelectionNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Card32(_G),rq.Window(_b),rq.Card32(_c),rq.Card32(_d),rq.Card32(_e),rq.Pad(8))
class ColormapNotify(rq.Event):_code=X.ColormapNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Window(_C),rq.Colormap('colormap',(X.NONE,)),rq.Card8('new'),rq.Card8(_K),rq.Pad(18))
class MappingNotify(rq.Event):_code=X.MappingNotify;_fields=rq.Struct(rq.Card8(_A),rq.Pad(1),rq.Card16(_B),rq.Card8('request'),rq.Card8('first_keycode'),rq.Card8(_P),rq.Pad(25))
class ClientMessage(rq.Event):_code=X.ClientMessage;_fields=rq.Struct(rq.Card8(_A),rq.Format(_M,1),rq.Card16(_B),rq.Window(_C),rq.Card32('client_type'),rq.FixedPropertyData(_M,20))
class KeymapNotify(rq.Event):_code=X.KeymapNotify;_fields=rq.Struct(rq.Card8(_A),rq.FixedList(_M,31,rq.Card8Obj,pad=0))
event_class={X.KeyPress:KeyPress,X.KeyRelease:KeyRelease,X.ButtonPress:ButtonPress,X.ButtonRelease:ButtonRelease,X.MotionNotify:MotionNotify,X.EnterNotify:EnterNotify,X.LeaveNotify:LeaveNotify,X.FocusIn:FocusIn,X.FocusOut:FocusOut,X.KeymapNotify:KeymapNotify,X.Expose:Expose,X.GraphicsExpose:GraphicsExpose,X.NoExpose:NoExpose,X.VisibilityNotify:VisibilityNotify,X.CreateNotify:CreateNotify,X.DestroyNotify:DestroyNotify,X.UnmapNotify:UnmapNotify,X.MapNotify:MapNotify,X.MapRequest:MapRequest,X.ReparentNotify:ReparentNotify,X.ConfigureNotify:ConfigureNotify,X.ConfigureRequest:ConfigureRequest,X.GravityNotify:GravityNotify,X.ResizeRequest:ResizeRequest,X.CirculateNotify:CirculateNotify,X.CirculateRequest:CirculateRequest,X.PropertyNotify:PropertyNotify,X.SelectionClear:SelectionClear,X.SelectionRequest:SelectionRequest,X.SelectionNotify:SelectionNotify,X.ColormapNotify:ColormapNotify,X.ClientMessage:ClientMessage,X.MappingNotify:MappingNotify}
