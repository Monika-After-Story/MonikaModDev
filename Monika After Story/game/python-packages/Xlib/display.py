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
# Xlib.protocol modules
from .protocol import display as protocol_display
from .protocol import request, event, rq

# Xlib.xobjects modules
from .xobject import resource
from .xobject import drawable

_resource_baseclasses = {
    'resource': resource.Resource,
    'drawable': drawable.Drawable,
    'window': drawable.Window,
    'pixmap': drawable.Pixmap
    }

_resource_hierarchy = {
    'resource': ('drawable', 'window', 'pixmap'),
    'drawable': ('window', 'pixmap'),
    'fontable': ('font', 'gc')
    }

class _BaseDisplay(protocol_display.Display):
    def __init__(self, *args, **keys):
        self.resource_classes = _resource_baseclasses.copy()
        protocol_display.Display.__init__(self, *args, **keys)
        self._atom_cache = {}

    def get_atom(self, atomname, only_if_exists=0):
        if atomname in self._atom_cache:
            return self._atom_cache[atomname]

        r = request.InternAtom(display = self, name = atomname, only_if_exists = only_if_exists)
        if r.atom != 0:
            self._atom_cache[atomname] = r.atom

        return r.atom


class Display(object):
    def __init__(self, display = None):
        self.display = _BaseDisplay(display)
        self._keymap_codes = [()] * 256
        self._keymap_syms = {}
        self.keysym_translations = {}
        self.extensions = []
        self.class_extension_dicts = {}
        self.display_extension_methods = {}
        self.extension_event = rq.DictWrapper({})

    def close(self):
        self.display.close()

    def flush(self):
        self.display.flush()

    def create_resource_object(self, type, id):
        return self.display.resource_classes[type](self.display, id)

    def screen(self, sno = None):
        if sno is None:
            return self.display.info.roots[self.display.default_screen]
        else:
            return self.display.info.roots[sno]

    def intern_atom(self, name, only_if_exists = 0):
        r = request.InternAtom(display = self.display,
                               name = name,
                               only_if_exists = only_if_exists)
        return r.atom
