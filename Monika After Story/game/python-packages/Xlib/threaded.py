from six.moves import _thread
from Xlib.support import lock
lock.allocate_lock=_thread.allocate_lock