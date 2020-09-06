_N='vendor'
_M='auth_prot_name'
_L='visuals'
_K='protocol_major'
_J='status'
_I='additional_length'
_H='auth_prot_data'
_G='reason_length'
_F='pixmap_formats'
_E='depth'
_D='allowed_depths'
_C='roots'
_B='unsupported type: {}'
_A='protocol_minor'
import errno,math,select,socket,struct,sys
from six import PY3,byte2int,indexbytes
from ..  import error
from ..ext import ge
from ..support import lock,connect
from .  import rq
from .  import event
if PY3:
	class bytesview(object):
		def __init__(E,data,offset=0,size=None):
			C=size;B=offset;A=data
			if C is None:C=len(A)-B
			if isinstance(A,bytes):D=memoryview(A)
			elif isinstance(A,bytesview):D=A.view
			else:raise TypeError(_B.format(type(A)))
			E.view=D[B:B+C]
		def __len__(A):return len(A.view)
		def __getitem__(B,key):
			A=key
			if isinstance(A,slice):return bytes(B.view[A])
			return B.view[A]
else:
	def bytesview(data,offset=0,size=None):
		C=offset;B=size;A=data
		if not isinstance(A,(bytes,buffer)):raise TypeError(_B.format(type(A)))
		if B is None:B=len(A)-C
		return buffer(A,C,B)
class Display(object):
	extension_major_opcodes={};error_classes=error.xerror_class.copy();event_classes=event.event_class.copy()
	def __init__(A,display=None):
		B,E,F,G,I=connect.get_display(display);A.display_name=B;A.default_screen=I;A.socket=connect.get_socket(B,E,F,G);J,K=connect.get_auth(A.socket,B,E,F,G);A.socket_error_lock=lock.allocate_lock();A.socket_error=None;A.event_queue_read_lock=lock.allocate_lock();A.event_queue_write_lock=lock.allocate_lock();A.event_queue=[];A.request_queue_lock=lock.allocate_lock();A.request_serial=1;A.request_queue=[];A.send_recv_lock=lock.allocate_lock();A.send_active=0;A.recv_active=0;A.event_waiting=0;A.event_wait_lock=lock.allocate_lock();A.request_waiting=0;A.request_wait_lock=lock.allocate_lock();C=A.socket.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF);C=math.pow(2,math.floor(math.log(C,2)));A.recv_buffer_size=int(C);A.sent_requests=[];A.recv_packet_len=0;A.data_send='';A.data_recv='';A.data_sent_bytes=0;A.resource_id_lock=lock.allocate_lock();A.resource_ids={};A.last_resource_id=0;A.error_handler=None;A.big_endian=struct.unpack('BB',struct.pack('H',256))[0]
		if A.big_endian:H=66
		else:H=108
		D=ConnectionSetupRequest(A,byte_order=H,protocol_major=11,protocol_minor=0,auth_prot_name=J,auth_prot_data=K)
		if D.status!=1:raise error.DisplayConnectionError(A.display_name,D.reason)
		A.info=D;A.default_screen=min(A.default_screen,len(A.info.roots)-1)
	def get_display_name(A):return A.display_name
	def get_default_screen(A):return A.default_screen
	def fileno(A):A.check_for_error();return A.socket.fileno()
	def next_event(A):
		A.check_for_error();A.event_queue_read_lock.acquire();A.event_queue_write_lock.acquire()
		while not A.event_queue:A.send_recv_lock.acquire();A.event_queue_write_lock.release();A.send_and_recv(event=1);A.event_queue_write_lock.acquire()
		B=A.event_queue[0];del A.event_queue[0];A.event_queue_write_lock.release();A.event_queue_read_lock.release();return B
	def pending_events(A):A.check_for_error();A.send_recv_lock.acquire();A.send_and_recv(recv=1);A.event_queue_write_lock.acquire();B=len(A.event_queue);A.event_queue_write_lock.release();return B
	def flush(A):A.check_for_error();A.send_recv_lock.acquire();A.send_and_recv(flush=1)
	def close(A):A.flush();A.close_internal('client')
	def set_error_handler(A,handler):A.error_handler=handler
	def allocate_resource_id(A):
		'id = d.allocate_resource_id()\n\n        Allocate a new X resource id number ID.\n\n        Raises ResourceIDError if there are no free resource ids.\n        ';A.resource_id_lock.acquire()
		try:
			B=A.last_resource_id
			while B in A.resource_ids:
				B=B+1
				if B>A.info.resource_id_mask:B=0
				if B==A.last_resource_id:raise error.ResourceIDError('out of resource ids')
			A.resource_ids[B]=None;A.last_resource_id=B;return A.info.resource_id_base|B
		finally:A.resource_id_lock.release()
	def free_resource_id(A,rid):
		"d.free_resource_id(rid)\n\n        Free resource id RID.  Attempts to free a resource id which\n        isn't allocated by us are ignored.\n        ";A.resource_id_lock.acquire()
		try:
			B=rid&A.info.resource_id_mask
			if rid-B!=A.info.resource_id_base:return None
			try:del A.resource_ids[B]
			except KeyError:pass
		finally:A.resource_id_lock.release()
	def get_resource_class(A,class_name,default=None):'class = d.get_resource_class(class_name, default = None)\n\n        Return the class to be used for X resource objects of type\n        CLASS_NAME, or DEFAULT if no such class is set.\n        ';return A.resource_classes.get(class_name,default)
	def set_extension_major(A,extname,major):A.extension_major_opcodes[extname]=major
	def get_extension_major(A,extname):return A.extension_major_opcodes[extname]
	def add_extension_event(A,code,evt,subcode=None):
		D=subcode;C=evt;B=code
		if D==None:A.event_classes[B]=C
		elif not B in A.event_classes:A.event_classes[B]={D:C}
		else:A.event_classes[B][D]=C
	def add_extension_error(A,code,err):A.error_classes[code]=err
	def check_for_error(A):
		A.socket_error_lock.acquire();B=A.socket_error;A.socket_error_lock.release()
		if B:raise B
	def send_request(A,request,wait_for_response):
		B=request
		if A.socket_error:raise A.socket_error
		A.request_queue_lock.acquire();B._serial=A.request_serial;A.request_serial=(A.request_serial+1)%65536;A.request_queue.append((B,wait_for_response));C=len(A.request_queue);A.request_queue_lock.release()
	def close_internal(A,whom):A.request_queue=None;A.sent_requests=None;A.event_queue=None;A.data_send=None;A.data_recv=None;A.socket.close();A.socket_error_lock.acquire();A.socket_error=error.ConnectionClosedError(whom);A.socket_error_lock.release()
	def send_and_recv(A,flush=None,event=None,request=None,recv=None):
		"send_and_recv(flush = None, event = None, request = None, recv = None)\n\n        Perform I/O, or wait for some other thread to do it for us.\n\n        send_recv_lock MUST be LOCKED when send_and_recv is called.\n        It will be UNLOCKED at return.\n\n        Exactly or one of the parameters flush, event, request and recv must\n        be set to control the return condition.\n\n        To attempt to send all requests in the queue, flush should\n        be true.  Will return immediately if another thread is\n        already doing send_and_recv.\n\n        To wait for an event to be received, event should be true.\n\n        To wait for a response to a certain request (either an error\n        or a response), request should be set the that request's\n        serial number.\n\n        To just read any pending data from the server, recv should be true.\n\n        It is not guaranteed that the return condition has been\n        fulfilled when the function returns, so the caller has to loop\n        until it is finished.\n        ";V='server: %s';I=event;G=recv;F=request;D=flush
		if(D or F is not None)and A.send_active or(I or G)and A.recv_active:
			if I:
				E=A.event_wait_lock
				if not A.event_waiting:A.event_waiting=1;E.acquire()
			elif F is not None:
				E=A.request_wait_lock
				if not A.request_waiting:A.request_waiting=1;E.acquire()
			A.send_recv_lock.release()
			if D or G:return
			E.acquire();E.release();return
		if not A.recv_active:H=1;A.recv_active=1
		else:H=0
		J=None;C=0
		while 1:
			if C or not A.send_active:
				A.request_queue_lock.acquire()
				for (L,S) in A.request_queue:
					A.data_send=A.data_send+L._binary
					if S:A.sent_requests.append(L)
				del A.request_queue[:];A.request_queue_lock.release()
				if A.data_send:A.send_active=1;C=1
				else:A.send_active=0;C=0
			A.send_recv_lock.release()
			if not(C or H):break
			if D and J is None:J=A.data_sent_bytes+len(A.data_send)
			try:
				if C:M=[A.socket]
				else:M=[]
				if G or D:N=0
				else:N=None
				T,U,W=select.select([A.socket],M,[],N)
			except select.error as B:
				if isinstance(B,OSError):O=B.errno
				else:O=B[0]
				if O!=errno.EINTR:raise
				A.send_recv_lock.acquire();continue
			if U:
				try:P=A.socket.send(A.data_send)
				except socket.error as B:A.close_internal(V%B);raise A.socket_error
				A.data_send=A.data_send[P:];A.data_sent_bytes=A.data_sent_bytes+P
			Q=0
			if T:
				if H:
					try:K=A.recv_packet_len-len(A.data_recv);K=max(A.recv_buffer_size,K);R=A.socket.recv(K)
					except socket.error as B:A.close_internal(V%B);raise A.socket_error
					if not R:A.close_internal('server');raise A.socket_error
					A.data_recv=bytes(A.data_recv)+R;Q=A.parse_response(F)
				else:A.send_recv_lock.acquire();A.send_active=0;A.send_recv_lock.release();return
			if D and J>=A.data_sent_bytes:break
			if I and A.event_queue:break
			if F is not None and Q:break
			if G:break
			A.send_recv_lock.acquire()
		A.send_recv_lock.acquire()
		if C:A.send_active=0
		if H:A.recv_active=0
		if A.event_waiting:A.event_waiting=0;A.event_wait_lock.release()
		if A.request_waiting:A.request_waiting=0;A.request_wait_lock.release()
		A.send_recv_lock.release()
	def parse_response(A,request):
		"Internal method.\n\n        Parse data received from server.  If REQUEST is not None\n        true is returned if the request with that serial number\n        was received, otherwise false is returned.\n\n        If REQUEST is -1, we're parsing the server connection setup\n        response.\n        ";D=request
		if D==-1:return A.parse_connection_setup()
		C=0
		while 1:
			if A.data_recv:B=byte2int(A.data_recv)
			if A.recv_packet_len:
				if len(A.data_recv)<A.recv_packet_len:return C
				if B==1:C=A.parse_request_response(D)or C;continue
				elif B&127==ge.GenericEventCode:A.parse_event_response(B);continue
				else:raise AssertionError(B)
			if len(A.data_recv)<32:return C
			if B==0:C=A.parse_error_response(D)or C
			elif B==1 or B&127==ge.GenericEventCode:E=int(struct.unpack('=L',A.data_recv[4:8])[0]);A.recv_packet_len=32+E*4
			else:A.parse_event_response(B)
	def parse_error_response(A,request):
		D=indexbytes(A.data_recv,1);E=A.error_classes.get(D,error.XError);B=E(A,A.data_recv[:32]);A.data_recv=bytesview(A.data_recv,32);C=A.get_waiting_request(B.sequence_number)
		if C and C._set_error(B):
			if isinstance(C,rq.ReplyRequest):
				A.send_recv_lock.acquire()
				if A.request_waiting:A.request_waiting=0;A.request_wait_lock.release()
				A.send_recv_lock.release()
			return request==B.sequence_number
		else:
			if A.error_handler:rq.call_error_handler(A.error_handler,B,None)
			else:A.default_error_handler(B)
			return 0
	def default_error_handler(A,err):sys.stderr.write('X protocol error:\n%s\n'%err)
	def parse_request_response(A,request):
		B=A.get_waiting_replyrequest();C=struct.unpack('=H',A.data_recv[2:4])[0]
		if C!=B._serial:raise RuntimeError("Expected reply for request %s, but got %s.  Can't happen!"%(B._serial,C))
		B._parse_response(A.data_recv[:A.recv_packet_len]);A.data_recv=bytesview(A.data_recv,A.recv_packet_len);A.recv_packet_len=0;A.send_recv_lock.acquire()
		if A.request_waiting:A.request_waiting=0;A.request_wait_lock.release()
		A.send_recv_lock.release();return B.sequence_number==request
	def parse_event_response(A,etype):
		B=etype;B=B&127
		if B==ge.GenericEventCode:E=A.recv_packet_len
		else:E=32
		C=A.event_classes.get(B,event.AnyEvent)
		if type(C)==dict:
			D=A.data_recv[1]
			if type(D)==str:D=ord(D)
			C=C[D]
		F=C(display=A,binarydata=A.data_recv[:E])
		if B==ge.GenericEventCode:A.recv_packet_len=0
		A.data_recv=bytesview(A.data_recv,E)
		if hasattr(F,'sequence_number'):A.get_waiting_request((F.sequence_number-1)%65536)
		A.event_queue_write_lock.acquire();A.event_queue.append(F);A.event_queue_write_lock.release();A.send_recv_lock.acquire()
		if A.event_waiting:A.event_waiting=0;A.event_wait_lock.release()
		A.send_recv_lock.release()
	def get_waiting_request(A,sno):
		B=sno
		if not A.sent_requests:return None
		if A.sent_requests[0]._serial>A.request_serial:
			I=A.request_serial+65536
			if B<A.request_serial:B=B+65536
		else:
			I=A.request_serial
			if B>A.request_serial:B=B-65536
		if B<A.sent_requests[0]._serial:return None
		E=None;F=len(A.sent_requests);G=0;H=0
		for D in range(0,len(A.sent_requests)):
			C=A.sent_requests[D]._serial+G
			if C<H:G=65536;C=C+G
			H=C
			if B==C:E=A.sent_requests[D];F=D+1;break
			elif B<C:E=None;F=D;break
		del A.sent_requests[:F];return E
	def get_waiting_replyrequest(A):
		for B in range(0,len(A.sent_requests)):
			if hasattr(A.sent_requests[B],'_reply'):C=A.sent_requests[B];del A.sent_requests[:B+1];return C
		else:raise RuntimeError("Request reply to unknown request.  Can't happen!")
	def parse_connection_setup(A):
		'Internal function used to parse connection setup response.\n        ';B=A.sent_requests[0]
		while 1:
			if B._data:
				C=B._data[_I]*4
				if len(A.data_recv)<C:return 0
				if B._data[_J]!=1:B._data['reason']=A.data_recv[:B._data[_G]]
				else:D,E=B._success_reply.parse_binary(A.data_recv[:C],A,rawdict=1);B._data.update(D)
				del A.sent_requests[0];A.data_recv=A.data_recv[C:];return 1
			else:
				if len(A.data_recv)<8:return 0
				B._data,E=B._reply.parse_binary(A.data_recv[:8],A,rawdict=1);A.data_recv=A.data_recv[8:]
PixmapFormat=rq.Struct(rq.Card8(_E),rq.Card8('bits_per_pixel'),rq.Card8('scanline_pad'),rq.Pad(5))
VisualType=rq.Struct(rq.Card32('visual_id'),rq.Card8('visual_class'),rq.Card8('bits_per_rgb_value'),rq.Card16('colormap_entries'),rq.Card32('red_mask'),rq.Card32('green_mask'),rq.Card32('blue_mask'),rq.Pad(4))
Depth=rq.Struct(rq.Card8(_E),rq.Pad(1),rq.LengthOf(_L,2),rq.Pad(4),rq.List(_L,VisualType))
Screen=rq.Struct(rq.Window('root'),rq.Colormap('default_colormap'),rq.Card32('white_pixel'),rq.Card32('black_pixel'),rq.Card32('current_input_mask'),rq.Card16('width_in_pixels'),rq.Card16('height_in_pixels'),rq.Card16('width_in_mms'),rq.Card16('height_in_mms'),rq.Card16('min_installed_maps'),rq.Card16('max_installed_maps'),rq.Card32('root_visual'),rq.Card8('backing_store'),rq.Card8('save_unders'),rq.Card8('root_depth'),rq.LengthOf(_D,1),rq.List(_D,Depth))
class ConnectionSetupRequest(rq.GetAttrData):
	_request=rq.Struct(rq.Set('byte_order',1,(66,108)),rq.Pad(1),rq.Card16(_K),rq.Card16(_A),rq.LengthOf(_M,2),rq.LengthOf(_H,2),rq.Pad(2),rq.String8(_M),rq.String8(_H));_reply=rq.Struct(rq.Card8(_J),rq.Card8(_G),rq.Card16(_K),rq.Card16(_A),rq.Card16(_I));_success_reply=rq.Struct(rq.Card32('release_number'),rq.Card32('resource_id_base'),rq.Card32('resource_id_mask'),rq.Card32('motion_buffer_size'),rq.LengthOf(_N,2),rq.Card16('max_request_length'),rq.LengthOf(_C,1),rq.LengthOf(_F,1),rq.Card8('image_byte_order'),rq.Card8('bitmap_format_bit_order'),rq.Card8('bitmap_format_scanline_unit'),rq.Card8('bitmap_format_scanline_pad'),rq.Card8('min_keycode'),rq.Card8('max_keycode'),rq.Pad(4),rq.String8(_N),rq.List(_F,PixmapFormat),rq.List(_C,Screen))
	def __init__(A,display,*C,**D):B=display;A._binary=A._request.to_binary(*C,**D);A._data=None;B.request_queue.append((A,1));B.send_recv_lock.acquire();B.send_and_recv(request=-1)