'Composite extension, allowing windows to be rendered to off-screen\nstorage.\n\nFor detailed description, see the protocol specification at\nhttp://freedesktop.org/wiki/Software/CompositeExt\n\nBy itself this extension is not very useful, it is intended to be used\ntogether with the DAMAGE and XFIXES extensions.  Typically you would\nalso need RENDER or glX or some similar method of creating fancy\ngraphics.\n'
_G='major_version'
_F='pixmap'
_E='sequence_number'
_D='minor_version'
_C='update'
_B='opcode'
_A='window'
from Xlib import X
from Xlib.protocol import rq
from Xlib.xobject import drawable
extname='Composite'
RedirectAutomatic=0
RedirectManual=1
class QueryVersion(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_B),rq.Opcode(0),rq.RequestLength(),rq.Card32(_G),rq.Card32(_D));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_E),rq.ReplyLength(),rq.Card32(_G),rq.Card32(_D),rq.Pad(16))
def query_version(self):return QueryVersion(display=self.display,opcode=self.display.get_extension_major(extname),major_version=0,minor_version=4)
class RedirectWindow(rq.Request):_request=rq.Struct(rq.Card8(_B),rq.Opcode(1),rq.RequestLength(),rq.Window(_A),rq.Set(_C,1,(RedirectAutomatic,RedirectManual)),rq.Pad(3))
def redirect_window(self,update,onerror=None):'Redirect the hierarchy starting at this window to off-screen\n    storage.\n    ';A=self;RedirectWindow(display=A.display,onerror=onerror,opcode=A.display.get_extension_major(extname),window=A,update=update)
class RedirectSubwindows(rq.Request):_request=rq.Struct(rq.Card8(_B),rq.Opcode(2),rq.RequestLength(),rq.Window(_A),rq.Set(_C,1,(RedirectAutomatic,RedirectManual)),rq.Pad(3))
def redirect_subwindows(self,update,onerror=None):'Redirect the hierarchies starting at all current and future\n    children to this window to off-screen storage.\n    ';A=self;RedirectSubwindows(display=A.display,onerror=onerror,opcode=A.display.get_extension_major(extname),window=A,update=update)
class UnredirectWindow(rq.Request):_request=rq.Struct(rq.Card8(_B),rq.Opcode(3),rq.RequestLength(),rq.Window(_A),rq.Set(_C,1,(RedirectAutomatic,RedirectManual)),rq.Pad(3))
def unredirect_window(self,update,onerror=None):'Stop redirecting this window hierarchy.\n    ';A=self;UnredirectWindow(display=A.display,onerror=onerror,opcode=A.display.get_extension_major(extname),window=A,update=update)
class UnredirectSubindows(rq.Request):_request=rq.Struct(rq.Card8(_B),rq.Opcode(4),rq.RequestLength(),rq.Window(_A),rq.Set(_C,1,(RedirectAutomatic,RedirectManual)),rq.Pad(3))
def unredirect_subwindows(self,update,onerror=None):'Stop redirecting the hierarchies of children to this window.\n    ';A=self;RedirectWindow(display=A.display,onerror=onerror,opcode=A.display.get_extension_major(extname),window=A,update=update)
class CreateRegionFromBorderClip(rq.Request):_request=rq.Struct(rq.Card8(_B),rq.Opcode(5),rq.RequestLength(),rq.Card32('region'),rq.Window(_A))
def create_region_from_border_clip(self,onerror=None):'Create a region of the border clip of the window, i.e. the area\n    that is not clipped by the parent and any sibling windows.\n    ';A=self;B=A.display.allocate_resource_id();CreateRegionFromBorderClip(display=A.display,onerror=onerror,opcode=A.display.get_extension_major(extname),region=B,window=A);return B
class NameWindowPixmap(rq.Request):_request=rq.Struct(rq.Card8(_B),rq.Opcode(6),rq.RequestLength(),rq.Window(_A),rq.Pixmap(_F))
def name_window_pixmap(self,onerror=None):'Create a new pixmap that refers to the off-screen storage of\n    the window, including its border.\n\n    This pixmap will remain allocated until freed whatever happens\n    with the window.  However, the window will get a new off-screen\n    pixmap every time it is mapped or resized, so to keep track of the\n    contents you must listen for these events and get a new pixmap\n    after them.\n    ';A=self;B=A.display.allocate_resource_id();NameWindowPixmap(display=A.display,onerror=onerror,opcode=A.display.get_extension_major(extname),window=A,pixmap=B);C=A.display.get_resource_class(_F,drawable.Pixmap);return C(A.display,B,owner=1)
class GetOverlayWindow(rq.ReplyRequest):_request=rq.Struct(rq.Card8(_B),rq.Opcode(7),rq.RequestLength(),rq.Window(_A));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_E),rq.ReplyLength(),rq.Window('overlay_window'),rq.Pad(20))
def get_overlay_window(self):'Return the overlay window of the root window.\n    ';A=self;return GetOverlayWindow(display=A.display,opcode=A.display.get_extension_major(extname),window=A)
def init(disp,info):A=disp;A.extension_add_method('display','composite_query_version',query_version);A.extension_add_method(_A,'composite_redirect_window',redirect_window);A.extension_add_method(_A,'composite_redirect_subwindows',redirect_subwindows);A.extension_add_method(_A,'composite_unredirect_window',unredirect_window);A.extension_add_method(_A,'composite_unredirect_subwindows',unredirect_subwindows);A.extension_add_method(_A,'composite_create_region_from_border_clip',create_region_from_border_clip);A.extension_add_method(_A,'composite_name_window_pixmap',name_window_pixmap);A.extension_add_method(_A,'composite_get_overlay_window',get_overlay_window)