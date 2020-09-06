from Xlib.protocol import request
class Resource(object):
	def __init__(A,display,rid,owner=0):A.display=display;A.id=rid;A.owner=owner
	def __resource__(A):return A.id
	def __eq__(B,obj):
		A=obj
		if isinstance(A,Resource):
			if B.display==A.display:return B.id==A.id
			else:return False
		else:return id(B)==id(A)
	def __ne__(A,obj):return not A==obj
	def __hash__(A):return int(A.id)
	def __str__(A):return'%s(0x%08x)'%(A.__class__,A.id)
	def __repr__(A):return'<%s 0x%08x>'%(A.__class__,A.id)
	def kill_client(A,onerror=None):request.KillClient(display=A.display,onerror=onerror,resource=A.id)