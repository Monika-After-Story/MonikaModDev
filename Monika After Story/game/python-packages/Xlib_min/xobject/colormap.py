from Xlib import error
from Xlib.protocol import request
from .  import resource
import re
rgb_res=[re.compile('\\Argb:([0-9a-fA-F]{1,4})/([0-9a-fA-F]{1,4})/([0-9a-fA-F]{1,4})\\Z'),re.compile('\\A#([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])\\Z'),re.compile('\\A#([0-9a-fA-F][0-9a-fA-F])([0-9a-fA-F][0-9a-fA-F])([0-9a-fA-F][0-9a-fA-F])\\Z'),re.compile('\\A#([0-9a-fA-F][0-9a-fA-F][0-9a-fA-F])([0-9a-fA-F][0-9a-fA-F][0-9a-fA-F])([0-9a-fA-F][0-9a-fA-F][0-9a-fA-F])\\Z'),re.compile('\\A#([0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F])([0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F])([0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F])\\Z')]
class Colormap(resource.Resource):
	__colormap__=resource.Resource.__resource__
	def free(A,onerror=None):request.FreeColormap(display=A.display,onerror=onerror,cmap=A.id);A.display.free_resource_id(A.id)
	def copy_colormap_and_free(A,scr_cmap):B=A.display.allocate_resource_id();request.CopyColormapAndFree(display=A.display,mid=B,src_cmap=src_cmap);C=A.display.get_resource_class('colormap',Colormap);return C(A.display,B,owner=1)
	def install_colormap(A,onerror=None):request.InstallColormap(display=A.display,onerror=onerror,cmap=A.id)
	def uninstall_colormap(A,onerror=None):request.UninstallColormap(display=A.display,onerror=onerror,cmap=A.id)
	def alloc_color(A,red,green,blue):return request.AllocColor(display=A.display,cmap=A.id,red=red,green=green,blue=blue)
	def alloc_named_color(B,name):
		G='0'
		for C in rgb_res:
			A=C.match(name)
			if A:D=A.group(1);C=int(D+G*(4-len(D)),16);E=A.group(2);H=int(E+G*(4-len(E)),16);F=A.group(3);I=int(F+G*(4-len(F)),16);return B.alloc_color(C,H,I)
		try:return request.AllocNamedColor(display=B.display,cmap=B.id,name=name)
		except error.BadName:return None
	def alloc_color_cells(A,contiguous,colors,planes):return request.AllocColorCells(display=A.display,contiguous=contiguous,cmap=A.id,colors=colors,planes=planes)
	def alloc_color_planes(A,contiguous,colors,red,green,blue):return request.AllocColorPlanes(display=A.display,contiguous=contiguous,cmap=A.id,colors=colors,red=red,green=green,blue=blue)
	def free_colors(A,pixels,plane_mask,onerror=None):request.FreeColors(display=A.display,onerror=onerror,cmap=A.id,plane_mask=plane_mask,pixels=pixels)
	def store_colors(A,items,onerror=None):request.StoreColors(display=A.display,onerror=onerror,cmap=A.id,items=items)
	def store_named_color(A,name,pixel,flags,onerror=None):request.StoreNamedColor(display=A.display,onerror=onerror,flags=flags,cmap=A.id,pixel=pixel,name=name)
	def query_colors(A,pixels):B=request.QueryColors(display=A.display,cmap=A.id,pixels=pixels);return B.colors
	def lookup_color(A,name):return request.LookupColor(display=A.display,cmap=A.id,name=name)