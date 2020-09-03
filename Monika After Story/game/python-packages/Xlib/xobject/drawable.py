# Xlib.xobject.drawable -- drawable objects (window and pixmap)
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

from Xlib.protocol import request

from . import resource

class Drawable(resource.Resource):
    __drawable__ = resource.Resource.__resource__

class Window(Drawable):
    __window__ = resource.Resource.__resource__

    _STRING_ENCODING = 'ISO-8859-1'
    _UTF8_STRING_ENCODING = 'UTF-8'

    def get_property(self, property, property_type, offset, length, delete = 0):
        r = request.GetProperty(display = self.display,
                                delete = delete,
                                window = self.id,
                                property = property,
                                type = property_type,
                                long_offset = offset,
                                long_length = length)

        if r.property_type:
            fmt, value = r.value
            r.format = fmt
            r.value = value
            return r
        else:
            return None

    def get_full_property(self, property, property_type, sizehint = 10):
        prop = self.get_property(property, property_type, 0, sizehint)
        if prop:
            val = prop.value
            if prop.bytes_after:
                prop = self.get_property(property, property_type, sizehint,
                                         prop.bytes_after // 4 + 1)
                val = val + prop.value

            prop.value = val
            return prop
        else:
            return None

def roundup(value, unit):
    return (value + (unit - 1)) & ~(unit - 1)
