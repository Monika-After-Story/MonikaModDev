'RandR - provide access to the RandR extension information.\n\nThis implementation is based off version 1.3 of the XRandR protocol, and may\nnot be compatible with other versions.\n\nVersion 1.2 of the protocol is documented at:\nhttp://cgit.freedesktop.org/xorg/proto/randrproto/tree/randrproto.txt\n\nVersion 1.3.1 here:\nhttp://www.x.org/releases/X11R7.5/doc/randrproto/randrproto.txt\n\n'
_A9='height_in_pixels'
_A8='minor_version'
_A7='border_bottom'
_A6='possible_outputs'
_A5='track_left'
_A4='track_height'
_A3='border_top'
_A2='track_top'
_A1='width_in_pixels'
_A0='border_right'
_z='current_filter_params'
_y='rates'
_x='border_left'
_w='rate'
_v='valid_values'
_u='range'
_t='top'
_s='left'
_r='current_filter_name'
_q='new_config_timestamp'
_p='filter_name'
_o='track_width'
_n='sizes'
_m='connection'
_l='pending_filter_name'
_k='names'
_j='atoms'
_i='mode_names'
_h='major_version'
_g='pending_filter_params'
_f='clones'
_e='pending'
_d='width_in_millimeters'
_c='sub_code'
_b='name'
_a='height_in_millimeters'
_Z='green'
_Y='blue'
_X='red'
_W='root'
_V='size_id'
_U='drawable'
_T='new_timestamp'
_S='property'
_R='subpixel_order'
_Q='height'
_P='width'
_O='crtcs'
_N='type'
_M='modes'
_L='value'
_K='outputs'
_J='rotation'
_I='mode'
_H='config_timestamp'
_G='status'
_F='crtc'
_E='output'
_D='timestamp'
_C='window'
_B='sequence_number'
_A='opcode'
from Xlib import X
from Xlib.protocol import rq,structs
extname='RANDR'
RRScreenChangeNotify=0
RRNotify=1
RRNotify_CrtcChange=0
RRNotify_OutputChange=1
RRNotify_OutputProperty=2
RRScreenChangeNotifyMask=1<<0
RRCrtcChangeNotifyMask=1<<1
RROutputChangeNotifyMask=1<<2
RROutputPropertyNotifyMask=1<<3
SetConfigSuccess=0
SetConfigInvalidConfigTime=1
SetConfigInvalidTime=2
SetConfigFailed=3
Rotate_0=1
Rotate_90=2
Rotate_180=4
Rotate_270=8
Reflect_X=16
Reflect_Y=32
HSyncPositive=1
HSyncNegative=2
VSyncPositive=4
VSyncNegative=8
Interlace=16
DoubleScan=32
CSync=64
CSyncPositive=128
CSyncNegative=256
HSkewPresent=512
BCast=1024
PixelMultiplex=2048
DoubleClock=4096
ClockDivideBy2=8192
Connected=0
Disconnected=1
UnknownConnection=2
PROPERTY_RANDR_EDID='EDID'
PROPERTY_SIGNAL_FORMAT='SignalFormat'
PROPERTY_SIGNAL_PROPERTIES='SignalProperties'
PROPERTY_CONNECTOR_TYPE='ConnectorType'
PROPERTY_CONNECTOR_NUMBER='ConnectorNumber'
PROPERTY_COMPATIBILITY_LIST='CompatibilityList'
PROPERTY_CLONE_LIST='CloneList'
SubPixelUnknown=0
SubPixelHorizontalRGB=1
SubPixelHorizontalBGR=2
SubPixelVerticalRGB=3
SubPixelVerticalBGR=4
SubPixelNone=5
BadRROutput=0
BadRRCrtc=1
BadRRMode=2
RandR_ScreenSizes=rq.Struct(rq.Card16(_A1),rq.Card16(_A9),rq.Card16(_d),rq.Card16(_a))
RandR_ModeInfo=rq.Struct(rq.Card32('id'),rq.Card16(_P),rq.Card16(_Q),rq.Card32('dot_clock'),rq.Card16('h_sync_start'),rq.Card16('h_sync_end'),rq.Card16('h_total'),rq.Card16('h_skew'),rq.Card16('v_sync_start'),rq.Card16('v_sync_end'),rq.Card16('v_total'),rq.Card16('name_length'),rq.Card32('flags'))
RandR_Rates=rq.Struct(rq.LengthOf(_y,2),rq.List(_y,rq.Card16Obj))
Render_Transform=rq.Struct(rq.Card32('matrix11'),rq.Card32('matrix12'),rq.Card32('matrix13'),rq.Card32('matrix21'),rq.Card32('matrix22'),rq.Card32('matrix23'),rq.Card32('matrix31'),rq.Card32('matrix32'),rq.Card32('matrix33'))
class QueryVersion(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(0),rq.RequestLength(),rq.Card32(_h),rq.Card32(_A8));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_B),rq.ReplyLength(),rq.Card32(_h),rq.Card32(_A8),rq.Pad(16))
def query_version(self):'Get the current version of the RandR extension.\n\n    ';return QueryVersion(display=self.display,opcode=self.display.get_extension_major(extname),major_version=1,minor_version=3)
class _1_0SetScreenConfig(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(2),rq.RequestLength(),rq.Drawable(_U),rq.Card32(_D),rq.Card32(_H),rq.Card16(_V),rq.Card16(_J));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_G),rq.Card16(_B),rq.ReplyLength(),rq.Card32(_T),rq.Card32(_q),rq.Window(_W),rq.Card16(_R),rq.Pad(10))
def _1_0set_screen_config(self,size_id,rotation,config_timestamp,timestamp=X.CurrentTime):'Sets the screen to the specified size and rotation.\n\n    ';A=self;return _1_0SetScreenConfig(display=A.display,opcode=A.display.get_extension_major(extname),drawable=A,timestamp=timestamp,config_timestamp=config_timestamp,size_id=size_id,rotation=rotation)
class SetScreenConfig(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(2),rq.RequestLength(),rq.Drawable(_U),rq.Card32(_D),rq.Card32(_H),rq.Card16(_V),rq.Card16(_J),rq.Card16(_w),rq.Pad(2));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_G),rq.Card16(_B),rq.ReplyLength(),rq.Card32(_T),rq.Card32(_q),rq.Window(_W),rq.Card16(_R),rq.Pad(10))
def set_screen_config(self,size_id,rotation,config_timestamp,rate=0,timestamp=X.CurrentTime):'Sets the screen to the specified size, rate, rotation and reflection.\n\n    rate can be 0 to have the server select an appropriate rate.\n\n    ';A=self;return SetScreenConfig(display=A.display,opcode=A.display.get_extension_major(extname),drawable=A,timestamp=timestamp,config_timestamp=config_timestamp,size_id=size_id,rotation=rotation,rate=rate)
class SelectInput(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(4),rq.RequestLength(),rq.Window(_C),rq.Card16('mask'),rq.Pad(2))
def select_input(self,mask):A=self;return SelectInput(display=A.display,opcode=A.display.get_extension_major(extname),window=A,mask=mask)
class GetScreenInfo(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(5),rq.RequestLength(),rq.Window(_C));_reply=rq.Struct(rq.ReplyCode(),rq.Card8('set_of_rotations'),rq.Card16(_B),rq.ReplyLength(),rq.Window(_W),rq.Card32(_D),rq.Card32(_H),rq.LengthOf(_n,2),rq.Card16(_V),rq.Card16(_J),rq.Card16(_w),rq.Card16('n_rate_ents'),rq.Pad(2),rq.List(_n,RandR_ScreenSizes))
def get_screen_info(self):'Retrieve information about the current and available configurations for\n    the screen associated with this window.\n\n    ';A=self;return GetScreenInfo(display=A.display,opcode=A.display.get_extension_major(extname),window=A)
class GetScreenSizeRange(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(6),rq.RequestLength(),rq.Window(_C));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_B),rq.ReplyLength(),rq.Card16('min_width'),rq.Card16('min_height'),rq.Card16('max_width'),rq.Card16('max_height'),rq.Pad(16))
def get_screen_size_range(self):'Retrieve the range of possible screen sizes. The screen may be set to\n\tany size within this range.\n\n    ';A=self;return GetScreenSizeRange(display=A.display,opcode=A.display.get_extension_major(extname),window=A)
class SetScreenSize(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(7),rq.RequestLength(),rq.Window(_C),rq.Card16(_P),rq.Card16(_Q),rq.Card32(_d),rq.Card32(_a))
def set_screen_size(self,width,height,width_in_millimeters=None,height_in_millimeters=None):A=self;return SetScreenSize(display=A.display,opcode=A.display.get_extension_major(extname),window=A,width=width,height=height,width_in_millimeters=width_in_millimeters,height_in_millimeters=height_in_millimeters)
class GetScreenResources(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(8),rq.RequestLength(),rq.Window(_C));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_B),rq.ReplyLength(),rq.Card32(_D),rq.Card32(_H),rq.LengthOf(_O,2),rq.LengthOf(_K,2),rq.LengthOf(_M,2),rq.LengthOf(_i,2),rq.Pad(8),rq.List(_O,rq.Card32Obj),rq.List(_K,rq.Card32Obj),rq.List(_M,RandR_ModeInfo),rq.String8(_i))
def get_screen_resources(self):A=self;return GetScreenResources(display=A.display,opcode=A.display.get_extension_major(extname),window=A)
class GetOutputInfo(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(9),rq.RequestLength(),rq.Card32(_E),rq.Card32(_H));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_G),rq.Card16(_B),rq.ReplyLength(),rq.Card32(_D),rq.Card32(_F),rq.Card32('mm_width'),rq.Card32('mm_height'),rq.Card8(_m),rq.Card8(_R),rq.LengthOf(_O,2),rq.LengthOf(_M,2),rq.Card16('num_preferred'),rq.LengthOf(_f,2),rq.LengthOf(_b,2),rq.List(_O,rq.Card32Obj),rq.List(_M,rq.Card32Obj),rq.List(_f,rq.Card32Obj),rq.String8(_b))
def get_output_info(self,output,config_timestamp):return GetOutputInfo(display=self.display,opcode=self.display.get_extension_major(extname),output=output,config_timestamp=config_timestamp)
class ListOutputProperties(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(10),rq.RequestLength(),rq.Card32(_E));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_B),rq.ReplyLength(),rq.LengthOf(_j,2),rq.Pad(22),rq.List(_j,rq.Card32Obj))
def list_output_properties(self,output):return ListOutputProperties(display=self.display,opcode=self.display.get_extension_major(extname),output=output)
class QueryOutputProperty(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(11),rq.RequestLength(),rq.Card32(_E),rq.Card32(_S));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_B),rq.ReplyLength(),rq.Bool(_e),rq.Bool(_u),rq.Bool('immutable'),rq.Pad(21),rq.List(_v,rq.Card32Obj))
def query_output_property(self,output,property):return QueryOutputProperty(display=self.display,opcode=self.display.get_extension_major(extname),output=output,property=property)
class ConfigureOutputProperty(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(12),rq.RequestLength(),rq.Card32(_E),rq.Card32(_S),rq.Bool(_e),rq.Bool(_u),rq.Pad(2),rq.List(_v,rq.Card32Obj))
def configure_output_property(self,output,property):return ConfigureOutputProperty(display=self.display,opcode=self.display.get_extension_major(extname),output=output,property=property)
class ChangeOutputProperty(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(13),rq.RequestLength(),rq.Card32(_E),rq.Card32(_S),rq.Card32(_N),rq.Format(_L,1),rq.Card8(_I),rq.Pad(2),rq.LengthOf(_L,4),rq.PropertyData(_L))
def change_output_property(self,output,property,type,mode,value):return ChangeOutputProperty(display=self.display,opcode=self.display.get_extension_major(extname),output=output,property=property,type=type,mode=mode,value=value)
class DeleteOutputProperty(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(14),rq.RequestLength(),rq.Card32(_E),rq.Card32(_S))
def delete_output_property(self,output,property):return DeleteOutputProperty(display=self.display,opcode=self.display.get_extension_major(extname),output=output,property=property)
class GetOutputProperty(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(15),rq.RequestLength(),rq.Card32(_E),rq.Card32(_S),rq.Card32(_N),rq.Card32('long_offset'),rq.Card32('long_length'),rq.Bool('delete'),rq.Bool(_e),rq.Pad(2));_reply=rq.Struct(rq.ReplyCode(),rq.Format(_L,1),rq.Card16(_B),rq.ReplyLength(),rq.Card32('property_type'),rq.Card32('bytes_after'),rq.LengthOf(_L,4),rq.Pad(12),rq.List(_L,rq.Card8Obj))
def get_output_property(self,output,property,type,long_offset,long_length,delete=False,pending=False):return GetOutputProperty(display=self.display,opcode=self.display.get_extension_major(extname),output=output,property=property,type=type,long_offset=long_offset,long_length=long_length,delete=delete,pending=pending)
class CreateMode(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(16),rq.RequestLength(),rq.Window(_C),rq.Object(_I,RandR_ModeInfo),rq.String8(_b));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_B),rq.ReplyLength(),rq.Card32(_I),rq.Pad(20))
def create_mode(self,mode,name):A=self;return CreateMode(display=A.display,opcode=A.display.get_extension_major(extname),window=A,mode=mode,name=name)
class DestroyMode(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(17),rq.RequestLength(),rq.Card32(_I))
def destroy_mode(self,mode):return DestroyMode(display=self.display,opcode=self.display.get_extension_major(extname),mode=mode)
class AddOutputMode(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(18),rq.RequestLength(),rq.Card32(_E),rq.Card32(_I))
def add_output_mode(self,output,mode):return AddOutputMode(display=self.display,opcode=self.display.get_extension_major(extname),output=output,mode=mode)
class DeleteOutputMode(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(19),rq.RequestLength(),rq.Card32(_E),rq.Card32(_I))
def delete_output_mode(self):return DeleteOutputMode(display=self.display,opcode=self.display.get_extension_major(extname),output=output,mode=mode)
class GetCrtcInfo(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(20),rq.RequestLength(),rq.Card32(_F),rq.Card32(_H));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_G),rq.Card16(_B),rq.ReplyLength(),rq.Card32(_D),rq.Int16('x'),rq.Int16('y'),rq.Card16(_P),rq.Card16(_Q),rq.Card32(_I),rq.Card16(_J),rq.Card16('possible_rotations'),rq.LengthOf(_K,2),rq.LengthOf(_A6,2),rq.List(_K,rq.Card32Obj),rq.List(_A6,rq.Card32Obj))
def get_crtc_info(self,crtc,config_timestamp):return GetCrtcInfo(display=self.display,opcode=self.display.get_extension_major(extname),crtc=crtc,config_timestamp=config_timestamp)
class SetCrtcConfig(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(21),rq.RequestLength(),rq.Card32(_F),rq.Card32(_D),rq.Card32(_H),rq.Int16('x'),rq.Int16('y'),rq.Card32(_I),rq.Card16(_J),rq.Pad(2),rq.List(_K,rq.Card32Obj));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_G),rq.Card16(_B),rq.ReplyLength(),rq.Card32(_T),rq.Pad(20))
def set_crtc_config(self,crtc,config_timestamp,x,y,mode,rotation,outputs,timestamp=X.CurrentTime):return SetCrtcConfig(display=self.display,opcode=self.display.get_extension_major(extname),crtc=crtc,config_timestamp=config_timestamp,x=x,y=y,mode=mode,rotation=rotation,outputs=outputs,timestamp=timestamp)
class GetCrtcGammaSize(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(22),rq.RequestLength(),rq.Card32(_F));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_G),rq.Card16(_B),rq.ReplyLength(),rq.Card16('size'),rq.Pad(22))
def get_crtc_gamma_size(self,crtc):return GetCrtcGammaSize(display=self.display,opcode=self.display.get_extension_major(extname),crtc=crtc)
class GetCrtcGamma(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(23),rq.RequestLength(),rq.Card32(_F));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_G),rq.Card16(_B),rq.ReplyLength(),rq.LengthOf((_X,_Z,_Y),2),rq.Pad(22),rq.List(_X,rq.Card16Obj),rq.List(_Z,rq.Card16Obj),rq.List(_Y,rq.Card16Obj))
def get_crtc_gamma(self,crtc):return GetCrtcGamma(display=self.display,opcode=self.display.get_extension_major(extname),crtc=crtc)
class SetCrtcGamma(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(24),rq.RequestLength(),rq.Card32(_F),rq.Card16('size'),rq.Pad(2),rq.List(_X,rq.Card16Obj),rq.List(_Z,rq.Card16Obj),rq.List(_Y,rq.Card16Obj))
def set_crtc_gamma(self,crtc,size,red,green,blue):return SetCrtcGamma(display=self.display,opcode=self.display.get_extension_major(extname),crtc=crtc,size=size,red=red,green=green,blue=blue)
class GetScreenResourcesCurrent(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(25),rq.RequestLength(),rq.Window(_C));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_B),rq.ReplyLength(),rq.Card32(_D),rq.Card32(_H),rq.LengthOf(_O,2),rq.LengthOf(_K,2),rq.LengthOf(_M,2),rq.LengthOf(_k,2),rq.Pad(8),rq.List(_O,rq.Card32Obj),rq.List(_K,rq.Card32Obj),rq.List(_M,RandR_ModeInfo),rq.String8(_k))
def get_screen_resources_current(self):A=self;return GetScreenResourcesCurrent(display=A.display,opcode=A.display.get_extension_major(extname),window=A)
class SetCrtcTransform(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(26),rq.RequestLength(),rq.Card32(_F),rq.Object('transform',Render_Transform),rq.LengthOf(_p,2),rq.Pad(2),rq.String8(_p),rq.List('filter_params',rq.Card32Obj))
def set_crtc_transform(self,crtc,n_bytes_filter):return SetCrtcTransform(display=self.display,opcode=self.display.get_extension_major(extname),crtc=crtc,n_bytes_filter=n_bytes_filter)
class GetCrtcTransform(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(27),rq.RequestLength(),rq.Card32(_F));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_G),rq.Card16(_B),rq.ReplyLength(),rq.Object('pending_transform',Render_Transform),rq.Bool('has_transforms'),rq.Pad(3),rq.Object('current_transform',Render_Transform),rq.Pad(4),rq.LengthOf(_l,2),rq.LengthOf(_g,2),rq.LengthOf(_r,2),rq.LengthOf(_z,2),rq.String8(_l),rq.List(_g,rq.Card32Obj),rq.String8(_r),rq.List(_z,rq.Card32Obj))
def get_crtc_transform(self,crtc):return GetCrtcTransform(display=self.display,opcode=self.display.get_extension_major(extname),crtc=crtc)
class GetPanning(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(28),rq.RequestLength(),rq.Card32(_F));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_G),rq.Card16(_B),rq.ReplyLength(),rq.Card32(_D),rq.Card16(_s),rq.Card16(_t),rq.Card16(_P),rq.Card16(_Q),rq.Card16(_A5),rq.Card16(_A2),rq.Card16(_o),rq.Card16(_A4),rq.Int16(_x),rq.Int16(_A3),rq.Int16(_A0),rq.Int16(_A7))
def get_panning(self,crtc):return GetPanning(display=self.display,opcode=self.display.get_extension_major(extname),crtc=crtc)
class SetPanning(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(29),rq.RequestLength(),rq.Card32(_F),rq.Card32(_D),rq.Card16(_s),rq.Card16(_t),rq.Card16(_P),rq.Card16(_Q),rq.Card16(_A5),rq.Card16(_A2),rq.Card16(_o),rq.Card16(_A4),rq.Int16(_x),rq.Int16(_A3),rq.Int16(_A0),rq.Int16(_A7));_reply=rq.Struct(rq.ReplyCode(),rq.Card8(_G),rq.Card16(_B),rq.ReplyLength(),rq.Card32(_T),rq.Pad(20))
def set_panning(self,crtc,left,top,width,height,track_left,track_top,track_width,track_height,border_left,border_top,border_width,border_height,timestamp=X.CurrentTime):return SetPanning(display=self.display,opcode=self.display.get_extension_major(extname),crtc=crtc,left=left,top=top,width=width,height=height,track_left=track_left,track_top=track_top,track_width=track_width,track_height=track_height,border_left=border_left,border_top=border_top,border_width=border_width,border_height=border_height,timestamp=timestamp)
class SetOutputPrimary(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(30),rq.RequestLength(),rq.Window(_C),rq.Card32(_E))
def set_output_primary(self,output):A=self;return SetOutputPrimary(display=A.display,opcode=A.display.get_extension_major(extname),window=A,output=output)
class GetOutputPrimary(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(31),rq.RequestLength(),rq.Window(_C));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_B),rq.ReplyLength(),rq.Card32(_E),rq.Pad(20))
def get_output_primary(self):A=self;return GetOutputPrimary(display=A.display,opcode=A.display.get_extension_major(extname),window=A)
class ScreenChangeNotify(rq.Event):_code=None;_fields=rq.Struct(rq.Card8(_N),rq.Card8(_J),rq.Card16(_B),rq.Card32(_D),rq.Card32(_H),rq.Window(_W),rq.Window(_C),rq.Card16(_V),rq.Card16(_R),rq.Card16(_A1),rq.Card16(_A9),rq.Card16(_d),rq.Card16(_a))
class CrtcChangeNotify(rq.Event):_code=None;_fields=rq.Struct(rq.Card8(_N),rq.Card8(_c),rq.Card16(_B),rq.Card32(_D),rq.Window(_C),rq.Card32(_F),rq.Card32(_I),rq.Card16(_J),rq.Pad(2),rq.Int16('x'),rq.Int16('y'),rq.Card16(_P),rq.Card16(_Q))
class OutputChangeNotify(rq.Event):_code=None;_fields=rq.Struct(rq.Card8(_N),rq.Card8(_c),rq.Card16(_B),rq.Card32(_D),rq.Card32(_H),rq.Window(_C),rq.Card32(_E),rq.Card32(_F),rq.Card32(_I),rq.Card16(_J),rq.Card8(_m),rq.Card8(_R))
class OutputPropertyNotify(rq.Event):_code=None;_fields=rq.Struct(rq.Card8(_N),rq.Card8(_c),rq.Card16(_B),rq.Window(_C),rq.Card32(_E),rq.Card32('atom'),rq.Card32(_D),rq.Card8('state'),rq.Pad(11))
def init(disp,info):C=info;B='display';A=disp;A.extension_add_method(B,'xrandr_query_version',query_version);A.extension_add_method(_C,'xrandr_select_input',select_input);A.extension_add_method(_C,'xrandr_get_screen_info',get_screen_info);A.extension_add_method(_U,'xrandr_1_0set_screen_config',_1_0set_screen_config);A.extension_add_method(_U,'xrandr_set_screen_config',set_screen_config);A.extension_add_method(_C,'xrandr_get_screen_size_range',get_screen_size_range);A.extension_add_method(_C,'xrandr_set_screen_size',set_screen_size);A.extension_add_method(_C,'xrandr_get_screen_resources',get_screen_resources);A.extension_add_method(B,'xrandr_get_output_info',get_output_info);A.extension_add_method(B,'xrandr_list_output_properties',list_output_properties);A.extension_add_method(B,'xrandr_query_output_property',query_output_property);A.extension_add_method(B,'xrandr_configure_output_property ',configure_output_property);A.extension_add_method(B,'xrandr_change_output_property',change_output_property);A.extension_add_method(B,'xrandr_delete_output_property',delete_output_property);A.extension_add_method(B,'xrandr_get_output_property',get_output_property);A.extension_add_method(_C,'xrandr_create_mode',create_mode);A.extension_add_method(B,'xrandr_destroy_mode',destroy_mode);A.extension_add_method(B,'xrandr_add_output_mode',add_output_mode);A.extension_add_method(B,'xrandr_delete_output_mode',delete_output_mode);A.extension_add_method(B,'xrandr_get_crtc_info',get_crtc_info);A.extension_add_method(B,'xrandr_set_crtc_config',set_crtc_config);A.extension_add_method(B,'xrandr_get_crtc_gamma_size',get_crtc_gamma_size);A.extension_add_method(B,'xrandr_get_crtc_gamma',get_crtc_gamma);A.extension_add_method(B,'xrandr_set_crtc_gamma',set_crtc_gamma);A.extension_add_method(_C,'xrandr_get_screen_resources_current',get_screen_resources_current);A.extension_add_method(B,'xrandr_set_crtc_transform',set_crtc_transform);A.extension_add_method(B,'xrandr_get_crtc_transform',get_crtc_transform);A.extension_add_method(_C,'xrandr_set_output_primary',set_output_primary);A.extension_add_method(_C,'xrandr_get_output_primary',get_output_primary);A.extension_add_method(B,'xrandr_get_panning',get_panning);A.extension_add_method(B,'xrandr_set_panning',set_panning);A.extension_add_event(C.first_event+RRScreenChangeNotify,ScreenChangeNotify);A.extension_add_subevent(C.first_event+RRNotify,RRNotify_CrtcChange,CrtcChangeNotify);A.extension_add_subevent(C.first_event+RRNotify,RRNotify_OutputChange,OutputChangeNotify);A.extension_add_subevent(C.first_event+RRNotify,RRNotify_OutputProperty,OutputPropertyNotify)