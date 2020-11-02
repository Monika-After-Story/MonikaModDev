'\nThis extension provides X Protocol control over the VESA Display\nPower Management Signaling (DPMS) characteristics of video boards\nunder control of the X Window System.\n\nDocumentation: https://www.x.org/releases/X11R7.7/doc/xextproto/dpms.html\n'
_H='suspend_timeout'
_G='major_version'
_F='power_level'
_E='off_timeout'
_D='standby_timeout'
_C='minor_version'
_B='sequence_number'
_A='opcode'
from Xlib import X
from Xlib.protocol import rq
extname='DPMS'
DPMSModeOn=0
DPMSModeStandby=1
DPMSModeSuspend=2
DPMSModeOff=3
DPMSPowerLevel=DPMSModeOn,DPMSModeStandby,DPMSModeSuspend,DPMSModeOff
class DPMSGetVersion(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(0),rq.RequestLength(),rq.Card16(_G),rq.Card16(_C));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_B),rq.ReplyLength(),rq.Card16(_G),rq.Card16(_C),rq.Pad(20))
def get_version(self):return DPMSGetVersion(display=self.display,opcode=self.display.get_extension_major(extname),major_version=1,minor_version=1)
class DPMSCapable(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(1),rq.RequestLength());_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_B),rq.ReplyLength(),rq.Bool('capable'),rq.Pad(23))
def capable(self):return DPMSCapable(display=self.display,opcode=self.display.get_extension_major(extname),major_version=1,minor_version=1)
class DPMSGetTimeouts(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(2),rq.RequestLength());_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_B),rq.ReplyLength(),rq.Card16(_D),rq.Card16(_H),rq.Card16(_E),rq.Pad(18))
def get_timeouts(self):return DPMSGetTimeouts(display=self.display,opcode=self.display.get_extension_major(extname),major_version=1,minor_version=1)
class DPMSSetTimeouts(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(3),rq.RequestLength(),rq.Card16(_D),rq.Card16(_H),rq.Card16(_E),rq.Pad(2))
def set_timeouts(self,standby_timeout,suspend_timeout,off_timeout):return DPMSSetTimeouts(display=self.display,opcode=self.display.get_extension_major(extname),major_version=1,minor_version=1,standby_timeout=standby_timeout,suspend_timeout=suspend_timeout,off_timeout=off_timeout)
class DPMSEnable(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(4),rq.RequestLength())
def enable(self):return DPMSEnable(display=self.display,opcode=self.display.get_extension_major(extname),major_version=1,minor_version=1)
class DPMSDisable(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(5),rq.RequestLength())
def disable(self):return DPMSDisable(display=self.display,opcode=self.display.get_extension_major(extname),major_version=1,minor_version=1)
class DPMSForceLevel(rq.Request):_request=rq.Struct(rq.Card8(_A),rq.Opcode(6),rq.RequestLength(),rq.Resource(_F,DPMSPowerLevel))
def force_level(self,power_level):return DPMSForceLevel(display=self.display,opcode=self.display.get_extension_major(extname),major_version=1,minor_version=1,power_level=power_level)
class DPMSInfo(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_A),rq.Opcode(7),rq.RequestLength());_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_B),rq.ReplyLength(),rq.Card16(_F),rq.Bool('state'),rq.Pad(21))
def info(self):return DPMSInfo(display=self.display,opcode=self.display.get_extension_major(extname),major_version=1,minor_version=1)
def init(disp,_info):B='display';A=disp;A.extension_add_method(B,'dpms_get_version',get_version);A.extension_add_method(B,'dpms_capable',capable);A.extension_add_method(B,'dpms_get_timeouts',get_timeouts);A.extension_add_method(B,'dpms_set_timeouts',set_timeouts);A.extension_add_method(B,'dpms_enable',enable);A.extension_add_method(B,'dpms_disable',disable);A.extension_add_method(B,'dpms_force_level',force_level);A.extension_add_method(B,'dpms_info',info)