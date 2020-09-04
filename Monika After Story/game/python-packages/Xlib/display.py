# Xlib.display -- high level display object
#
#    Copyright (C) 2000 Peter Liljenberg <petli@ctrl-c.liu.se>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 2.1
# of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
#    Free Software Foundation, Inc.,
#    59 Temple Place,
#    Suite 330,
#    Boston, MA 02111-1307 USA

# *** This file has been minified using python-minifier

_D='resource'
_C=None
_B='window'
_A='drawable'
from .protocol import display as protocol_display,request,event,rq
from .xobject import resource
from .xobject import drawable
_resource_baseclasses={_D:resource.Resource,_A:drawable.Drawable,_B:drawable.Window}
_resource_hierarchy={_D:(_A,_B),_A:(_B,'pixmap')}
class _BaseDisplay(protocol_display.Display):
	def __init__(A,*B,**C):A.resource_classes=_resource_baseclasses.copy();protocol_display.Display.__init__(A,*B,**C);A._atom_cache={}
	def get_atom(A,atomname,only_if_exists=0):
		B=atomname
		if B in A._atom_cache:return A._atom_cache[B]
		C=request.InternAtom(display=A,name=B,only_if_exists=only_if_exists)
		if C.atom!=0:A._atom_cache[B]=C.atom
		return C.atom
class Display:
	def __init__(A,display=_C):A.display=_BaseDisplay(display);A._keymap_codes=[()]*256;A._keymap_syms={};A.keysym_translations={};A.extensions=[];A.class_extension_dicts={};A.display_extension_methods={};A.extension_event=rq.DictWrapper({})
	def close(A):A.display.close()
	def flush(A):A.display.flush()
	def create_resource_object(A,type,id):return A.display.resource_classes[type](A.display,id)
	def screen(A,sno=_C):
		if sno is _C:return A.display.info.roots[A.display.default_screen]
		else:return A.display.info.roots[sno]
	def intern_atom(A,name,only_if_exists=0):B=request.InternAtom(display=A.display,name=name,only_if_exists=only_if_exists);return B.atom
