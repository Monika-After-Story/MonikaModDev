'\nA partial implementation of the XFIXES extension.  Only the HideCursor and\nShowCursor requests and SelectionNotify events are provided.\n'
_F='major_version'
_E='sequence_number'
_D='selection'
_C='minor_version'
_B='opcode'
_A='window'
from Xlib.protocol import rq
extname='XFIXES'
XFixesSelectionNotify=0
XFixesSetSelectionOwnerNotifyMask=1<<0
XFixesSelectionWindowDestroyNotifyMask=1<<1
XFixesSelectionClientCloseNotifyMask=1<<2
XFixesSetSelectionOwnerNotify=0
XFixesSelectionWindowDestroyNotify=1
XFixesSelectionClientCloseNotify=2
class QueryVersion(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_B),rq.Opcode(0),rq.RequestLength(),rq.Card32(_F),rq.Card32(_C));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_E),rq.ReplyLength(),rq.Card32(_F),rq.Card32(_C),rq.Pad(16))
def query_version(self):return QueryVersion(display=self.display,opcode=self.display.get_extension_major(extname),major_version=4,minor_version=0)
class HideCursor(rq.Request):_request=rq.Struct(rq.Card8(_B),rq.Opcode(29),rq.RequestLength(),rq.Window(_A))
def hide_cursor(self):A=self;HideCursor(display=A.display,opcode=A.display.get_extension_major(extname),window=A)
class ShowCursor(rq.Request):_request=rq.Struct(rq.Card8(_B),rq.Opcode(30),rq.RequestLength(),rq.Window(_A))
def show_cursor(self):A=self;ShowCursor(display=A.display,opcode=A.display.get_extension_major(extname),window=A)
class SelectSelectionInput(rq.Request):_request=rq.Struct(rq.Card8(_B),rq.Opcode(2),rq.RequestLength(),rq.Window(_A),rq.Card32(_D),rq.Card32('mask'))
def select_selection_input(self,window,selection,mask):return SelectSelectionInput(opcode=self.display.get_extension_major(extname),display=self.display,window=window,selection=selection,mask=mask)
class SelectionNotify(rq.Event):_code=None;_fields=rq.Struct(rq.Card8('type'),rq.Card8('sub_code'),rq.Card16(_E),rq.Window(_A),rq.Window('owner'),rq.Card32(_D),rq.Card32('timestamp'),rq.Card32('selection_timestamp'),rq.Pad(8))
class SetSelectionOwnerNotify(SelectionNotify):0
class SelectionWindowDestroyNotify(SelectionNotify):0
class SelectionClientCloseNotify(SelectionNotify):0
def init(disp,info):C='display';B=info;A=disp;A.extension_add_method(C,'xfixes_select_selection_input',select_selection_input);A.extension_add_method(C,'xfixes_query_version',query_version);A.extension_add_method(_A,'xfixes_hide_cursor',hide_cursor);A.extension_add_method(_A,'xfixes_show_cursor',show_cursor);A.extension_add_subevent(B.first_event+XFixesSelectionNotify,XFixesSetSelectionOwnerNotify,SetSelectionOwnerNotify);A.extension_add_subevent(B.first_event+XFixesSelectionNotify,XFixesSelectionWindowDestroyNotify,SelectionWindowDestroyNotify);A.extension_add_subevent(B.first_event+XFixesSelectionNotify,XFixesSelectionClientCloseNotify,SelectionClientCloseNotify)