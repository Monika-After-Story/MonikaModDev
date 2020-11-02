"Xinerama - provide access to the Xinerama extension information.\n\nThere are at least there different - and mutually incomparable -\nXinerama extensions available. This uses the one bundled with XFree86\n4.6 and/or Xorg 6.9 in the ati/radeon driver. It uses the include\nfiles from that X distribution, so should work with it as well.  I\nprovide code for the lone Sun 1.0 request that isn't part of 1.1, but\nthis is untested because I don't have a server that implements it.\n\nThe functions loosely follow the libXineram functions. Mostly, they\nreturn an rq.Struct in lieu of passing in pointers that get data from\nthe rq.Struct crammed into them. The exception is isActive, which\nreturns the state information - because that's what libXinerama does."
_G='state'
_F='minor_version'
_E='major_version'
_D='screen'
_C='sequence_number'
_B='opcode'
_A='window'
from Xlib import X
from Xlib.protocol import rq,structs
extname='XINERAMA'
class QueryVersion(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_B),rq.Opcode(0),rq.RequestLength(),rq.Card8(_E),rq.Card8(_F),rq.Pad(2));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_C),rq.ReplyLength(),rq.Card16(_E),rq.Card16(_F),rq.Pad(20))
def query_version(self):return QueryVersion(display=self.display,opcode=self.display.get_extension_major(extname),major_version=1,minor_version=1)
class GetState(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_B),rq.Opcode(1),rq.RequestLength(),rq.Window(_A));_reply=rq.Struct(rq.ReplyCode(),rq.Bool(_G),rq.Card16(_C),rq.ReplyLength(),rq.Window(_A),rq.Pad(20))
def get_state(self):A=self;return GetState(display=A.display,opcode=A.display.get_extension_major(extname),window=A.id)
class GetScreenCount(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_B),rq.Opcode(2),rq.RequestLength(),rq.Window(_A));_reply=rq.Struct(rq.ReplyCode(),rq.Card8('screen_count'),rq.Card16(_C),rq.ReplyLength(),rq.Window(_A),rq.Pad(20))
def get_screen_count(self):A=self;return GetScreenCount(display=A.display,opcode=A.display.get_extension_major(extname),window=A.id)
class GetScreenSize(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_B),rq.Opcode(3),rq.RequestLength(),rq.Window(_A),rq.Card32(_D));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_C),rq.Card32('length'),rq.Card32('width'),rq.Card32('height'),rq.Window(_A),rq.Card32(_D),rq.Pad(8))
def get_screen_size(self,screen_no):'Returns the size of the given screen number';A=self;return GetScreenSize(display=A.display,opcode=A.display.get_extension_major(extname),window=A.id,screen=screen_no)
class IsActive(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_B),rq.Opcode(4),rq.RequestLength());_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_C),rq.ReplyLength(),rq.Card32(_G),rq.Pad(20))
def is_active(self):A=IsActive(display=self.display,opcode=self.display.get_extension_major(extname));return A.state
class QueryScreens(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_B),rq.Opcode(5),rq.RequestLength());_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_C),rq.ReplyLength(),rq.Card32('number'),rq.Pad(20),rq.List('screens',structs.Rectangle))
def query_screens(self):return QueryScreens(display=self.display,opcode=self.display.get_extension_major(extname))
class GetInfo(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_B),rq.Opcode(4),rq.RequestLength(),rq.Card32('visual'));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_C),rq.ReplyLength(),rq.Window(_A))
def get_info(self,visual):A=GetInfo(display=self.display,opcode=self.display.get_extension_major(extname),visual=visual)
def init(disp,info):B='display';A=disp;A.extension_add_method(B,'xinerama_query_version',query_version);A.extension_add_method(_A,'xinerama_get_state',get_state);A.extension_add_method(_A,'xinerama_get_screen_count',get_screen_count);A.extension_add_method(_A,'xinerama_get_screen_size',get_screen_size);A.extension_add_method(B,'xinerama_is_active',is_active);A.extension_add_method(B,'xinerama_query_screens',query_screens);A.extension_add_method(B,'xinerama_get_info',get_info)