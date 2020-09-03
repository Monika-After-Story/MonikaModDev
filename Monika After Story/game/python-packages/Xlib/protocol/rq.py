# Xlib.protocol.rq -- structure primitives for request, events and errors
#
#    Copyright (C) 2000-2002 Peter Liljenberg <petli@ctrl-c.liu.se>
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

# Standard modules
import sys
import traceback
import struct
from array import array
import types

# Python 2/3 compatibility.
from six import PY3, binary_type, byte2int, indexbytes, iterbytes

# Xlib modules
from .. import X
from ..support import lock


def decode_string(bs):
    return bs.decode('latin1')

if PY3:
    def encode_array(a):
        return a.tobytes()
else:
    def encode_array(a):
        return a.tostring()


class BadDataError(Exception): pass

signed_codes = { 1: 'b', 2: 'h', 4: 'l' }
unsigned_codes = { 1: 'B', 2: 'H', 4: 'L' }

array_unsigned_codes = { }
struct_to_array_codes = { }

for c in 'bhil':
    size = array(c).itemsize
    array_unsigned_codes[size] = c.upper()
    try:
        struct_to_array_codes[signed_codes[size]] = c
        struct_to_array_codes[unsigned_codes[size]] = c.upper()
    except KeyError:
        pass

class Field(object):
    name = None
    default = None

    structcode = None
    structvalues = 0

    check_value = None
    parse_value = None

    keyword_args = 0

    def __init__(self):
        pass

    def parse_binary_value(self, data, display, length, format):
        raise RuntimeError('Neither structcode or parse_binary_value ' \
                'provided for {0}'.format(self))

class Pad(Field):
    def __init__(self, size):
        self.size = size
        self.value = b'\0' * size
        self.structcode = '{0}x'.format(size)
        self.structvalues = 0


class ConstantField(Field):
    def __init__(self, value):
        self.value = value

class Opcode(ConstantField):
    structcode = 'B'
    structvalues = 1

class ReplyCode(ConstantField):
    structcode = 'B'
    structvalues = 1

    def __init__(self):
        self.value = 1

class LengthField(Field):
    structcode = 'L'
    structvalues = 1
    other_fields = None

    def calc_length(self, length):
        return length


class TotalLengthField(LengthField):
    pass

class RequestLength(TotalLengthField):
    structcode = 'H'
    structvalues = 1

    def calc_length(self, length):
        return length // 4

class ReplyLength(TotalLengthField):
    structcode = 'L'
    structvalues = 1

    def calc_length(self, length):
        return (length - 32) // 4

class LengthOf(LengthField):
    def __init__(self, name, size):
        if isinstance(name, (list, tuple)):
            self.name = name[0]
            self.other_fields = name[1:]
        else:
            self.name = name
        self.structcode = unsigned_codes[size]

class Card16(ValueField):
    structcode = 'H'
    structvalues = 1

class Card32(ValueField):
    structcode = 'L'
    structvalues = 1

class Resource(Card32):
    cast_function = '__resource__'
    class_name = 'resource'

    def __init__(self, name, codes = (), default = None):
        Card32.__init__(self, name, default)
        self.codes = codes

    def check_value(self, value):
        if hasattr(value, self.cast_function):
            return getattr(value, self.cast_function)()
        else:
            return value

    def parse_value(self, value, display):
        if value in self.codes:
            return value

        c = display.get_resource_class(self.class_name)
        if c:
            return c(display, value)
        else:
            return value

class Window(Resource):
    cast_function = '__window__'
    class_name = 'window'

class Bool(ValueField):
    structvalues = 1
    structcode = 'B'

    def check_value(self, value):
        return not not value

class String8(ValueField):
    structcode = None

    def __init__(self, name, pad = 1):
        ValueField.__init__(self, name)
        self.pad = pad

    def pack_value(self, val):
        if isinstance(val, bytes):
            val_bytes = val
        else:
            val_bytes = val.encode()
        slen = len(val_bytes)

        if self.pad:
            return val_bytes + b'\0' * ((4 - slen % 4) % 4), slen, None
        else:
            return val_bytes, slen, None

    def parse_binary_value(self, data, display, length, format):
        if length is None:
            return decode_string(data), b''

        if self.pad:
            slen = length + ((4 - length % 4) % 4)
        else:
            slen = length

        data_str = decode_string(data[:length])

        return data_str, data[slen:]

class Object(ValueField):
    def __init__(self, name, type, default = None):
        ValueField.__init__(self, name, default)
        self.type = type
        self.structcode = self.type.structcode
        self.structvalues = self.type.structvalues

    def parse_binary_value(self, data, display, length, format):
        return self.type.parse_binary(data, display)

    def parse_value(self, val, display):
        return self.type.parse_value(val, display)

    def pack_value(self, val):
        return self.type.pack_value(val)

    def check_value(self, val):
        if isinstance(val, tuple):
            vals = []
            i = 0
            for f in self.type.fields:
                if f.name:
                    if f.check_value is None:
                        v = val[i]
                    else:
                        v = f.check_value(val[i])
                    if f.structvalues == 1:
                        vals.append(v)
                    else:
                        vals.extend(v)
                    i = i + 1
            return vals

        if isinstance(val, dict):
            data = val
        elif isinstance(val, DictWrapper):
            data = val._data
        else:
            raise TypeError('Object value must be tuple, dictionary or DictWrapper: %s' % val)

        vals = []
        for f in self.type.fields:
            if f.name:
                if f.check_value is None:
                    v = data[f.name]
                else:
                    v = f.check_value(data[f.name])
                if f.structvalues == 1:
                    vals.append(v)
                else:
                    vals.extend(v)

        return vals

class PropertyData(ValueField):
    structcode = None

    def parse_binary_value(self, data, display, length, format):
        if length is None:
            length = len(data) // (format // 8)
        else:
            length = int(length)

        if format == 0:
            ret = None

        elif format == 8:
            ret = (8, data[:length])
            data = data[length + ((4 - length % 4) % 4):]

        elif format == 16:
            ret = (16, array(array_unsigned_codes[2], data[:2 * length]))
            data = data[2 * (length + length % 2):]

        elif format == 32:
            ret = (32, array(array_unsigned_codes[4], data[:4 * length]))
            data = data[4 * length:]

        return ret, data

    def pack_value(self, value):
        fmt, val = value

        if fmt not in (8, 16, 32):
            raise BadDataError('Invalid property data format {0}'.format(fmt))

        if isinstance(val, binary_type):
            size = fmt // 8
            vlen = len(val)
            if vlen % size:
                vlen = vlen - vlen % size
                data = val[:vlen]
            else:
                data = val

            dlen = vlen // size

        else:
            if isinstance(val, tuple):
                val = list(val)

            size = fmt // 8
            a = array(array_unsigned_codes[size], val)
            data = encode_array(a)
            dlen = len(val)

        dl = len(data)
        data = data + b'\0' * ((4 - dl % 4) % 4)

        return data, dlen, fmt

class ResourceObj(object):
    structcode = 'L'
    structvalues = 1

    def __init__(self, class_name):
        self.class_name = class_name
        self.check_value = None

    def parse_value(self, value, display):
        # if not display:
        #     return value
        c = display.get_resource_class(self.class_name)
        if c:
            return c(display, value)
        else:
            return value

WindowObj = ResourceObj('window')
ColormapObj = ResourceObj('colormap')

def call_error_handler(handler, error, request):
    try:
        return handler(error, request)
    except:
        sys.stderr.write('Exception raised by error handler.\n')
        traceback.print_exc()
        return 0
