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

# *** This file has been minified using python-minifier

_P='%s(%s)'
_O='colormap'
_N='window'
_M='odd'
_L='even'
_K='send_event'
_J='delta'
_I='type'
_H='string'
_G='='
_F='L'
_E='H'
_D=b''
_C=b'\x00'
_B='B'
_A=None
import sys,traceback,struct
from array import array
import types
from six import PY3,binary_type,byte2int,indexbytes,iterbytes
from ..  import X
from ..support import lock
def decode_string(bs):return bs.decode('latin1')
if PY3:
	def encode_array(a):return a.tobytes()
else:
	def encode_array(a):return a.tostring()
class BadDataError(Exception):0
signed_codes={1:'b',2:'h',4:'l'}
unsigned_codes={1:_B,2:_E,4:_F}
array_unsigned_codes={}
struct_to_array_codes={}
for c in 'bhil':
	size=array(c).itemsize;array_unsigned_codes[size]=c.upper()
	try:struct_to_array_codes[signed_codes[size]]=c;struct_to_array_codes[unsigned_codes[size]]=c.upper()
	except KeyError:pass
class Field:
	name=_A;default=_A;structcode=_A;structvalues=0;check_value=_A;parse_value=_A;keyword_args=0
	def __init__(A):0
	def parse_binary_value(A,data,display,length,format):raise RuntimeError('Neither structcode or parse_binary_value provided for {0}'.format(A))
class Pad(Field):
	def __init__(A,size):B=size;A.size=B;A.value=_C*B;A.structcode='{0}x'.format(B);A.structvalues=0
class ConstantField(Field):
	def __init__(A,value):A.value=value
class Opcode(ConstantField):structcode=_B;structvalues=1
class ReplyCode(ConstantField):
	structcode=_B;structvalues=1
	def __init__(A):A.value=1
class LengthField(Field):
	structcode=_F;structvalues=1;other_fields=_A
	def calc_length(A,length):return length
class TotalLengthField(LengthField):0
class RequestLength(TotalLengthField):
	structcode=_E;structvalues=1
	def calc_length(A,length):return length//4
class ReplyLength(TotalLengthField):
	structcode=_F;structvalues=1
	def calc_length(A,length):return(length-32)//4
class LengthOf(LengthField):
	def __init__(A,name,size):
		B=name
		if isinstance(B,(list,tuple)):A.name=B[0];A.other_fields=B[1:]
		else:A.name=B
		A.structcode=unsigned_codes[size]
class OddLength(LengthField):
	structcode=_B;structvalues=1
	def __init__(A,name):A.name=name
	def calc_length(A,length):return length%2
	def parse_value(A,value,display):
		if value==0:return _L
		else:return _M
class FormatField(Field):
	structvalues=1
	def __init__(A,name,size):A.name=name;A.structcode=unsigned_codes[size]
Format=FormatField
class ValueField(Field):
	def __init__(A,name,default=_A):A.name=name;A.default=default
class Int8(ValueField):structcode='b';structvalues=1
class Int16(ValueField):structcode='h';structvalues=1
class Int32(ValueField):structcode='l';structvalues=1
class Card8(ValueField):structcode=_B;structvalues=1
class Card16(ValueField):structcode=_E;structvalues=1
class Card32(ValueField):structcode=_F;structvalues=1
class Resource(Card32):
	cast_function='__resource__';class_name='resource'
	def __init__(A,name,codes=(),default=_A):Card32.__init__(A,name,default);A.codes=codes
	def check_value(B,value):
		A=value
		if hasattr(A,B.cast_function):return getattr(A,B.cast_function)()
		else:return A
	def parse_value(B,value,display):
		C=display;A=value
		if A in B.codes:return A
		D=C.get_resource_class(B.class_name)
		if D:return D(C,A)
		else:return A
class Window(Resource):cast_function='__window__';class_name=_N
class Pixmap(Resource):cast_function='__pixmap__';class_name='pixmap'
class Drawable(Resource):cast_function='__drawable__';class_name='drawable'
class Fontable(Resource):cast_function='__fontable__';class_name='fontable'
class Font(Resource):cast_function='__font__';class_name='font'
class GC(Resource):cast_function='__gc__';class_name='gc'
class Colormap(Resource):cast_function='__colormap__';class_name=_O
class Cursor(Resource):cast_function='__cursor__';class_name='cursor'
class Bool(ValueField):
	structvalues=1;structcode=_B
	def check_value(A,value):return not(not value)
class Set(ValueField):
	structvalues=1
	def __init__(A,name,size,values,default=_A):ValueField.__init__(A,name,default);A.structcode=unsigned_codes[size];A.values=values
	def check_value(A,val):
		B=val
		if B not in A.values:raise ValueError('field %s: argument %s not in %s'%(A.name,B,A.values))
		return B
class Gravity(Set):
	def __init__(A,name):Set.__init__(A,name,1,(X.ForgetGravity,X.StaticGravity,X.NorthWestGravity,X.NorthGravity,X.NorthEastGravity,X.WestGravity,X.CenterGravity,X.EastGravity,X.SouthWestGravity,X.SouthGravity,X.SouthEastGravity))
class FixedBinary(ValueField):
	structvalues=1
	def __init__(A,name,size):ValueField.__init__(A,name);A.structcode='{0}s'.format(size)
class Binary(ValueField):
	structcode=_A
	def __init__(A,name,pad=1):ValueField.__init__(A,name);A.pad=pad
	def pack_value(C,val):
		A=val;B=len(A)
		if C.pad:return A+_C*((4-B%4)%4),B,_A
		else:return A,B,_A
	def parse_binary_value(D,data,display,length,format):
		B=data;A=length
		if A is _A:return B,_D
		if D.pad:C=A+(4-A%4)%4
		else:C=A
		return B[:A],B[C:]
class String8(ValueField):
	structcode=_A
	def __init__(A,name,pad=1):ValueField.__init__(A,name);A.pad=pad
	def pack_value(D,val):
		B=val
		if isinstance(B,bytes):A=B
		else:A=B.encode()
		C=len(A)
		if D.pad:return A+_C*((4-C%4)%4),C,_A
		else:return A,C,_A
	def parse_binary_value(D,data,display,length,format):
		B=data;A=length
		if A is _A:return decode_string(B),_D
		if D.pad:C=A+(4-A%4)%4
		else:C=A
		E=decode_string(B[:A]);return E,B[C:]
class String16(ValueField):
	structcode=_A
	def __init__(A,name,pad=1):ValueField.__init__(A,name);A.pad=pad
	def pack_value(D,val):
		A=val
		if isinstance(A,bytes):A=list(iterbytes(A))
		B=len(A)
		if D.pad:C=b'\x00\x00'*(B%2)
		else:C=_D
		return struct.pack('>'+_E*B,*A)+C,B,_A
	def parse_binary_value(D,data,display,length,format):
		B=data;A=length
		if A==_M:A=len(B)//2-1
		elif A==_L:A=len(B)//2
		if D.pad:C=A+A%2
		else:C=A
		return struct.unpack('>'+_E*A,B[:A*2]),B[C*2:]
class List(ValueField):
	structcode=_A
	def __init__(A,name,type,pad=1):ValueField.__init__(A,name);A.type=type;A.pad=pad
	def parse_binary_value(B,data,display,length,format):
		I=length;H=display;A=data
		if I is _A:
			E=[]
			if B.type.structcode is _A:
				while A:K,A=B.type.parse_binary(A,H);E.append(K)
			else:
				G=_G+B.type.structcode;F=struct.calcsize(G);C=0
				while C+F<=len(A):
					D=struct.unpack(G,A[C:C+F])
					if B.type.structvalues==1:D=D[0]
					if B.type.parse_value is _A:E.append(D)
					else:E.append(B.type.parse_value(D,H))
					C=C+F
				A=A[C:]
		else:
			E=[_A]*int(I)
			if B.type.structcode is _A:
				for J in range(0,I):E[J],A=B.type.parse_binary(A,H)
			else:
				G=_G+B.type.structcode;F=struct.calcsize(G);C=0
				for J in range(0,I):
					D=struct.unpack(G,A[C:C+F])
					if B.type.structvalues==1:D=D[0]
					if B.type.parse_value is _A:E[J]=D
					else:E[J]=B.type.parse_value(D,H)
					C=C+F
				A=A[C:]
		if B.pad:A=A[len(A)%4:]
		return E,A
	def pack_value(B,val):
		C=val
		if B.type.structcode and len(B.type.structcode)==1:
			if B.type.check_value is not _A:C=[B.type.check_value(A)for A in C]
			D=array(struct_to_array_codes[B.type.structcode],C);A=encode_array(D)
		else:
			A=[]
			for E in C:A.append(B.type.pack_value(E))
			A=_D.join(A)
		if B.pad:F=len(A);A=A+_C*((4-F%4)%4)
		return A,len(C),_A
class FixedList(List):
	def __init__(A,name,size,type,pad=1):List.__init__(A,name,type,pad);A.size=size
	def parse_binary_value(A,data,display,length,format):return List.parse_binary_value(A,data,display,A.size,format)
	def pack_value(A,val):
		if len(val)!=A.size:raise BadDataError('length mismatch for FixedList %s'%A.name)
		return List.pack_value(A,val)
class Object(ValueField):
	def __init__(A,name,type,default=_A):ValueField.__init__(A,name,default);A.type=type;A.structcode=A.type.structcode;A.structvalues=A.type.structvalues
	def parse_binary_value(A,data,display,length,format):return A.type.parse_binary(data,display)
	def parse_value(A,val,display):return A.type.parse_value(val,display)
	def pack_value(A,val):return A.type.pack_value(val)
	def check_value(G,val):
		B=val
		if isinstance(B,tuple):
			C=[];E=0
			for A in G.type.fields:
				if A.name:
					if A.check_value is _A:D=B[E]
					else:D=A.check_value(B[E])
					if A.structvalues==1:C.append(D)
					else:C.extend(D)
					E=E+1
			return C
		if isinstance(B,dict):F=B
		elif isinstance(B,DictWrapper):F=B._data
		else:raise TypeError('Object value must be tuple, dictionary or DictWrapper: %s'%B)
		C=[]
		for A in G.type.fields:
			if A.name:
				if A.check_value is _A:D=F[A.name]
				else:D=A.check_value(F[A.name])
				if A.structvalues==1:C.append(D)
				else:C.extend(D)
		return C
class PropertyData(ValueField):
	structcode=_A
	def parse_binary_value(D,data,display,length,format):
		B=data;A=length
		if A is _A:A=len(B)//(format//8)
		else:A=int(A)
		if format==0:C=_A
		elif format==8:C=8,B[:A];B=B[A+(4-A%4)%4:]
		elif format==16:C=16,array(array_unsigned_codes[2],B[:2*A]);B=B[2*(A+A%2):]
		elif format==32:C=32,array(array_unsigned_codes[4],B[:4*A]);B=B[4*A:]
		return C,B
	def pack_value(I,value):
		D,A=value
		if D not in(8,16,32):raise BadDataError('Invalid property data format {0}'.format(D))
		if isinstance(A,binary_type):
			E=D//8;B=len(A)
			if B%E:B=B-B%E;C=A[:B]
			else:C=A
			F=B//E
		else:
			if isinstance(A,tuple):A=list(A)
			E=D//8;G=array(array_unsigned_codes[E],A);C=encode_array(G);F=len(A)
		H=len(C);C=C+_C*((4-H%4)%4);return C,F,D
class FixedPropertyData(PropertyData):
	def __init__(A,name,size):PropertyData.__init__(A,name);A.size=size
	def parse_binary_value(A,data,display,length,format):return PropertyData.parse_binary_value(A,data,display,A.size//(format//8),format)
	def pack_value(A,value):
		B=value;C,D,E=PropertyData.pack_value(A,B)
		if len(C)!=A.size:raise BadDataError('Wrong data length for FixedPropertyData: %s'%(B,))
		return C,D,E
class ValueList(Field):
	structcode=_A;keyword_args=1;default='usekeywords'
	def __init__(A,name,mask,pad,*D):
		A.name=name;A.maskcode='={0}{1}x'.format(unsigned_codes[mask],pad).encode();A.maskcodelen=struct.calcsize(A.maskcode);A.fields=[];B=1
		for C in D:
			if C.name:A.fields.append((C,B));B=B<<1
	def pack_value(C,arg,keys):
		B=arg;D=0;E=_D
		if B==C.default:B=keys
		for (A,H) in C.fields:
			if A.name in B:
				D=D|H;F=B[A.name]
				if A.check_value is not _A:F=A.check_value(F)
				G=struct.pack(_G+A.structcode,F);E=E+G+_C*(4-len(G))
		return struct.pack(C.maskcode,D)+E,_A,_A
	def parse_binary_value(D,data,display,length,format):
		E=display;A=data;F={};G=int(struct.unpack(D.maskcode,A[:D.maskcodelen])[0]);A=A[D.maskcodelen:]
		for (B,H) in D.fields:
			if G&H:
				if B.structcode:
					C=struct.unpack(_G+B.structcode,A[:struct.calcsize(_G+B.structcode)])
					if B.structvalues==1:C=C[0]
					if B.parse_value is not _A:C=B.parse_value(C,E)
				else:C,I=B.parse_binary_value(A[:4],E,_A,_A)
				F[B.name]=C;A=A[4:]
		return DictWrapper(F),A
class KeyboardMapping(ValueField):
	structcode=_A
	def parse_binary_value(G,data,display,length,format):
		C=length;A=data
		if C is _A:B=len(A)
		else:B=4*C*format
		D=array(array_unsigned_codes[4],bytes(A[:B]));E=[]
		for F in range(0,len(D),format):E.append(D[F:F+format])
		return E,A[B:]
	def pack_value(F,value):
		C=value;A=0
		for B in C:A=max(A,len(B))
		D=array(array_unsigned_codes[4])
		for B in C:
			for E in B:D.append(E)
			for G in range(len(B),A):D.append(X.NoSymbol)
		return encode_array(D),len(C),A
class ModifierMapping(ValueField):
	structcode=_A
	def parse_binary_value(D,data,display,length,format):
		C=array(array_unsigned_codes[1],data[:8*format]);A=[]
		for B in range(0,8):A.append(C[B*format:(B+1)*format])
		return A,data[8*format:]
	def pack_value(F,value):
		A=value
		if len(A)!=8:raise BadDataError('ModifierMapping list should have eight elements')
		B=0
		for C in A:B=max(B,len(C))
		D=array(array_unsigned_codes[1])
		for C in A:
			for E in C:D.append(E)
			for G in range(len(C),B):D.append(0)
		return encode_array(D),len(A),B
class EventField(ValueField):
	structcode=_A
	def pack_value(B,value):
		A=value
		if not isinstance(A,Event):raise BadDataError('%s is not an Event for field %s'%(A,B.name))
		return A._binary,_A,_A
	def parse_binary_value(D,data,display,length,format):
		C=display;A=data;from .  import event;B=C.event_classes.get(byte2int(A)&127,event.AnyEvent)
		if type(B)==dict:B=B[indexbytes(A,1)]
		return B(display=C,binarydata=A[:32]),A[32:]
class ScalarObj:
	def __init__(A,code):A.structcode=code;A.structvalues=1;A.parse_value=_A;A.check_value=_A
Card8Obj=ScalarObj(_B)
Card16Obj=ScalarObj(_E)
Card32Obj=ScalarObj(_F)
class ResourceObj:
	structcode=_F;structvalues=1
	def __init__(A,class_name):A.class_name=class_name;A.check_value=_A
	def parse_value(D,value,display):
		B=display;A=value;C=B.get_resource_class(D.class_name)
		if C:return C(B,A)
		else:return A
WindowObj=ResourceObj(_N)
ColormapObj=ResourceObj(_O)
class StrClass:
	structcode=_A
	def pack_value(A,val):return (chr(len(val))+val).encode()
	def parse_binary(C,data,display):A=data;B=byte2int(A)+1;return decode_string(A[1:B]),A[B:]
Str=StrClass()
class Struct:
	def __init__(A,*C):
		A.fields=C;A.static_codes=_G;A.static_values=0;A.static_fields=[];A.static_size=_A;A.var_fields=[]
		for B in A.fields:
			if B.structcode is not _A:
				assert not A.var_fields;A.static_codes=A.static_codes+B.structcode
				if B.structvalues>0:A.static_fields.append(B);A.static_values=A.static_values+B.structvalues
			else:A.var_fields.append(B)
		A.static_size=struct.calcsize(A.static_codes)
		if A.var_fields:A.structcode=_A;A.structvalues=0
		else:A.structcode=A.static_codes[1:];A.structvalues=A.static_values
	def to_binary(D,*M,**E):
		N=[A.name for A in D.fields if isinstance(A,ValueField)and A.name];B=dict(zip(N,M))
		if set(B).intersection(E):O=', '.join(set(B).intersection(E));raise TypeError('{0} arguments were passed both positionally and by keyword'.format(O))
		B.update(E)
		for A in D.fields:
			if A.name and A.name not in B:
				if A.default is _A:raise TypeError('Missing required argument {0}'.format(A.name))
				B[A.name]=A.default
		G=D.static_size;H={};I={};J={}
		for A in D.var_fields:
			if A.keyword_args:F,K,L=A.pack_value(B[A.name],E)
			else:F,K,L=A.pack_value(B[A.name])
			H[A.name]=F;I[A.name]=K;J[A.name]=L;G+=len(F)
		C=[]
		for A in D.static_fields:
			if isinstance(A,LengthField):
				if isinstance(A,TotalLengthField):C.append(A.calc_length(G))
				else:C.append(A.calc_length(I[A.name]))
			elif isinstance(A,FormatField):C.append(J[A.name])
			elif isinstance(A,ConstantField):C.append(A.value)
			elif A.structvalues==1:
				if A.check_value is not _A:C.append(A.check_value(B[A.name]))
				else:C.append(B[A.name])
			elif A.check_value is not _A:C.extend(A.check_value(B[A.name]))
			else:C.extend(B[A.name])
		P=struct.pack(D.static_codes,*C);Q=[H[A.name]for A in D.var_fields];return P+_D.join(Q)
	def pack_value(B,value):
		A=value
		if type(A)is tuple:return B.to_binary(*A)
		elif isinstance(A,dict):return B.to_binary(**A)
		elif isinstance(A,DictWrapper):return B.to_binary(**A._data)
		else:raise BadDataError('%s is not a tuple or a list'%A)
	def parse_value(F,val,display,rawdict=0):
		E=rawdict;D={};B=0
		for A in F.static_fields:
			if not A.name:0
			elif isinstance(A,LengthField):0
			elif isinstance(A,FormatField):0
			else:
				if A.structvalues==1:C=val[B]
				else:C=val[B:B+A.structvalues]
				if A.parse_value is not _A:C=A.parse_value(C,display,rawdict=E)
				D[A.name]=C
			B=B+A.structvalues
		if not E:return DictWrapper(D)
		return D
	def parse_binary(E,data,display,rawdict=0):
		H=display;D=data;F={};G=struct.unpack(E.static_codes,D[:E.static_size]);I={};J={};C=0
		for A in E.static_fields:
			if not A.name:0
			elif isinstance(A,LengthField):
				K=[A.name]
				if A.other_fields:K.extend(A.other_fields)
				B=G[C]
				if A.parse_value is not _A:B=A.parse_value(B,H)
				for L in K:I[L]=B
			elif isinstance(A,FormatField):J[A.name]=G[C]
			else:
				if A.structvalues==1:B=G[C]
				else:B=G[C:C+A.structvalues]
				if A.parse_value is not _A:B=A.parse_value(B,H)
				F[A.name]=B
			C=C+A.structvalues
		D=D[E.static_size:]
		for A in E.var_fields:F[A.name],D=A.parse_binary_value(D,H,I.get(A.name),J.get(A.name))
		if not rawdict:F=DictWrapper(F)
		return F,D
class TextElements8(ValueField):
	string_textitem=Struct(LengthOf(_H,1),Int8(_J),String8(_H,pad=0))
	def pack_value(F,value):
		B=_D;E={}
		for A in value:
			if type(A)in(str,bytes):A=0,A
			if isinstance(A,(tuple,dict,DictWrapper)):
				if isinstance(A,tuple):D,C=A
				else:D=A[_J];C=A[_H]
				while D or C:E[_J]=D;E[_H]=C[:254];B=B+F.string_textitem.to_binary(*(),**E);D=0;C=C[254:]
			else:
				if isinstance(A,Fontable):A=A.__fontable__()
				B=B+struct.pack('>BL',255,A)
		G=len(B);return B+_C*((4-G%4)%4),_A,_A
	def parse_binary_value(C,data,display,length,format):
		A=data;B=[]
		while 1:
			if len(A)<2:break
			if byte2int(A)==255:B.append(struct.unpack('>L',bytes(A[1:5]))[0]);A=A[5:]
			elif byte2int(A)==0 and indexbytes(A,1)==0:A=A[2:]
			else:D,A=C.string_textitem.parse_binary(A,display);B.append(D)
		return B,''
class TextElements16(TextElements8):string_textitem=Struct(LengthOf(_H,1),Int8(_J),String16(_H,pad=0))
class GetAttrData:
	def __getattr__(B,attr):
		A=attr
		try:
			if B._data:return B._data[A]
			else:raise AttributeError(A)
		except KeyError:raise AttributeError(A)
class DictWrapper(GetAttrData):
	def __init__(A,dict):A.__dict__['_data']=dict
	def __getitem__(A,key):return A._data[key]
	def __setitem__(A,key,value):A._data[key]=value
	def __delitem__(A,key):del A._data[key]
	def __setattr__(A,key,value):A._data[key]=value
	def __delattr__(A,key):del A._data[key]
	def __str__(A):return str(A._data)
	def __repr__(A):return _P%(A.__class__,repr(A._data))
	def __lt__(B,other):
		A=other
		if isinstance(A,DictWrapper):return B._data<A._data
		else:return B._data<A
	def __gt__(B,other):
		A=other
		if isinstance(A,DictWrapper):return B._data>A._data
		else:return B._data>A
	def __eq__(B,other):
		A=other
		if isinstance(A,DictWrapper):return B._data==A._data
		else:return B._data==A
class Request:
	def __init__(A,display,onerror=_A,*C,**D):B=onerror;A._errorhandler=B;A._binary=A._request.to_binary(*C,**D);A._serial=_A;display.send_request(A,B is not _A)
	def _set_error(A,error):
		if A._errorhandler is not _A:return call_error_handler(A._errorhandler,error,A)
		else:return 0
class ReplyRequest(GetAttrData):
	def __init__(A,display,defer=0,*B,**C):
		A._display=display;A._binary=A._request.to_binary(*B,**C);A._serial=_A;A._data=_A;A._error=_A;A._response_lock=lock.allocate_lock();A._display.send_request(A,1)
		if not defer:A.reply()
	def reply(A):
		A._response_lock.acquire()
		while A._data is _A and A._error is _A:A._display.send_recv_lock.acquire();A._response_lock.release();A._display.send_and_recv(request=A._serial);A._response_lock.acquire()
		A._response_lock.release();A._display=_A
		if A._error:raise A._error
	def _parse_response(A,data):A._response_lock.acquire();A._data,B=A._reply.parse_binary(data,A._display,rawdict=1);A._response_lock.release()
	def _set_error(A,error):A._response_lock.acquire();A._error=error;A._response_lock.release();return 1
	def __repr__(A):return'<%s serial = %s, data = %s, error = %s>'%(A.__class__,A._serial,A._data,A._error)
class Event(GetAttrData):
	def __init__(A,binarydata=_A,display=_A,**B):
		C=binarydata
		if C:A._binary=C;A._data,D=A._fields.parse_binary(C,display,rawdict=1);A._data[_K]=not(not A._data[_I]&128);A._data[_I]=A._data[_I]&127
		else:
			if A._code:B[_I]=A._code
			B['sequence_number']=0;A._binary=A._fields.to_binary(**B);B[_K]=0;A._data=B
	def __repr__(A):
		D=[]
		for (B,C) in A._data.items():
			if B==_K:continue
			if B==_I and A._data[_K]:C=C|128
			D.append('%s = %s'%(B,repr(C)))
		E=', '.join(D);return _P%(A.__class__,E)
	def __lt__(B,other):
		A=other
		if isinstance(A,Event):return B._data<A._data
		else:return B._data<A
	def __gt__(B,other):
		A=other
		if isinstance(A,Event):return B._data>A._data
		else:return B._data>A
	def __eq__(B,other):
		A=other
		if isinstance(A,Event):return B._data==A._data
		else:return B._data==A
def call_error_handler(handler,error,request):
	try:return handler(error,request)
	except:sys.stderr.write('Exception raised by error handler.\n');traceback.print_exc();return 0
