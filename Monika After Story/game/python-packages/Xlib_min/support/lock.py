class _DummyLock(object):
	def __init__(A):A.acquire=A.release=A.locked=A.__noop
	def __noop(B,*A):return
_dummy_lock=_DummyLock()
def allocate_lock():return _dummy_lock