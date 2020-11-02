_Aw='confine_to'
_Av='default_char'
_Au='dst_drawable'
_At='screen_green'
_As='max_bounds'
_Ar='events'
_Aq='min_bounds'
_Ap='bell_percent'
_Ao='screen_red'
_An='button'
_Am='masks'
_Al='exact_blue'
_Ak='child'
_Aj='focus'
_Ai='screen_blue'
_Ah='dashes'
_Ag='cmaps'
_Af='hosts'
_Ae='exact_red'
_Ad='threshold'
_Ac='max_names'
_Ab='paths'
_Aa='bell_duration'
_AZ='format'
_AY='allow_exposures'
_AX='src_drawable'
_AW='key_click_percent'
_AV='contiguous'
_AU='revert_to'
_AT='children'
_AS='timeout'
_AR='char_infos'
_AQ='first_keycode'
_AP='min_byte1'
_AO='bell_pitch'
_AN='interval'
_AM='all_chars_exist'
_AL='max_char_or_byte2'
_AK='min_char_or_byte2'
_AJ='fonts'
_AI='source'
_AH='names'
_AG='exact_green'
_AF='atoms'
_AE='same_screen'
_AD='plane_mask'
_AC='accel_num'
_AB='max_byte1'
_AA='parent'
_A9='selection'
_A8='back_blue'
_A7='points'
_A6='items'
_A5='coord_mode'
_A4='draw_direction'
_A3='blue'
_A2='rectangles'
_A1='green'
_A0='font'
_z='value'
_y='fore_green'
_x='font_descent'
_w='key'
_v='root'
_u='font_ascent'
_t='border_width'
_s='fore_blue'
_r='fore_red'
_q='pixel'
_p='back_red'
_o='red'
_n='cid'
_m='back_green'
_l='pointer_mode'
_k='keycodes'
_j='src_y'
_i='src_x'
_h='modifiers'
_g='owner_events'
_f='keyboard_mode'
_e='colors'
_d='status'
_c='event_mask'
_b='pattern'
_a='dst_x'
_Z='mask'
_Y='property'
_X='dst_y'
_W='visual'
_V='depth'
_U='data'
_T='map'
_S='cursor'
_R='keysyms'
_Q='pixels'
_P='attrs'
_O='properties'
_N='string'
_M='grab_window'
_L='mode'
_K='time'
_J='height'
_I='width'
_H='y'
_G='x'
_F='cmap'
_E='name'
_D='drawable'
_C='gc'
_B='window'
_A='sequence_number'
from ..  import X
from .  import rq
from .  import structs
class CreateWindow(rq.Request):_request=rq.Struct(rq.Opcode(1),rq.Card8(_V),rq.RequestLength(),rq.Window('wid'),rq.Window(_AA),rq.Int16(_G),rq.Int16(_H),rq.Card16(_I),rq.Card16(_J),rq.Card16(_t),rq.Set('window_class',2,(X.CopyFromParent,X.InputOutput,X.InputOnly)),rq.Card32(_W),structs.WindowValues(_P))
class ChangeWindowAttributes(rq.Request):_request=rq.Struct(rq.Opcode(2),rq.Pad(1),rq.RequestLength(),rq.Window(_B),structs.WindowValues(_P))
class GetWindowAttributes(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(3),rq.Pad(1),rq.RequestLength(),rq.Window(_B));_reply=rq.Struct(rq.ReplyCode(),rq.Card8('backing_store'),rq.Card16(_A),rq.ReplyLength(),rq.Card32(_W),rq.Card16('win_class'),rq.Card8('bit_gravity'),rq.Card8('win_gravity'),rq.Card32('backing_bit_planes'),rq.Card32('backing_pixel'),rq.Card8('save_under'),rq.Card8('map_is_installed'),rq.Card8('map_state'),rq.Card8('override_redirect'),rq.Colormap('colormap',(X.NONE,)),rq.Card32('all_event_masks'),rq.Card32('your_event_mask'),rq.Card16('do_not_propagate_mask'),rq.Pad(2))
class DestroyWindow(rq.Request):_request=rq.Struct(rq.Opcode(4),rq.Pad(1),rq.RequestLength(),rq.Window(_B))
class DestroySubWindows(rq.Request):_request=rq.Struct(rq.Opcode(5),rq.Pad(1),rq.RequestLength(),rq.Window(_B))
class ChangeSaveSet(rq.Request):_request=rq.Struct(rq.Opcode(6),rq.Set(_L,1,(X.SetModeInsert,X.SetModeDelete)),rq.RequestLength(),rq.Window(_B))
class ReparentWindow(rq.Request):_request=rq.Struct(rq.Opcode(7),rq.Pad(1),rq.RequestLength(),rq.Window(_B),rq.Window(_AA),rq.Int16(_G),rq.Int16(_H))
class MapWindow(rq.Request):_request=rq.Struct(rq.Opcode(8),rq.Pad(1),rq.RequestLength(),rq.Window(_B))
class MapSubwindows(rq.Request):_request=rq.Struct(rq.Opcode(9),rq.Pad(1),rq.RequestLength(),rq.Window(_B))
class UnmapWindow(rq.Request):_request=rq.Struct(rq.Opcode(10),rq.Pad(1),rq.RequestLength(),rq.Window(_B))
class UnmapSubwindows(rq.Request):_request=rq.Struct(rq.Opcode(11),rq.Pad(1),rq.RequestLength(),rq.Window(_B))
class ConfigureWindow(rq.Request):_request=rq.Struct(rq.Opcode(12),rq.Pad(1),rq.RequestLength(),rq.Window(_B),rq.ValueList(_P,2,2,rq.Int16(_G),rq.Int16(_H),rq.Card16(_I),rq.Card16(_J),rq.Int16(_t),rq.Window('sibling'),rq.Set('stack_mode',1,(X.Above,X.Below,X.TopIf,X.BottomIf,X.Opposite))))
class CirculateWindow(rq.Request):_request=rq.Struct(rq.Opcode(13),rq.Set('direction',1,(X.RaiseLowest,X.LowerHighest)),rq.RequestLength(),rq.Window(_B))
class GetGeometry(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(14),rq.Pad(1),rq.RequestLength(),rq.Drawable(_D));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_V),rq.Card16(_A),rq.ReplyLength(),rq.Window(_v),rq.Int16(_G),rq.Int16(_H),rq.Card16(_I),rq.Card16(_J),rq.Card16(_t),rq.Pad(10))
class QueryTree(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(15),rq.Pad(1),rq.RequestLength(),rq.Window(_B));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.Window(_v),rq.Window(_AA,(X.NONE,)),rq.LengthOf(_AT,2),rq.Pad(14),rq.List(_AT,rq.WindowObj))
class InternAtom(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(16),rq.Bool('only_if_exists'),rq.RequestLength(),rq.LengthOf(_E,2),rq.Pad(2),rq.String8(_E));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.Card32('atom'),rq.Pad(20))
class GetAtomName(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(17),rq.Pad(1),rq.RequestLength(),rq.Card32('atom'));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.LengthOf(_E,2),rq.Pad(22),rq.String8(_E))
class ChangeProperty(rq.Request):_request=rq.Struct(rq.Opcode(18),rq.Set(_L,1,(X.PropModeReplace,X.PropModePrepend,X.PropModeAppend)),rq.RequestLength(),rq.Window(_B),rq.Card32(_Y),rq.Card32('type'),rq.Format(_U,1),rq.Pad(3),rq.LengthOf(_U,4),rq.PropertyData(_U))
class DeleteProperty(rq.Request):_request=rq.Struct(rq.Opcode(19),rq.Pad(1),rq.RequestLength(),rq.Window(_B),rq.Card32(_Y))
class GetProperty(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(20),rq.Bool('delete'),rq.RequestLength(),rq.Window(_B),rq.Card32(_Y),rq.Card32('type'),rq.Card32('long_offset'),rq.Card32('long_length'));_reply=rq.Struct(rq.ReplyCode(),rq.Format(_z,1),rq.Card16(_A),rq.ReplyLength(),rq.Card32('property_type'),rq.Card32('bytes_after'),rq.LengthOf(_z,4),rq.Pad(12),rq.PropertyData(_z))
class ListProperties(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(21),rq.Pad(1),rq.RequestLength(),rq.Window(_B));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.LengthOf(_AF,2),rq.Pad(22),rq.List(_AF,rq.Card32Obj))
class SetSelectionOwner(rq.Request):_request=rq.Struct(rq.Opcode(22),rq.Pad(1),rq.RequestLength(),rq.Window(_B),rq.Card32(_A9),rq.Card32(_K))
class GetSelectionOwner(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(23),rq.Pad(1),rq.RequestLength(),rq.Card32(_A9));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.Window('owner',(X.NONE,)),rq.Pad(20))
class ConvertSelection(rq.Request):_request=rq.Struct(rq.Opcode(24),rq.Pad(1),rq.RequestLength(),rq.Window('requestor'),rq.Card32(_A9),rq.Card32('target'),rq.Card32(_Y),rq.Card32(_K))
class SendEvent(rq.Request):_request=rq.Struct(rq.Opcode(25),rq.Bool('propagate'),rq.RequestLength(),rq.Window('destination'),rq.Card32(_c),rq.EventField('event'))
class GrabPointer(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(26),rq.Bool(_g),rq.RequestLength(),rq.Window(_M),rq.Card16(_c),rq.Set(_l,1,(X.GrabModeSync,X.GrabModeAsync)),rq.Set(_f,1,(X.GrabModeSync,X.GrabModeAsync)),rq.Window(_Aw,(X.NONE,)),rq.Cursor(_S,(X.NONE,)),rq.Card32(_K));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_d),rq.Card16(_A),rq.ReplyLength(),rq.Pad(24))
class UngrabPointer(rq.Request):_request=rq.Struct(rq.Opcode(27),rq.Pad(1),rq.RequestLength(),rq.Card32(_K))
class GrabButton(rq.Request):_request=rq.Struct(rq.Opcode(28),rq.Bool(_g),rq.RequestLength(),rq.Window(_M),rq.Card16(_c),rq.Set(_l,1,(X.GrabModeSync,X.GrabModeAsync)),rq.Set(_f,1,(X.GrabModeSync,X.GrabModeAsync)),rq.Window(_Aw,(X.NONE,)),rq.Cursor(_S,(X.NONE,)),rq.Card8(_An),rq.Pad(1),rq.Card16(_h))
class UngrabButton(rq.Request):_request=rq.Struct(rq.Opcode(29),rq.Card8(_An),rq.RequestLength(),rq.Window(_M),rq.Card16(_h),rq.Pad(2))
class ChangeActivePointerGrab(rq.Request):_request=rq.Struct(rq.Opcode(30),rq.Pad(1),rq.RequestLength(),rq.Cursor(_S),rq.Card32(_K),rq.Card16(_c),rq.Pad(2))
class GrabKeyboard(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(31),rq.Bool(_g),rq.RequestLength(),rq.Window(_M),rq.Card32(_K),rq.Set(_l,1,(X.GrabModeSync,X.GrabModeAsync)),rq.Set(_f,1,(X.GrabModeSync,X.GrabModeAsync)),rq.Pad(2));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_d),rq.Card16(_A),rq.ReplyLength(),rq.Pad(24))
class UngrabKeyboard(rq.Request):_request=rq.Struct(rq.Opcode(32),rq.Pad(1),rq.RequestLength(),rq.Card32(_K))
class GrabKey(rq.Request):_request=rq.Struct(rq.Opcode(33),rq.Bool(_g),rq.RequestLength(),rq.Window(_M),rq.Card16(_h),rq.Card8(_w),rq.Set(_l,1,(X.GrabModeSync,X.GrabModeAsync)),rq.Set(_f,1,(X.GrabModeSync,X.GrabModeAsync)),rq.Pad(3))
class UngrabKey(rq.Request):_request=rq.Struct(rq.Opcode(34),rq.Card8(_w),rq.RequestLength(),rq.Window(_M),rq.Card16(_h),rq.Pad(2))
class AllowEvents(rq.Request):_request=rq.Struct(rq.Opcode(35),rq.Set(_L,1,(X.AsyncPointer,X.SyncPointer,X.ReplayPointer,X.AsyncKeyboard,X.SyncKeyboard,X.ReplayKeyboard,X.AsyncBoth,X.SyncBoth)),rq.RequestLength(),rq.Card32(_K))
class GrabServer(rq.Request):_request=rq.Struct(rq.Opcode(36),rq.Pad(1),rq.RequestLength())
class UngrabServer(rq.Request):_request=rq.Struct(rq.Opcode(37),rq.Pad(1),rq.RequestLength())
class QueryPointer(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(38),rq.Pad(1),rq.RequestLength(),rq.Window(_B));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_AE),rq.Card16(_A),rq.ReplyLength(),rq.Window(_v),rq.Window(_Ak,(X.NONE,)),rq.Int16('root_x'),rq.Int16('root_y'),rq.Int16('win_x'),rq.Int16('win_y'),rq.Card16(_Z),rq.Pad(6))
class GetMotionEvents(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(39),rq.Pad(1),rq.RequestLength(),rq.Window(_B),rq.Card32('start'),rq.Card32('stop'));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.LengthOf(_Ar,4),rq.Pad(20),rq.List(_Ar,structs.TimeCoord))
class TranslateCoords(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(40),rq.Pad(1),rq.RequestLength(),rq.Window('src_wid'),rq.Window('dst_wid'),rq.Int16(_i),rq.Int16(_j));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_AE),rq.Card16(_A),rq.ReplyLength(),rq.Window(_Ak,(X.NONE,)),rq.Int16(_G),rq.Int16(_H),rq.Pad(16))
class WarpPointer(rq.Request):_request=rq.Struct(rq.Opcode(41),rq.Pad(1),rq.RequestLength(),rq.Window('src_window'),rq.Window('dst_window'),rq.Int16(_i),rq.Int16(_j),rq.Card16('src_width'),rq.Card16('src_height'),rq.Int16(_a),rq.Int16(_X))
class SetInputFocus(rq.Request):_request=rq.Struct(rq.Opcode(42),rq.Set(_AU,1,(X.RevertToNone,X.RevertToPointerRoot,X.RevertToParent)),rq.RequestLength(),rq.Window(_Aj),rq.Card32(_K))
class GetInputFocus(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(43),rq.Pad(1),rq.RequestLength());_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_AU),rq.Card16(_A),rq.ReplyLength(),rq.Window(_Aj,(X.NONE,X.PointerRoot)),rq.Pad(20))
class QueryKeymap(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(44),rq.Pad(1),rq.RequestLength());_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.FixedList(_T,32,rq.Card8Obj))
class OpenFont(rq.Request):_request=rq.Struct(rq.Opcode(45),rq.Pad(1),rq.RequestLength(),rq.Font('fid'),rq.LengthOf(_E,2),rq.Pad(2),rq.String8(_E))
class CloseFont(rq.Request):_request=rq.Struct(rq.Opcode(46),rq.Pad(1),rq.RequestLength(),rq.Font(_A0))
class QueryFont(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(47),rq.Pad(1),rq.RequestLength(),rq.Fontable(_A0));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.Object(_Aq,structs.CharInfo),rq.Pad(4),rq.Object(_As,structs.CharInfo),rq.Pad(4),rq.Card16(_AK),rq.Card16(_AL),rq.Card16(_Av),rq.LengthOf(_O,2),rq.Card8(_A4),rq.Card8(_AP),rq.Card8(_AB),rq.Card8(_AM),rq.Int16(_u),rq.Int16(_x),rq.LengthOf(_AR,4),rq.List(_O,structs.FontProp),rq.List(_AR,structs.CharInfo))
class QueryTextExtents(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(48),rq.OddLength(_N),rq.RequestLength(),rq.Fontable(_A0),rq.String16(_N));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_A4),rq.Card16(_A),rq.ReplyLength(),rq.Int16(_u),rq.Int16(_x),rq.Int16('overall_ascent'),rq.Int16('overall_descent'),rq.Int32('overall_width'),rq.Int32('overall_left'),rq.Int32('overall_right'),rq.Pad(4))
class ListFonts(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(49),rq.Pad(1),rq.RequestLength(),rq.Card16(_Ac),rq.LengthOf(_b,2),rq.String8(_b));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.LengthOf(_AJ,2),rq.Pad(22),rq.List(_AJ,rq.Str))
class ListFontsWithInfo(rq.ReplyRequest):
	_request=rq.Struct(rq.Opcode(50),rq.Pad(1),rq.RequestLength(),rq.Card16(_Ac),rq.LengthOf(_b,2),rq.String8(_b));_reply=rq.Struct(rq.ReplyCode(),rq.LengthOf(_E,1),rq.Card16(_A),rq.ReplyLength(),rq.Object(_Aq,structs.CharInfo),rq.Pad(4),rq.Object(_As,structs.CharInfo),rq.Pad(4),rq.Card16(_AK),rq.Card16(_AL),rq.Card16(_Av),rq.LengthOf(_O,2),rq.Card8(_A4),rq.Card8(_AP),rq.Card8(_AB),rq.Card8(_AM),rq.Int16(_u),rq.Int16(_x),rq.Card32('replies_hint'),rq.List(_O,structs.FontProp),rq.String8(_E))
	def __init__(A,*B,**C):A._fonts=[];rq.ReplyRequest.__init__(A,*B,**C)
	def _parse_response(A,data):
		if ord(data[1])==0:A._response_lock.acquire();A._data=A._fonts;del A._fonts;A._response_lock.release();return
		B,C=A._reply.parse_binary(data);A._fonts.append(B);A._display.sent_requests.insert(0,A)
	def __getattr__(A,attr):raise AttributeError(attr)
	def __getitem__(A,item):return A._data[item]
	def __len__(A):return len(A._data)
class SetFontPath(rq.Request):_request=rq.Struct(rq.Opcode(51),rq.Pad(1),rq.RequestLength(),rq.LengthOf('path',2),rq.Pad(2),rq.List('path',rq.Str))
class GetFontPath(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(52),rq.Pad(1),rq.RequestLength());_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.LengthOf(_Ab,2),rq.Pad(22),rq.List(_Ab,rq.Str))
class CreatePixmap(rq.Request):_request=rq.Struct(rq.Opcode(53),rq.Card8(_V),rq.RequestLength(),rq.Pixmap('pid'),rq.Drawable(_D),rq.Card16(_I),rq.Card16(_J))
class FreePixmap(rq.Request):_request=rq.Struct(rq.Opcode(54),rq.Pad(1),rq.RequestLength(),rq.Pixmap('pixmap'))
class CreateGC(rq.Request):_request=rq.Struct(rq.Opcode(55),rq.Pad(1),rq.RequestLength(),rq.GC(_n),rq.Drawable(_D),structs.GCValues(_P))
class ChangeGC(rq.Request):_request=rq.Struct(rq.Opcode(56),rq.Pad(1),rq.RequestLength(),rq.GC(_C),structs.GCValues(_P))
class CopyGC(rq.Request):_request=rq.Struct(rq.Opcode(57),rq.Pad(1),rq.RequestLength(),rq.GC('src_gc'),rq.GC('dst_gc'),rq.Card32(_Z))
class SetDashes(rq.Request):_request=rq.Struct(rq.Opcode(58),rq.Pad(1),rq.RequestLength(),rq.GC(_C),rq.Card16('dash_offset'),rq.LengthOf(_Ah,2),rq.List(_Ah,rq.Card8Obj))
class SetClipRectangles(rq.Request):_request=rq.Struct(rq.Opcode(59),rq.Set('ordering',1,(X.Unsorted,X.YSorted,X.YXSorted,X.YXBanded)),rq.RequestLength(),rq.GC(_C),rq.Int16('x_origin'),rq.Int16('y_origin'),rq.List(_A2,structs.Rectangle))
class FreeGC(rq.Request):_request=rq.Struct(rq.Opcode(60),rq.Pad(1),rq.RequestLength(),rq.GC(_C))
class ClearArea(rq.Request):_request=rq.Struct(rq.Opcode(61),rq.Bool('exposures'),rq.RequestLength(),rq.Window(_B),rq.Int16(_G),rq.Int16(_H),rq.Card16(_I),rq.Card16(_J))
class CopyArea(rq.Request):_request=rq.Struct(rq.Opcode(62),rq.Pad(1),rq.RequestLength(),rq.Drawable(_AX),rq.Drawable(_Au),rq.GC(_C),rq.Int16(_i),rq.Int16(_j),rq.Int16(_a),rq.Int16(_X),rq.Card16(_I),rq.Card16(_J))
class CopyPlane(rq.Request):_request=rq.Struct(rq.Opcode(63),rq.Pad(1),rq.RequestLength(),rq.Drawable(_AX),rq.Drawable(_Au),rq.GC(_C),rq.Int16(_i),rq.Int16(_j),rq.Int16(_a),rq.Int16(_X),rq.Card16(_I),rq.Card16(_J),rq.Card32('bit_plane'))
class PolyPoint(rq.Request):_request=rq.Struct(rq.Opcode(64),rq.Set(_A5,1,(X.CoordModeOrigin,X.CoordModePrevious)),rq.RequestLength(),rq.Drawable(_D),rq.GC(_C),rq.List(_A7,structs.Point))
class PolyLine(rq.Request):_request=rq.Struct(rq.Opcode(65),rq.Set(_A5,1,(X.CoordModeOrigin,X.CoordModePrevious)),rq.RequestLength(),rq.Drawable(_D),rq.GC(_C),rq.List(_A7,structs.Point))
class PolySegment(rq.Request):_request=rq.Struct(rq.Opcode(66),rq.Pad(1),rq.RequestLength(),rq.Drawable(_D),rq.GC(_C),rq.List('segments',structs.Segment))
class PolyRectangle(rq.Request):_request=rq.Struct(rq.Opcode(67),rq.Pad(1),rq.RequestLength(),rq.Drawable(_D),rq.GC(_C),rq.List(_A2,structs.Rectangle))
class PolyArc(rq.Request):_request=rq.Struct(rq.Opcode(68),rq.Pad(1),rq.RequestLength(),rq.Drawable(_D),rq.GC(_C),rq.List('arcs',structs.Arc))
class FillPoly(rq.Request):_request=rq.Struct(rq.Opcode(69),rq.Pad(1),rq.RequestLength(),rq.Drawable(_D),rq.GC(_C),rq.Set('shape',1,(X.Complex,X.Nonconvex,X.Convex)),rq.Set(_A5,1,(X.CoordModeOrigin,X.CoordModePrevious)),rq.Pad(2),rq.List(_A7,structs.Point))
class PolyFillRectangle(rq.Request):_request=rq.Struct(rq.Opcode(70),rq.Pad(1),rq.RequestLength(),rq.Drawable(_D),rq.GC(_C),rq.List(_A2,structs.Rectangle))
class PolyFillArc(rq.Request):_request=rq.Struct(rq.Opcode(71),rq.Pad(1),rq.RequestLength(),rq.Drawable(_D),rq.GC(_C),rq.List('arcs',structs.Arc))
class PutImage(rq.Request):_request=rq.Struct(rq.Opcode(72),rq.Set(_AZ,1,(X.XYBitmap,X.XYPixmap,X.ZPixmap)),rq.RequestLength(),rq.Drawable(_D),rq.GC(_C),rq.Card16(_I),rq.Card16(_J),rq.Int16(_a),rq.Int16(_X),rq.Card8('left_pad'),rq.Card8(_V),rq.Pad(2),rq.Binary(_U))
class GetImage(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(73),rq.Set(_AZ,1,(X.XYPixmap,X.ZPixmap)),rq.RequestLength(),rq.Drawable(_D),rq.Int16(_G),rq.Int16(_H),rq.Card16(_I),rq.Card16(_J),rq.Card32(_AD));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_V),rq.Card16(_A),rq.ReplyLength(),rq.Card32(_W),rq.Pad(20),rq.Binary(_U))
class PolyText8(rq.Request):_request=rq.Struct(rq.Opcode(74),rq.Pad(1),rq.RequestLength(),rq.Drawable(_D),rq.GC(_C),rq.Int16(_G),rq.Int16(_H),rq.TextElements8(_A6))
class PolyText16(rq.Request):_request=rq.Struct(rq.Opcode(75),rq.Pad(1),rq.RequestLength(),rq.Drawable(_D),rq.GC(_C),rq.Int16(_G),rq.Int16(_H),rq.TextElements16(_A6))
class ImageText8(rq.Request):_request=rq.Struct(rq.Opcode(76),rq.LengthOf(_N,1),rq.RequestLength(),rq.Drawable(_D),rq.GC(_C),rq.Int16(_G),rq.Int16(_H),rq.String8(_N))
class ImageText16(rq.Request):_request=rq.Struct(rq.Opcode(77),rq.LengthOf(_N,1),rq.RequestLength(),rq.Drawable(_D),rq.GC(_C),rq.Int16(_G),rq.Int16(_H),rq.String16(_N))
class CreateColormap(rq.Request):_request=rq.Struct(rq.Opcode(78),rq.Set('alloc',1,(X.AllocNone,X.AllocAll)),rq.RequestLength(),rq.Colormap('mid'),rq.Window(_B),rq.Card32(_W))
class FreeColormap(rq.Request):_request=rq.Struct(rq.Opcode(79),rq.Pad(1),rq.RequestLength(),rq.Colormap(_F))
class CopyColormapAndFree(rq.Request):_request=rq.Struct(rq.Opcode(80),rq.Pad(1),rq.RequestLength(),rq.Colormap('mid'),rq.Colormap('src_cmap'))
class InstallColormap(rq.Request):_request=rq.Struct(rq.Opcode(81),rq.Pad(1),rq.RequestLength(),rq.Colormap(_F))
class UninstallColormap(rq.Request):_request=rq.Struct(rq.Opcode(82),rq.Pad(1),rq.RequestLength(),rq.Colormap(_F))
class ListInstalledColormaps(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(83),rq.Pad(1),rq.RequestLength(),rq.Window(_B));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.LengthOf(_Ag,2),rq.Pad(22),rq.List(_Ag,rq.ColormapObj))
class AllocColor(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(84),rq.Pad(1),rq.RequestLength(),rq.Colormap(_F),rq.Card16(_o),rq.Card16(_A1),rq.Card16(_A3),rq.Pad(2));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.Card16(_o),rq.Card16(_A1),rq.Card16(_A3),rq.Pad(2),rq.Card32(_q),rq.Pad(12))
class AllocNamedColor(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(85),rq.Pad(1),rq.RequestLength(),rq.Colormap(_F),rq.LengthOf(_E,2),rq.Pad(2),rq.String8(_E));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.Card32(_q),rq.Card16(_Ae),rq.Card16(_AG),rq.Card16(_Al),rq.Card16(_Ao),rq.Card16(_At),rq.Card16(_Ai),rq.Pad(8))
class AllocColorCells(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(86),rq.Bool(_AV),rq.RequestLength(),rq.Colormap(_F),rq.Card16(_e),rq.Card16('planes'));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.LengthOf(_Q,2),rq.LengthOf(_Am,2),rq.Pad(20),rq.List(_Q,rq.Card32Obj),rq.List(_Am,rq.Card32Obj))
class AllocColorPlanes(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(87),rq.Bool(_AV),rq.RequestLength(),rq.Colormap(_F),rq.Card16(_e),rq.Card16(_o),rq.Card16(_A1),rq.Card16(_A3));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.LengthOf(_Q,2),rq.Pad(2),rq.Card32('red_mask'),rq.Card32('green_mask'),rq.Card32('blue_mask'),rq.Pad(8),rq.List(_Q,rq.Card32Obj))
class FreeColors(rq.Request):_request=rq.Struct(rq.Opcode(88),rq.Pad(1),rq.RequestLength(),rq.Colormap(_F),rq.Card32(_AD),rq.List(_Q,rq.Card32Obj))
class StoreColors(rq.Request):_request=rq.Struct(rq.Opcode(89),rq.Pad(1),rq.RequestLength(),rq.Colormap(_F),rq.List(_A6,structs.ColorItem))
class StoreNamedColor(rq.Request):_request=rq.Struct(rq.Opcode(90),rq.Card8('flags'),rq.RequestLength(),rq.Colormap(_F),rq.Card32(_q),rq.LengthOf(_E,2),rq.Pad(2),rq.String8(_E))
class QueryColors(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(91),rq.Pad(1),rq.RequestLength(),rq.Colormap(_F),rq.List(_Q,rq.Card32Obj));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.LengthOf(_e,2),rq.Pad(22),rq.List(_e,structs.RGB))
class LookupColor(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(92),rq.Pad(1),rq.RequestLength(),rq.Colormap(_F),rq.LengthOf(_E,2),rq.Pad(2),rq.String8(_E));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.Card16(_Ae),rq.Card16(_AG),rq.Card16(_Al),rq.Card16(_Ao),rq.Card16(_At),rq.Card16(_Ai),rq.Pad(12))
class CreateCursor(rq.Request):_request=rq.Struct(rq.Opcode(93),rq.Pad(1),rq.RequestLength(),rq.Cursor(_n),rq.Pixmap(_AI),rq.Pixmap(_Z),rq.Card16(_r),rq.Card16(_y),rq.Card16(_s),rq.Card16(_p),rq.Card16(_m),rq.Card16(_A8),rq.Card16(_G),rq.Card16(_H))
class CreateGlyphCursor(rq.Request):_request=rq.Struct(rq.Opcode(94),rq.Pad(1),rq.RequestLength(),rq.Cursor(_n),rq.Font(_AI),rq.Font(_Z),rq.Card16('source_char'),rq.Card16('mask_char'),rq.Card16(_r),rq.Card16(_y),rq.Card16(_s),rq.Card16(_p),rq.Card16(_m),rq.Card16(_A8))
class FreeCursor(rq.Request):_request=rq.Struct(rq.Opcode(95),rq.Pad(1),rq.RequestLength(),rq.Cursor(_S))
class RecolorCursor(rq.Request):_request=rq.Struct(rq.Opcode(96),rq.Pad(1),rq.RequestLength(),rq.Cursor(_S),rq.Card16(_r),rq.Card16(_y),rq.Card16(_s),rq.Card16(_p),rq.Card16(_m),rq.Card16(_A8))
class QueryBestSize(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(97),rq.Set('item_class',1,(X.CursorShape,X.TileShape,X.StippleShape)),rq.RequestLength(),rq.Drawable(_D),rq.Card16(_I),rq.Card16(_J));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.Card16(_I),rq.Card16(_J),rq.Pad(20))
class QueryExtension(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(98),rq.Pad(1),rq.RequestLength(),rq.LengthOf(_E,2),rq.Pad(2),rq.String8(_E));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.Card8('present'),rq.Card8('major_opcode'),rq.Card8('first_event'),rq.Card8('first_error'),rq.Pad(20))
class ListExtensions(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(99),rq.Pad(1),rq.RequestLength());_reply=rq.Struct(rq.ReplyCode(),rq.LengthOf(_AH,1),rq.Card16(_A),rq.ReplyLength(),rq.Pad(24),rq.List(_AH,rq.Str))
class ChangeKeyboardMapping(rq.Request):_request=rq.Struct(rq.Opcode(100),rq.LengthOf(_R,1),rq.RequestLength(),rq.Card8(_AQ),rq.Format(_R,1),rq.Pad(2),rq.KeyboardMapping(_R))
class GetKeyboardMapping(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(101),rq.Pad(1),rq.RequestLength(),rq.Card8(_AQ),rq.Card8('count'),rq.Pad(2));_reply=rq.Struct(rq.ReplyCode(),rq.Format(_R,1),rq.Card16(_A),rq.ReplyLength(),rq.Pad(24),rq.KeyboardMapping(_R))
class ChangeKeyboardControl(rq.Request):_request=rq.Struct(rq.Opcode(102),rq.Pad(1),rq.RequestLength(),rq.ValueList(_P,4,0,rq.Int8(_AW),rq.Int8(_Ap),rq.Int16(_AO),rq.Int16(_Aa),rq.Card8('led'),rq.Set('led_mode',1,(X.LedModeOff,X.LedModeOn)),rq.Card8(_w),rq.Set('auto_repeat_mode',1,(X.AutoRepeatModeOff,X.AutoRepeatModeOn,X.AutoRepeatModeDefault))))
class GetKeyboardControl(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(103),rq.Pad(1),rq.RequestLength());_reply=rq.Struct(rq.ReplyCode(),rq.Card8('global_auto_repeat'),rq.Card16(_A),rq.ReplyLength(),rq.Card32('led_mask'),rq.Card8(_AW),rq.Card8(_Ap),rq.Card16(_AO),rq.Card16(_Aa),rq.Pad(2),rq.FixedList('auto_repeats',32,rq.Card8Obj))
class Bell(rq.Request):_request=rq.Struct(rq.Opcode(104),rq.Int8('percent'),rq.RequestLength())
class ChangePointerControl(rq.Request):_request=rq.Struct(rq.Opcode(105),rq.Pad(1),rq.RequestLength(),rq.Int16(_AC),rq.Int16('accel_denum'),rq.Int16(_Ad),rq.Bool('do_accel'),rq.Bool('do_thresh'))
class GetPointerControl(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(106),rq.Pad(1),rq.RequestLength());_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.Card16(_AC),rq.Card16('accel_denom'),rq.Card16(_Ad),rq.Pad(18))
class SetScreenSaver(rq.Request):_request=rq.Struct(rq.Opcode(107),rq.Pad(1),rq.RequestLength(),rq.Int16(_AS),rq.Int16(_AN),rq.Set('prefer_blank',1,(X.DontPreferBlanking,X.PreferBlanking,X.DefaultBlanking)),rq.Set(_AY,1,(X.DontAllowExposures,X.AllowExposures,X.DefaultExposures)),rq.Pad(2))
class GetScreenSaver(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(108),rq.Pad(1),rq.RequestLength());_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_A),rq.ReplyLength(),rq.Card16(_AS),rq.Card16(_AN),rq.Card8('prefer_blanking'),rq.Card8(_AY),rq.Pad(18))
class ChangeHosts(rq.Request):_request=rq.Struct(rq.Opcode(109),rq.Set(_L,1,(X.HostInsert,X.HostDelete)),rq.RequestLength(),rq.Set('host_family',1,(X.FamilyInternet,X.FamilyDECnet,X.FamilyChaos)),rq.Pad(1),rq.LengthOf('host',2),rq.List('host',rq.Card8Obj))
class ListHosts(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(110),rq.Pad(1),rq.RequestLength());_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_L),rq.Card16(_A),rq.ReplyLength(),rq.LengthOf(_Af,2),rq.Pad(22),rq.List(_Af,structs.Host))
class SetAccessControl(rq.Request):_request=rq.Struct(rq.Opcode(111),rq.Set(_L,1,(X.DisableAccess,X.EnableAccess)),rq.RequestLength())
class SetCloseDownMode(rq.Request):_request=rq.Struct(rq.Opcode(112),rq.Set(_L,1,(X.DestroyAll,X.RetainPermanent,X.RetainTemporary)),rq.RequestLength())
class KillClient(rq.Request):_request=rq.Struct(rq.Opcode(113),rq.Pad(1),rq.RequestLength(),rq.Resource('resource'))
class RotateProperties(rq.Request):_request=rq.Struct(rq.Opcode(114),rq.Pad(1),rq.RequestLength(),rq.Window(_B),rq.LengthOf(_O,2),rq.Int16('delta'),rq.List(_O,rq.Card32Obj))
class ForceScreenSaver(rq.Request):_request=rq.Struct(rq.Opcode(115),rq.Set(_L,1,(X.ScreenSaverReset,X.ScreenSaverActive)),rq.RequestLength())
class SetPointerMapping(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(116),rq.LengthOf(_T,1),rq.RequestLength(),rq.List(_T,rq.Card8Obj));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_d),rq.Card16(_A),rq.ReplyLength(),rq.Pad(24))
class GetPointerMapping(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(117),rq.Pad(1),rq.RequestLength());_reply=rq.Struct(rq.ReplyCode(),rq.LengthOf(_T,1),rq.Card16(_A),rq.ReplyLength(),rq.Pad(24),rq.List(_T,rq.Card8Obj))
class SetModifierMapping(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(118),rq.Format(_k,1),rq.RequestLength(),rq.ModifierMapping(_k));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_d),rq.Card16(_A),rq.ReplyLength(),rq.Pad(24))
class GetModifierMapping(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(119),rq.Pad(1),rq.RequestLength());_reply=rq.Struct(rq.ReplyCode(),rq.Format(_k,1),rq.Card16(_A),rq.ReplyLength(),rq.Pad(24),rq.ModifierMapping(_k))
class NoOperation(rq.Request):_request=rq.Struct(rq.Opcode(127),rq.Pad(1),rq.RequestLength())
major_codes={1:CreateWindow,2:ChangeWindowAttributes,3:GetWindowAttributes,4:DestroyWindow,5:DestroySubWindows,6:ChangeSaveSet,7:ReparentWindow,8:MapWindow,9:MapSubwindows,10:UnmapWindow,11:UnmapSubwindows,12:ConfigureWindow,13:CirculateWindow,14:GetGeometry,15:QueryTree,16:InternAtom,17:GetAtomName,18:ChangeProperty,19:DeleteProperty,20:GetProperty,21:ListProperties,22:SetSelectionOwner,23:GetSelectionOwner,24:ConvertSelection,25:SendEvent,26:GrabPointer,27:UngrabPointer,28:GrabButton,29:UngrabButton,30:ChangeActivePointerGrab,31:GrabKeyboard,32:UngrabKeyboard,33:GrabKey,34:UngrabKey,35:AllowEvents,36:GrabServer,37:UngrabServer,38:QueryPointer,39:GetMotionEvents,40:TranslateCoords,41:WarpPointer,42:SetInputFocus,43:GetInputFocus,44:QueryKeymap,45:OpenFont,46:CloseFont,47:QueryFont,48:QueryTextExtents,49:ListFonts,50:ListFontsWithInfo,51:SetFontPath,52:GetFontPath,53:CreatePixmap,54:FreePixmap,55:CreateGC,56:ChangeGC,57:CopyGC,58:SetDashes,59:SetClipRectangles,60:FreeGC,61:ClearArea,62:CopyArea,63:CopyPlane,64:PolyPoint,65:PolyLine,66:PolySegment,67:PolyRectangle,68:PolyArc,69:FillPoly,70:PolyFillRectangle,71:PolyFillArc,72:PutImage,73:GetImage,74:PolyText8,75:PolyText16,76:ImageText8,77:ImageText16,78:CreateColormap,79:FreeColormap,80:CopyColormapAndFree,81:InstallColormap,82:UninstallColormap,83:ListInstalledColormaps,84:AllocColor,85:AllocNamedColor,86:AllocColorCells,87:AllocColorPlanes,88:FreeColors,89:StoreColors,90:StoreNamedColor,91:QueryColors,92:LookupColor,93:CreateCursor,94:CreateGlyphCursor,95:FreeCursor,96:RecolorCursor,97:QueryBestSize,98:QueryExtension,99:ListExtensions,100:ChangeKeyboardMapping,101:GetKeyboardMapping,102:ChangeKeyboardControl,103:GetKeyboardControl,104:Bell,105:ChangePointerControl,106:GetPointerControl,107:SetScreenSaver,108:GetScreenSaver,109:ChangeHosts,110:ListHosts,111:SetAccessControl,112:SetCloseDownMode,113:KillClient,114:RotateProperties,115:ForceScreenSaver,116:SetPointerMapping,117:GetPointerMapping,118:SetModifierMapping,119:GetModifierMapping,127:NoOperation}