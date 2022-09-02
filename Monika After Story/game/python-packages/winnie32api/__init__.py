"""
winnie32api - minimalistic Windows API

Provides a small number of utils, allowing to not include big dependencies like pywin32/win32api
"""

from __future__ import annotations

__title__ = "winnie32api"
__author__ = "Booplicate"
__version__ = "0.0.4"

import ctypes

from .mouse import (
    get_screen_mouse_pos
)
from .windows import (
    get_hwnd_by_title,
    get_window_title,
    get_window_rect,
    flash_window,
    unflash_window,
    get_active_window_hwnd,
    get_active_window_title,
    get_active_window_rect
)

from .notifs import WindowsNotifManager, WindowsNotif
