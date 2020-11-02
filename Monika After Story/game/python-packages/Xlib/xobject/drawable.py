_E='WM_COLORMAP_WINDOWS'
_D='WM_PROTOCOLS'
_C='WM_STATE'
_B='UTF8_STRING'
_A='window'
from Xlib import X,Xatom,Xutil
from Xlib.protocol import request,rq
from .  import resource
from .  import colormap
from .  import cursor
from .  import fontable
from .  import icccm
class Drawable(resource.Resource):
	__drawable__=resource.Resource.__resource__
	def get_geometry(A):return request.GetGeometry(display=A.display,drawable=A)
	def create_pixmap(A,width,height,depth):B=A.display.allocate_resource_id();request.CreatePixmap(display=A.display,depth=depth,pid=B,drawable=A.id,width=width,height=height);C=A.display.get_resource_class('pixmap',Pixmap);return C(A.display,B,owner=1)
	def create_gc(A,**C):B=A.display.allocate_resource_id();request.CreateGC(display=A.display,cid=B,drawable=A.id,attrs=C);D=A.display.get_resource_class('gc',fontable.GC);return D(A.display,B,owner=1)
	def copy_area(A,gc,src_drawable,src_x,src_y,width,height,dst_x,dst_y,onerror=None):request.CopyArea(display=A.display,onerror=onerror,src_drawable=src_drawable,dst_drawable=A.id,gc=gc,src_x=src_x,src_y=src_y,dst_x=dst_x,dst_y=dst_y,width=width,height=height)
	def copy_plane(A,gc,src_drawable,src_x,src_y,width,height,dst_x,dst_y,bit_plane,onerror=None):request.CopyPlane(display=A.display,onerror=onerror,src_drawable=src_drawable,dst_drawable=A.id,gc=gc,src_x=src_x,src_y=src_y,dst_x=dst_x,dst_y=dst_y,width=width,height=height,bit_plane=bit_plane)
	def poly_point(A,gc,coord_mode,points,onerror=None):request.PolyPoint(display=A.display,onerror=onerror,coord_mode=coord_mode,drawable=A.id,gc=gc,points=points)
	def point(A,gc,x,y,onerror=None):request.PolyPoint(display=A.display,onerror=onerror,coord_mode=X.CoordModeOrigin,drawable=A.id,gc=gc,points=[(x,y)])
	def poly_line(A,gc,coord_mode,points,onerror=None):request.PolyLine(display=A.display,onerror=onerror,coord_mode=coord_mode,drawable=A.id,gc=gc,points=points)
	def line(A,gc,x1,y1,x2,y2,onerror=None):request.PolySegment(display=A.display,onerror=onerror,drawable=A.id,gc=gc,segments=[(x1,y1,x2,y2)])
	def poly_segment(A,gc,segments,onerror=None):request.PolySegment(display=A.display,onerror=onerror,drawable=A.id,gc=gc,segments=segments)
	def poly_rectangle(A,gc,rectangles,onerror=None):request.PolyRectangle(display=A.display,onerror=onerror,drawable=A.id,gc=gc,rectangles=rectangles)
	def rectangle(A,gc,x,y,width,height,onerror=None):request.PolyRectangle(display=A.display,onerror=onerror,drawable=A.id,gc=gc,rectangles=[(x,y,width,height)])
	def poly_arc(A,gc,arcs,onerror=None):request.PolyArc(display=A.display,onerror=onerror,drawable=A.id,gc=gc,arcs=arcs)
	def arc(A,gc,x,y,width,height,angle1,angle2,onerror=None):request.PolyArc(display=A.display,onerror=onerror,drawable=A.id,gc=gc,arcs=[(x,y,width,height,angle1,angle2)])
	def fill_poly(A,gc,shape,coord_mode,points,onerror=None):request.FillPoly(display=A.display,onerror=onerror,shape=shape,coord_mode=coord_mode,drawable=A.id,gc=gc,points=points)
	def poly_fill_rectangle(A,gc,rectangles,onerror=None):request.PolyFillRectangle(display=A.display,onerror=onerror,drawable=A.id,gc=gc,rectangles=rectangles)
	def fill_rectangle(A,gc,x,y,width,height,onerror=None):request.PolyFillRectangle(display=A.display,onerror=onerror,drawable=A.id,gc=gc,rectangles=[(x,y,width,height)])
	def poly_fill_arc(A,gc,arcs,onerror=None):request.PolyFillArc(display=A.display,onerror=onerror,drawable=A.id,gc=gc,arcs=arcs)
	def fill_arc(A,gc,x,y,width,height,angle1,angle2,onerror=None):request.PolyFillArc(display=A.display,onerror=onerror,drawable=A.id,gc=gc,arcs=[(x,y,width,height,angle1,angle2)])
	def put_image(A,gc,x,y,width,height,format,depth,left_pad,data,onerror=None):request.PutImage(display=A.display,onerror=onerror,format=format,drawable=A.id,gc=gc,width=width,height=height,dst_x=x,dst_y=y,left_pad=left_pad,depth=depth,data=data)
	def put_pil_image(A,gc,x,y,image,onerror=None):
		S='1';C=image;F,G=C.size
		if C.mode==S:
			format=X.XYBitmap;K=1
			if A.display.info.bitmap_format_bit_order==0:E='1;R'
			else:E=S
			H=A.display.info.bitmap_format_scanline_pad;I=roundup(F,H)>>3
		elif C.mode=='RGB':
			format=X.ZPixmap;K=24
			if A.display.info.image_byte_order==0:E='BGRX'
			else:E='RGBX'
			H=A.display.info.bitmap_format_scanline_pad;L=A.display.info.bitmap_format_scanline_unit;I=roundup(F*L,H)>>3
		else:raise ValueError('Unknown data format')
		M=(A.display.info.max_request_length<<2)-request.PutImage._request.static_size;N=M//I;O=0;P=F;D=0
		while D<G:
			B=min(G,N)
			if B<G:J=C.crop((O,D,P,D+B))
			else:J=C
			Q,B=J.size;R=J.tobytes('raw',E,I,0);A.put_image(gc,x,y,Q,B,format,K,0,R);D=D+B;y=y+B
	def get_image(A,x,y,width,height,format,plane_mask):return request.GetImage(display=A.display,format=format,drawable=A.id,x=x,y=y,width=width,height=height,plane_mask=plane_mask)
	def draw_text(A,gc,x,y,text,onerror=None):request.PolyText8(display=A.display,onerror=onerror,drawable=A.id,gc=gc,x=x,y=y,items=[text])
	def poly_text(A,gc,x,y,items,onerror=None):request.PolyText8(display=A.display,onerror=onerror,drawable=A.id,gc=gc,x=x,y=y,items=items)
	def poly_text_16(A,gc,x,y,items,onerror=None):request.PolyText16(display=A.display,onerror=onerror,drawable=A.id,gc=gc,x=x,y=y,items=items)
	def image_text(A,gc,x,y,string,onerror=None):request.ImageText8(display=A.display,onerror=onerror,drawable=A.id,gc=gc,x=x,y=y,string=string)
	def image_text_16(A,gc,x,y,string,onerror=None):request.ImageText16(display=A.display,onerror=onerror,drawable=A.id,gc=gc,x=x,y=y,string=string)
	def query_best_size(A,item_class,width,height):return request.QueryBestSize(display=A.display,item_class=item_class,drawable=A.id,width=width,height=height)
class Window(Drawable):
	__window__=resource.Resource.__resource__;_STRING_ENCODING='ISO-8859-1';_UTF8_STRING_ENCODING='UTF-8'
	def create_window(A,x,y,width,height,border_width,depth,window_class=X.CopyFromParent,visual=X.CopyFromParent,onerror=None,**C):B=A.display.allocate_resource_id();request.CreateWindow(display=A.display,onerror=onerror,depth=depth,wid=B,parent=A.id,x=x,y=y,width=width,height=height,border_width=border_width,window_class=window_class,visual=visual,attrs=C);D=A.display.get_resource_class(_A,Window);return D(A.display,B,owner=1)
	def change_attributes(A,onerror=None,**B):request.ChangeWindowAttributes(display=A.display,onerror=onerror,window=A.id,attrs=B)
	def get_attributes(A):return request.GetWindowAttributes(display=A.display,window=A.id)
	def destroy(A,onerror=None):request.DestroyWindow(display=A.display,onerror=onerror,window=A.id);A.display.free_resource_id(A.id)
	def destroy_sub_windows(A,onerror=None):request.DestroySubWindows(display=A.display,onerror=onerror,window=A.id)
	def change_save_set(A,mode,onerror=None):request.ChangeSaveSet(display=A.display,onerror=onerror,mode=mode,window=A.id)
	def reparent(A,parent,x,y,onerror=None):request.ReparentWindow(display=A.display,onerror=onerror,window=A.id,parent=parent,x=x,y=y)
	def map(A,onerror=None):request.MapWindow(display=A.display,onerror=onerror,window=A.id)
	def map_sub_windows(A,onerror=None):request.MapSubwindows(display=A.display,onerror=onerror,window=A.id)
	def unmap(A,onerror=None):request.UnmapWindow(display=A.display,onerror=onerror,window=A.id)
	def unmap_sub_windows(A,onerror=None):request.UnmapSubwindows(display=A.display,onerror=onerror,window=A.id)
	def configure(A,onerror=None,**B):request.ConfigureWindow(display=A.display,onerror=onerror,window=A.id,attrs=B)
	def circulate(A,direction,onerror=None):request.CirculateWindow(display=A.display,onerror=onerror,direction=direction,window=A.id)
	def raise_window(A,onerror=None):'alias for raising the window to the top - as in XRaiseWindow';A.configure(onerror,stack_mode=X.Above)
	def query_tree(A):return request.QueryTree(display=A.display,window=A.id)
	def change_property(A,property,property_type,format,data,mode=X.PropModeReplace,onerror=None):request.ChangeProperty(display=A.display,onerror=onerror,mode=mode,window=A.id,property=property,type=property_type,data=(format,data))
	def change_text_property(B,property,property_type,data,mode=X.PropModeReplace,onerror=None):
		C=property_type;A=data
		if not isinstance(A,bytes):
			if C==Xatom.STRING:A=A.encode(B._STRING_ENCODING)
			elif C==B.display.get_atom(_B):A=A.encode(B._UTF8_STRING_ENCODING)
		B.change_property(property,C,8,A,mode=mode,onerror=onerror)
	def delete_property(A,property,onerror=None):request.DeleteProperty(display=A.display,onerror=onerror,window=A.id,property=property)
	def get_property(B,property,property_type,offset,length,delete=0):
		A=request.GetProperty(display=B.display,delete=delete,window=B.id,property=property,type=property_type,long_offset=offset,long_length=length)
		if A.property_type:C,D=A.value;A.format=C;A.value=D;return A
		else:return None
	def get_full_property(C,property,property_type,sizehint=10):
		E=sizehint;D=property_type;A=C.get_property(property,D,0,E)
		if A:
			B=A.value
			if A.bytes_after:A=C.get_property(property,D,E,A.bytes_after//4+1);B=B+A.value
			A.value=B;return A
		else:return None
	def get_full_text_property(B,property,property_type=X.AnyPropertyType,sizehint=10):
		A=B.get_full_property(property,property_type,sizehint=sizehint)
		if A is None or A.format!=8:return None
		if A.property_type==Xatom.STRING:A.value=A.value.decode(B._STRING_ENCODING)
		elif A.property_type==B.display.get_atom(_B):A.value=A.value.decode(B._UTF8_STRING_ENCODING)
		return A.value
	def list_properties(A):B=request.ListProperties(display=A.display,window=A.id);return B.atoms
	def set_selection_owner(A,selection,time,onerror=None):request.SetSelectionOwner(display=A.display,onerror=onerror,window=A.id,selection=selection,time=time)
	def convert_selection(A,selection,target,property,time,onerror=None):request.ConvertSelection(display=A.display,onerror=onerror,requestor=A.id,selection=selection,target=target,property=property,time=time)
	def send_event(A,event,event_mask=0,propagate=0,onerror=None):request.SendEvent(display=A.display,onerror=onerror,propagate=propagate,destination=A.id,event_mask=event_mask,event=event)
	def grab_pointer(A,owner_events,event_mask,pointer_mode,keyboard_mode,confine_to,cursor,time):B=request.GrabPointer(display=A.display,owner_events=owner_events,grab_window=A.id,event_mask=event_mask,pointer_mode=pointer_mode,keyboard_mode=keyboard_mode,confine_to=confine_to,cursor=cursor,time=time);return B.status
	def grab_button(A,button,modifiers,owner_events,event_mask,pointer_mode,keyboard_mode,confine_to,cursor,onerror=None):request.GrabButton(display=A.display,onerror=onerror,owner_events=owner_events,grab_window=A.id,event_mask=event_mask,pointer_mode=pointer_mode,keyboard_mode=keyboard_mode,confine_to=confine_to,cursor=cursor,button=button,modifiers=modifiers)
	def ungrab_button(A,button,modifiers,onerror=None):request.UngrabButton(display=A.display,onerror=onerror,button=button,grab_window=A.id,modifiers=modifiers)
	def grab_keyboard(A,owner_events,pointer_mode,keyboard_mode,time):B=request.GrabKeyboard(display=A.display,owner_events=owner_events,grab_window=A.id,time=time,pointer_mode=pointer_mode,keyboard_mode=keyboard_mode);return B.status
	def grab_key(A,key,modifiers,owner_events,pointer_mode,keyboard_mode,onerror=None):request.GrabKey(display=A.display,onerror=onerror,owner_events=owner_events,grab_window=A.id,modifiers=modifiers,key=key,pointer_mode=pointer_mode,keyboard_mode=keyboard_mode)
	def ungrab_key(A,key,modifiers,onerror=None):request.UngrabKey(display=A.display,onerror=onerror,key=key,grab_window=A.id,modifiers=modifiers)
	def query_pointer(A):return request.QueryPointer(display=A.display,window=A.id)
	def get_motion_events(A,start,stop):B=request.GetMotionEvents(display=A.display,window=A.id,start=start,stop=stop);return B.events
	def translate_coords(A,src_window,src_x,src_y):return request.TranslateCoords(display=A.display,src_wid=src_window,dst_wid=A.id,src_x=src_x,src_y=src_y)
	def warp_pointer(A,x,y,src_window=0,src_x=0,src_y=0,src_width=0,src_height=0,onerror=None):request.WarpPointer(display=A.display,onerror=onerror,src_window=src_window,dst_window=A.id,src_x=src_x,src_y=src_y,src_width=src_width,src_height=src_height,dst_x=x,dst_y=y)
	def set_input_focus(A,revert_to,time,onerror=None):request.SetInputFocus(display=A.display,onerror=onerror,revert_to=revert_to,focus=A.id,time=time)
	def clear_area(A,x=0,y=0,width=0,height=0,exposures=0,onerror=None):request.ClearArea(display=A.display,onerror=onerror,exposures=exposures,window=A.id,x=x,y=y,width=width,height=height)
	def create_colormap(A,visual,alloc):B=A.display.allocate_resource_id();request.CreateColormap(display=A.display,alloc=alloc,mid=B,window=A.id,visual=visual);C=A.display.get_resource_class('colormap',colormap.Colormap);return C(A.display,B,owner=1)
	def list_installed_colormaps(A):B=request.ListInstalledColormaps(display=A.display,window=A.id);return B.cmaps
	def rotate_properties(A,properties,delta,onerror=None):request.RotateProperties(display=A.display,onerror=onerror,window=A.id,delta=delta,properties=properties)
	def set_wm_name(A,name,onerror=None):A.change_text_property(Xatom.WM_NAME,Xatom.STRING,name,onerror=onerror)
	def get_wm_name(A):return A.get_full_text_property(Xatom.WM_NAME,Xatom.STRING)
	def set_wm_icon_name(A,name,onerror=None):A.change_text_property(Xatom.WM_ICON_NAME,Xatom.STRING,name,onerror=onerror)
	def get_wm_icon_name(A):return A.get_full_text_property(Xatom.WM_ICON_NAME,Xatom.STRING)
	def set_wm_class(A,inst,cls,onerror=None):A.change_text_property(Xatom.WM_CLASS,Xatom.STRING,'%s\x00%s\x00'%(inst,cls),onerror=onerror)
	def get_wm_class(C):
		B=C.get_full_text_property(Xatom.WM_CLASS,Xatom.STRING)
		if B is None:return None
		A=B.split('\x00')
		if len(A)<2:return None
		else:return A[0],A[1]
	def set_wm_transient_for(A,window,onerror=None):A.change_property(Xatom.WM_TRANSIENT_FOR,Xatom.WINDOW,32,[window.id],onerror=onerror)
	def get_wm_transient_for(B):
		A=B.get_property(Xatom.WM_TRANSIENT_FOR,Xatom.WINDOW,0,1)
		if A is None or A.format!=32 or len(A.value)<1:return None
		else:C=B.display.get_resource_class(_A,Window);return C(B.display,A.value[0])
	def set_wm_protocols(A,protocols,onerror=None):A.change_property(A.display.get_atom(_D),Xatom.ATOM,32,protocols,onerror=onerror)
	def get_wm_protocols(B):
		A=B.get_full_property(B.display.get_atom(_D),Xatom.ATOM)
		if A is None or A.format!=32:return[]
		else:return A.value
	def set_wm_colormap_windows(A,windows,onerror=None):A.change_property(A.display.get_atom(_E),Xatom.WINDOW,32,map(lambda w:w.id,windows),onerror=onerror)
	def get_wm_colormap_windows(A):
		B=A.get_full_property(A.display.get_atom(_E),Xatom.WINDOW)
		if B is None or B.format!=32:return[]
		else:C=A.display.get_resource_class(_A,Window);return map(lambda i,d=A.display,c=C:c(d,i),B.value)
	def set_wm_client_machine(A,name,onerror=None):A.change_text_property(Xatom.WM_CLIENT_MACHINE,Xatom.STRING,name,onerror=onerror)
	def get_wm_client_machine(A):return A.get_full_text_property(Xatom.WM_CLIENT_MACHINE,Xatom.STRING)
	def set_wm_normal_hints(B,hints={},onerror=None,**A):B._set_struct_prop(Xatom.WM_NORMAL_HINTS,Xatom.WM_SIZE_HINTS,icccm.WMNormalHints,hints,A,onerror)
	def get_wm_normal_hints(A):return A._get_struct_prop(Xatom.WM_NORMAL_HINTS,Xatom.WM_SIZE_HINTS,icccm.WMNormalHints)
	def set_wm_hints(B,hints={},onerror=None,**A):B._set_struct_prop(Xatom.WM_HINTS,Xatom.WM_HINTS,icccm.WMHints,hints,A,onerror)
	def get_wm_hints(A):return A._get_struct_prop(Xatom.WM_HINTS,Xatom.WM_HINTS,icccm.WMHints)
	def set_wm_state(A,hints={},onerror=None,**C):B=A.display.get_atom(_C);A._set_struct_prop(B,B,icccm.WMState,hints,C,onerror)
	def get_wm_state(A):B=A.display.get_atom(_C);return A._get_struct_prop(B,B,icccm.WMState)
	def set_wm_icon_size(B,hints={},onerror=None,**A):B._set_struct_prop(Xatom.WM_ICON_SIZE,Xatom.WM_ICON_SIZE,icccm.WMIconSize,hints,A,onerror)
	def get_wm_icon_size(A):return A._get_struct_prop(Xatom.WM_ICON_SIZE,Xatom.WM_ICON_SIZE,icccm.WMIconSize)
	def _get_struct_prop(C,pname,ptype,pstruct):
		A=pstruct;B=C.get_property(pname,ptype,0,A.static_size//4)
		if B and B.format==32:
			D=B.value.tostring()
			if len(D)==A.static_size:return A.parse_binary(D,C.display)[0]
		return None
	def _set_struct_prop(C,pname,ptype,pstruct,hints,keys,onerror):
		B=keys;A=hints
		if isinstance(A,rq.DictWrapper):B.update(A._data)
		else:B.update(A)
		D=pstruct.to_binary(*(),**B);C.change_property(pname,ptype,32,D,onerror=onerror)
class Pixmap(Drawable):
	__pixmap__=resource.Resource.__resource__
	def free(A,onerror=None):request.FreePixmap(display=A.display,onerror=onerror,pixmap=A.id);A.display.free_resource_id(A.id)
	def create_cursor(A,mask,foreground,background,x,y):C,D,E=foreground;F,G,H=background;B=A.display.allocate_resource_id();request.CreateCursor(display=A.display,cid=B,source=A.id,mask=mask,fore_red=C,fore_green=D,fore_blue=E,back_red=F,back_green=G,back_blue=H,x=x,y=y);I=A.display.get_resource_class('cursor',cursor.Cursor);return I(A.display,B,owner=1)
def roundup(value,unit):return value+(unit-1)&~(unit-1)