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


# Xlib modules
from .. import X

# Xlib.protocol modules
from . import rq

class InternAtom(rq.ReplyRequest):
    _request = rq.Struct(
        rq.Opcode(16),
        rq.Bool('only_if_exists'),
        rq.RequestLength(),
        rq.LengthOf('name', 2),
        rq.Pad(2),
        rq.String8('name'),
        )

    _reply = rq.Struct(
        rq.ReplyCode(),
        rq.Pad(1),
        rq.Card16('sequence_number'),
        rq.ReplyLength(),
        rq.Card32('atom'),
        rq.Pad(20),
        )
