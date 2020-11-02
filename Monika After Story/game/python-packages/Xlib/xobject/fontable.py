from Xlib.protocol import request
from .  import resource
from .  import cursor
class Fontable(resource.Resource):
	__fontable__=resource.Resource.__resource__
	def query(A):return request.QueryFont(display=A.display,font=A.id)
	def query_text_extents(A,string):return request.QueryTextExtents(display=A.display,font=A.id,string=string)
class GC(Fontable):
	__gc__=resource.Resource.__resource__
	def change(A,onerror=None,**B):request.ChangeGC(display=A.display,onerror=onerror,gc=A.id,attrs=B)
	def copy(A,src_gc,mask,onerror=None):request.CopyGC(display=A.display,onerror=onerror,src_gc=src_gc,dst_gc=A.id,mask=mask)
	def set_dashes(A,offset,dashes,onerror=None):request.SetDashes(display=A.display,onerror=onerror,gc=A.id,dash_offset=offset,dashes=dashes)
	def set_clip_rectangles(A,x_origin,y_origin,rectangles,ordering,onerror=None):request.SetClipRectangles(display=A.display,onerror=onerror,ordering=ordering,gc=A.id,x_origin=x_origin,y_origin=y_origin,rectangles=rectangles)
	def free(A,onerror=None):request.FreeGC(display=A.display,onerror=onerror,gc=A.id);A.display.free_resource_id(A.id)
class Font(Fontable):
	__font__=resource.Resource.__resource__
	def close(A,onerror=None):request.CloseFont(display=A.display,onerror=onerror,font=A.id);A.display.free_resource_id(A.id)
	def create_glyph_cursor(A,mask,source_char,mask_char,foreground,background):C,D,E=foreground;F,G,H=background;B=A.display.allocate_resource_id();request.CreateGlyphCursor(display=A.display,cid=B,source=A.id,mask=mask,source_char=source_char,mask_char=mask_char,fore_red=C,fore_green=D,fore_blue=E,back_red=F,back_green=G,back_blue=H);I=A.display.get_resource_class('cursor',cursor.Cursor);return I(A.display,B,owner=1)