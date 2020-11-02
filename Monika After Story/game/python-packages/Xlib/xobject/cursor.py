from Xlib.protocol import request
from .  import resource
class Cursor(resource.Resource):
	__cursor__=resource.Resource.__resource__
	def free(A,onerror=None):request.FreeCursor(display=A.display,onerror=onerror,cursor=A.id);A.display.free_resource_id(A.id)
	def recolor(A,foreground,background,onerror=None):B,C,D=foreground;E,F,G=background;request.RecolorCursor(display=A.display,onerror=onerror,cursor=A.id,fore_red=B,fore_green=C,fore_blue=D,back_red=E,back_green=F,back_blue=G)