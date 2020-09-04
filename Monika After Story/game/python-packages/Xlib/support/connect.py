# Xlib.support.connect -- OS-independent display connection functions
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

_C='unix_connect'
_B='vms_connect'
_A='OpenVMS'
import sys,importlib
_display_mods={_A:_B}
_default_display_mod=_C
_socket_mods={_A:_B}
_default_socket_mod=_C
_auth_mods={_A:_B}
_default_auth_mod=_C
_parts=sys.platform.split('-')
platform=_parts[0]
del _parts
def _relative_import(modname):return importlib.import_module('..'+modname,__name__)
def get_display(display):A=_display_mods.get(platform,_default_display_mod);B=_relative_import(A);return B.get_display(display)
def get_socket(dname,protocol,host,dno):A=_socket_mods.get(platform,_default_socket_mod);B=_relative_import(A);return B.get_socket(dname,protocol,host,dno)
def get_auth(sock,dname,protocol,host,dno):A=_auth_mods.get(platform,_default_auth_mod);B=_relative_import(A);return B.get_auth(sock,dname,protocol,host,dno)
