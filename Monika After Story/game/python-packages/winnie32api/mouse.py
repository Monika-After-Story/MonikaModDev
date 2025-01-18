__all__ = (
    "get_screen_mouse_pos",
)

import ctypes
import ctypes.wintypes as wt

from .common import Point, _get_last_err
from .errors import WinAPIError


user32 = ctypes.windll.user32


user32.GetCursorPos.argtypes = (wt.LPPOINT,)
user32.GetCursorPos.restype = wt.BOOL


def get_screen_mouse_pos() -> Point:
    """
    Returns mouse position in screen coords
    """
    c_point = wt.POINT()
    result = user32.GetCursorPos(ctypes.byref(c_point))
    if not result:
        raise WinAPIError("failed to get mouse position", _get_last_err())

    return Point(c_point.x, c_point.y)# type: ignore
