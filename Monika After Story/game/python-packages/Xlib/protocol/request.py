# Xlib.protocol.request -- definitions of core requests
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

# *** This file has been minified using python-minifier

_C='sequence_number'
_B='name'
_A='value'
from ..  import X
from .  import rq
class InternAtom(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(16),rq.Bool('only_if_exists'),rq.RequestLength(),rq.LengthOf(_B,2),rq.Pad(2),rq.String8(_B));_reply=rq.Struct(rq.ReplyCode(),rq.Pad(1),rq.Card16(_C),rq.ReplyLength(),rq.Card32('atom'),rq.Pad(20))
class GetProperty(rq.ReplyRequest):_request=rq.Struct(rq.Opcode(20),rq.Bool('delete'),rq.RequestLength(),rq.Window('window'),rq.Card32('property'),rq.Card32('type'),rq.Card32('long_offset'),rq.Card32('long_length'));_reply=rq.Struct(rq.ReplyCode(),rq.Format(_A,1),rq.Card16(_C),rq.ReplyLength(),rq.Card32('property_type'),rq.Card32('bytes_after'),rq.LengthOf(_A,4),rq.Pad(12),rq.PropertyData(_A))
