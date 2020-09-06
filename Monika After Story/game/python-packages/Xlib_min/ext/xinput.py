'\nA very incomplete implementation of the XInput extension.\n'
_g='labels'
_f='paired_device_mode'
_e='owner_events'
_d='grab_mode'
_c='buttons'
_b='minor_version'
_a='mode'
_Z='keycodes'
_Y='devices'
_X='masks'
_W='number'
_V='major_version'
_U='enabled'
_T='attachment'
_S='cursor'
_R='name'
_Q='state'
_P='grab_type'
_O='info'
_N='detail'
_M='grab_window'
_L='classes'
_K='sequence_number'
_J='flags'
_I='window'
_H='modifiers'
_G='length'
_F='mask'
_E='time'
_D='type'
_C='opcode'
_B='sourceid'
_A='deviceid'
import sys,array,struct
from six import integer_types
from Xlib.protocol import rq
from Xlib import X
extname='XInputExtension'
PropertyDeleted=0
PropertyCreated=1
PropertyModified=2
NotifyNormal=0
NotifyGrab=1
NotifyUngrab=2
NotifyWhileGrabbed=3
NotifyPassiveGrab=4
NotifyPassiveUngrab=5
NotifyAncestor=0
NotifyVirtual=1
NotifyInferior=2
NotifyNonlinear=3
NotifyNonlinearVirtual=4
NotifyPointer=5
NotifyPointerRoot=6
NotifyDetailNone=7
GrabtypeButton=0
GrabtypeKeycode=1
GrabtypeEnter=2
GrabtypeFocusIn=3
GrabtypeTouchBegin=4
AnyModifier=1<<31
AnyButton=0
AnyKeycode=0
AsyncDevice=0
SyncDevice=1
ReplayDevice=2
AsyncPairedDevice=3
AsyncPair=4
SyncPair=5
SlaveSwitch=1
DeviceChange=2
MasterAdded=1<<0
MasterRemoved=1<<1
SlaveAdded=1<<2
SlaveRemoved=1<<3
SlaveAttached=1<<4
SlaveDetached=1<<5
DeviceEnabled=1<<6
DeviceDisabled=1<<7
AddMaster=1
RemoveMaster=2
AttachSlave=3
DetachSlave=4
AttachToMaster=1
Floating=2
ModeRelative=0
ModeAbsolute=1
MasterPointer=1
MasterKeyboard=2
SlavePointer=3
SlaveKeyboard=4
FloatingSlave=5
KeyClass=0
ButtonClass=1
ValuatorClass=2
ScrollClass=3
TouchClass=8
KeyRepeat=1<<16
AllDevices=0
AllMasterDevices=1
DeviceChanged=1
KeyPress=2
KeyRelease=3
ButtonPress=4
ButtonRelease=5
Motion=6
Enter=7
Leave=8
FocusIn=9
FocusOut=10
HierarchyChanged=11
PropertyEvent=12
RawKeyPress=13
RawKeyRelease=14
RawButtonPress=15
RawButtonRelease=16
RawMotion=17
DeviceChangedMask=1<<DeviceChanged
KeyPressMask=1<<KeyPress
KeyReleaseMask=1<<KeyRelease
ButtonPressMask=1<<ButtonPress
ButtonReleaseMask=1<<ButtonRelease
MotionMask=1<<Motion
EnterMask=1<<Enter
LeaveMask=1<<Leave
FocusInMask=1<<FocusIn
FocusOutMask=1<<FocusOut
HierarchyChangedMask=1<<HierarchyChanged
PropertyEventMask=1<<PropertyEvent
RawKeyPressMask=1<<RawKeyPress
RawKeyReleaseMask=1<<RawKeyRelease
RawButtonPressMask=1<<RawButtonPress
RawButtonReleaseMask=1<<RawButtonRelease
RawMotionMask=1<<RawMotion
GrabModeSync=0
GrabModeAsync=1
GrabModeTouch=2
DEVICEID=rq.Card16
DEVICE=rq.Card16
DEVICEUSE=rq.Card8
class FP1616(rq.Int32):
	def check_value(A,value):return int(value*65536.0)
	def parse_value(A,value,display):return float(value)/float(1<<16)
class FP3232(rq.ValueField):
	structcode='lL';structvalues=2
	def check_value(A,value):return value
	def parse_value(D,value,display):B,C=value;A=float(B);A+=float(C)*(1.0/(1<<32));return A
class XIQueryVersion(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_C),rq.Opcode(47),rq.RequestLength(),rq.Card16(_V),rq.Card16(_b));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_K),rq.ReplyLength(),rq.Card16(_V),rq.Card16(_b),rq.Pad(20))
def query_version(self):return XIQueryVersion(display=self.display,opcode=self.display.get_extension_major(extname),major_version=2,minor_version=0)
class Mask(rq.List):
	def __init__(A,name):rq.List.__init__(A,name,rq.Card32,pad=0)
	def pack_value(D,val):
		A=val;B=array.array(rq.struct_to_array_codes['L'])
		if isinstance(A,integer_types):
			if sys.byteorder=='little':
				def C(val):B.insert(0,val)
			elif sys.byteorder=='big':C=B.append
			else:raise AssertionError(sys.byteorder)
			while A:C(A&4294967295);A=A>>32
		else:B.extend(A)
		return B.tostring(),len(B),None
EventMask=rq.Struct(DEVICE(_A),rq.LengthOf(_F,2),Mask(_F))
class XISelectEvents(rq.Request):_request=rq.Struct(rq.Card8(_C),rq.Opcode(46),rq.RequestLength(),rq.Window(_I),rq.LengthOf(_X,2),rq.Pad(2),rq.List(_X,EventMask))
def select_events(self,event_masks):'\n    select_events(event_masks)\n\n    event_masks:\n      Sequence of (deviceid, mask) pairs, where deviceid is a numerical device\n      ID, or AllDevices or AllMasterDevices, and mask is either an unsigned\n      integer or sequence of 32 bits unsigned values\n    ';A=self;return XISelectEvents(display=A.display,opcode=A.display.get_extension_major(extname),window=A,masks=event_masks)
AnyInfo=rq.Struct(rq.Card16(_D),rq.Card16(_G),rq.Card16(_B),rq.Pad(2))
class ButtonMask(object):
	def __init__(A,value,length):A._value=value;A._length=length
	def __len__(A):return A._length
	def __getitem__(A,key):return A._value&1<<key
	def __str__(A):return repr(A)
	def __repr__(A):return '0b{value:0{width}b}'.format(value=A._value,width=A._length)
class ButtonState(rq.ValueField):
	structcode=None
	def __init__(A,name):rq.ValueField.__init__(A,name)
	def parse_binary_value(G,data,display,length,fmt):
		D=length;A=data;C=4*((D+7>>3)+3>>2);E=A[:C];B=0
		for F in reversed(struct.unpack('={0:d}B'.format(C),E)):B<<=8;B|=F
		A=A[C:];assert B&1==0;return ButtonMask(B>>1,D),A
ButtonInfo=rq.Struct(rq.Card16(_D),rq.Card16(_G),rq.Card16(_B),rq.LengthOf((_Q,_g),2),ButtonState(_Q),rq.List(_g,rq.Card32))
KeyInfo=rq.Struct(rq.Card16(_D),rq.Card16(_G),rq.Card16(_B),rq.LengthOf(_Z,2),rq.List(_Z,rq.Card32))
ValuatorInfo=rq.Struct(rq.Card16(_D),rq.Card16(_G),rq.Card16(_B),rq.Card16(_W),rq.Card32('label'),FP3232('min'),FP3232('max'),FP3232('value'),rq.Card32('resolution'),rq.Card8(_a),rq.Pad(3))
ScrollInfo=rq.Struct(rq.Card16(_D),rq.Card16(_G),rq.Card16(_B),rq.Card16(_W),rq.Card16('scroll_type'),rq.Pad(2),rq.Card32(_J),FP3232('increment'))
TouchInfo=rq.Struct(rq.Card16(_D),rq.Card16(_G),rq.Card16(_B),rq.Card8(_a),rq.Card8('num_touches'))
INFO_CLASSES={KeyClass:KeyInfo,ButtonClass:ButtonInfo,ValuatorClass:ValuatorInfo,ScrollClass:ScrollInfo,TouchClass:TouchInfo}
class ClassInfoClass(object):
	structcode=None
	def parse_binary(F,data,display):A=data;B,C=struct.unpack('=HH',A[:4]);D=INFO_CLASSES.get(B,AnyInfo);E,G=D.parse_binary(A,display);A=A[C*4:];return E,A
ClassInfo=ClassInfoClass()
DeviceInfo=rq.Struct(DEVICEID(_A),rq.Card16('use'),rq.Card16(_T),rq.LengthOf(_L,2),rq.LengthOf(_R,2),rq.Bool(_U),rq.Pad(1),rq.String8(_R,4),rq.List(_L,ClassInfo))
class XIQueryDevice(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_C),rq.Opcode(48),rq.RequestLength(),DEVICEID(_A),rq.Pad(2));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_K),rq.ReplyLength(),rq.LengthOf(_Y,2),rq.Pad(22),rq.List(_Y,DeviceInfo))
def query_device(self,deviceid):return XIQueryDevice(display=self.display,opcode=self.display.get_extension_major(extname),deviceid=deviceid)
class XIGrabDevice(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_C),rq.Opcode(51),rq.RequestLength(),rq.Window(_M),rq.Card32(_E),rq.Cursor(_S,(X.NONE,)),DEVICEID(_A),rq.Set(_d,1,(GrabModeSync,GrabModeAsync)),rq.Set(_f,1,(GrabModeSync,GrabModeAsync)),rq.Bool(_e),rq.Pad(1),rq.LengthOf(_F,2),Mask(_F));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_K),rq.ReplyLength(),rq.Card8('status'),rq.Pad(23))
def grab_device(self,deviceid,time,grab_mode,paired_device_mode,owner_events,event_mask):A=self;return XIGrabDevice(display=A.display,opcode=A.display.get_extension_major(extname),deviceid=deviceid,grab_window=A,time=time,cursor=X.NONE,grab_mode=grab_mode,paired_device_mode=paired_device_mode,owner_events=owner_events,mask=event_mask)
class XIUngrabDevice(rq.Request):_request=rq.Struct(rq.Card8(_C),rq.Opcode(52),rq.RequestLength(),rq.Card32(_E),DEVICEID(_A),rq.Pad(2))
def ungrab_device(self,deviceid,time):return XIUngrabDevice(display=self.display,opcode=self.display.get_extension_major(extname),time=time,deviceid=deviceid)
class XIPassiveGrabDevice(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_C),rq.Opcode(54),rq.RequestLength(),rq.Card32(_E),rq.Window(_M),rq.Cursor(_S,(X.NONE,)),rq.Card32(_N),DEVICEID(_A),rq.LengthOf(_H,2),rq.LengthOf(_F,2),rq.Set(_P,1,(GrabtypeButton,GrabtypeKeycode,GrabtypeEnter,GrabtypeFocusIn,GrabtypeTouchBegin)),rq.Set(_d,1,(GrabModeSync,GrabModeAsync)),rq.Set(_f,1,(GrabModeSync,GrabModeAsync)),rq.Bool(_e),rq.Pad(2),Mask(_F),rq.List(_H,rq.Card32));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_K),rq.ReplyLength(),rq.LengthOf(_H,2),rq.Pad(22),rq.List(_H,rq.Card32))
def passive_grab_device(self,deviceid,time,detail,grab_type,grab_mode,paired_device_mode,owner_events,event_mask,modifiers):A=self;return XIPassiveGrabDevice(display=A.display,opcode=A.display.get_extension_major(extname),deviceid=deviceid,grab_window=A,time=time,cursor=X.NONE,detail=detail,grab_type=grab_type,grab_mode=grab_mode,paired_device_mode=paired_device_mode,owner_events=owner_events,mask=event_mask,modifiers=modifiers)
def grab_keycode(self,deviceid,time,keycode,grab_mode,paired_device_mode,owner_events,event_mask,modifiers):return passive_grab_device(self,deviceid,time,keycode,GrabtypeKeycode,grab_mode,paired_device_mode,owner_events,event_mask,modifiers)
class XIPassiveUngrabDevice(rq.Request):_request=rq.Struct(rq.Card8(_C),rq.Opcode(55),rq.RequestLength(),rq.Window(_M),rq.Card32(_N),DEVICEID(_A),rq.LengthOf(_H,2),rq.Set(_P,1,(GrabtypeButton,GrabtypeKeycode,GrabtypeEnter,GrabtypeFocusIn,GrabtypeTouchBegin)),rq.Pad(3),rq.List(_H,rq.Card32))
def passive_ungrab_device(self,deviceid,detail,grab_type,modifiers):A=self;return XIPassiveUngrabDevice(display=A.display,opcode=A.display.get_extension_major(extname),deviceid=deviceid,grab_window=A,detail=detail,grab_type=grab_type,modifiers=modifiers)
def ungrab_keycode(self,deviceid,keycode,modifiers):return passive_ungrab_device(self,deviceid,keycode,GrabtypeKeycode,modifiers)
HierarchyInfo=rq.Struct(DEVICEID(_A),DEVICEID(_T),DEVICEUSE(_D),rq.Bool(_U),rq.Pad(2),rq.Card32(_J))
HierarchyEventData=rq.Struct(DEVICEID(_A),rq.Card32(_E),rq.Card32(_J),rq.LengthOf(_O,2),rq.Pad(10),rq.List(_O,HierarchyInfo))
ModifierInfo=rq.Struct(rq.Card32('base_mods'),rq.Card32('latched_mods'),rq.Card32('locked_mods'),rq.Card32('effective_mods'))
GroupInfo=rq.Struct(rq.Card8('base_group'),rq.Card8('latched_group'),rq.Card8('locked_group'),rq.Card8('effective_group'))
DeviceEventData=rq.Struct(DEVICEID(_A),rq.Card32(_E),rq.Card32(_N),rq.Window('root'),rq.Window('event'),rq.Window('child'),FP1616('root_x'),FP1616('root_y'),FP1616('event_x'),FP1616('event_y'),rq.LengthOf(_c,2),rq.Card16('valulators_len'),DEVICEID(_B),rq.Pad(2),rq.Card32(_J),rq.Object('mods',ModifierInfo),rq.Object('groups',GroupInfo),ButtonState(_c))
DeviceChangedEventData=rq.Struct(DEVICEID(_A),rq.Card32(_E),rq.LengthOf(_L,2),DEVICEID(_B),rq.Card8('reason'),rq.Pad(11),rq.List(_L,ClassInfo))
def init(disp,info):
	C='display';B=info;A=disp;A.extension_add_method(C,'xinput_query_version',query_version);A.extension_add_method(_I,'xinput_select_events',select_events);A.extension_add_method(C,'xinput_query_device',query_device);A.extension_add_method(_I,'xinput_grab_device',grab_device);A.extension_add_method(C,'xinput_ungrab_device',ungrab_device);A.extension_add_method(_I,'xinput_grab_keycode',grab_keycode);A.extension_add_method(_I,'xinput_ungrab_keycode',ungrab_keycode)
	if hasattr(A,'ge_add_event_data'):
		for D in (ButtonPress,ButtonRelease,KeyPress,KeyRelease,Motion):A.ge_add_event_data(B.major_opcode,D,DeviceEventData)
		A.ge_add_event_data(B.major_opcode,DeviceChanged,DeviceEventData);A.ge_add_event_data(B.major_opcode,HierarchyChanged,HierarchyEventData)