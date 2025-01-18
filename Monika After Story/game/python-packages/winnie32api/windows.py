# pylint: disable=attribute-defined-outside-init
# pylint: disable=invalid-name
from __future__ import annotations

__all__ = (
    "get_hwnd_by_title",
    "get_window_title",
    "get_window_rect",
    "flash_window",
    "unflash_window",
    "set_active_window",
    "get_active_window_hwnd",
    "get_active_window_title",
    "get_active_window_rect"
)

import ctypes
import ctypes.wintypes as wt

from .common import (
    Rect,
    Pack,
    _get_last_err,
    _reset_last_err
)
from .errors import WinAPIError


user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


WNDENUMPROC = ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)


class FlashWInfo(ctypes.Structure):
    _fields_ = [
        ("cbSize", wt.UINT),
        ("hwnd", wt.HWND),
        ("dwFlags", wt.DWORD),
        ("uCount", wt.UINT),
        ("dwTimeout", wt.DWORD)
    ]

class FLASHW():
    """
    0x00000003. Flash both the window caption and taskbar button.
    0x00000001. Flash the window caption.
    0. Stop flashing. The system restores the window to its original state.
    0x00000004. Flash continuously, until the FLASHW_STOP flag is set.
    0x0000000C. Flash continuously until the window comes to the foreground.
    0x00000002. Flash the taskbar button.
    """
    ALL = 0x00000003
    CAPTION = 0x00000001
    STOP = 0
    TIMER = 0x00000004
    TIMERNOFG = 0x0000000C
    TRAY = 0x00000002


user32.IsWindowVisible.argtypes = (wt.HWND,)
user32.IsWindowVisible.restype = wt.BOOL

user32.GetWindowTextLengthW.argtypes = (wt.HWND,)
user32.GetWindowTextLengthW.restype = wt.INT

user32.GetWindowTextW.argtypes = (wt.HWND, wt.LPWSTR, wt.INT)
user32.GetWindowTextW.restype = wt.INT

user32.EnumWindows.argtypes = (WNDENUMPROC, wt.LPARAM)
user32.EnumWindows.restype = wt.BOOL

user32.GetWindowRect.argtypes = (wt.HWND, wt.LPRECT)
user32.GetWindowRect.restype = wt.BOOL

user32.FlashWindowEx.argtypes = (ctypes.POINTER(FlashWInfo),)
user32.FlashWindowEx.restype = wt.BOOL

user32.GetForegroundWindow.argtypes = ()
user32.GetForegroundWindow.restype = wt.HWND


def get_hwnd_by_title(title: str) -> int|None:
    """
    Returns first window hwnd with the given title
    """
    pack = Pack(None)

    def callback(hwnd: int, lparam: int) -> bool:
        c_hwnd = wt.HWND(hwnd)

        if user32.IsWindowVisible(c_hwnd):
            rv = get_window_title(hwnd)
            if title == rv:
                pack.value = hwnd
                return False

        return True

    user32.EnumWindows(WNDENUMPROC(callback), wt.LPARAM(0))
    return pack.value

def get_window_title(hwnd: int) -> str:
    """
    Returns a window title as a str
    """
    _reset_last_err()

    title_len = user32.GetWindowTextLengthW(hwnd)
    if not title_len:
        last_err = _get_last_err()
        if last_err:
            raise WinAPIError("failed to get title length", last_err)

    buffer = ctypes.create_unicode_buffer(title_len + 1)
    result = user32.GetWindowTextW(
        hwnd,
        buffer,
        title_len + 1
    )
    if result != title_len:
        last_err = _get_last_err()
        if last_err:
            raise WinAPIError("failed to get title", last_err)

    return buffer.value

def get_window_rect(hwnd: int) -> Rect:
    """
    Returns a window rect
    """
    c_rect = wt.RECT()
    result = user32.GetWindowRect(hwnd, ctypes.byref(c_rect))
    if not result:
        raise WinAPIError("failed to get window rect", _get_last_err())

    return Rect.from_coords(c_rect.left, c_rect.top, c_rect.right, c_rect.bottom)# type: ignore


def flash_window(
    hwnd: int,
    count: int|None = 1,
    caption: bool = True,
    tray: bool = True
):
    """
    Flashes a window

    IN:
        hwnd - the window hwnd
        coutn - the number of flashes
            -1 means flash infinitely until asked to stop
            None means flash infinitely until the window becomes focused
        caption - do we flash window caption
        tray - do weflash tray icon
    """
    flash_info = FlashWInfo()
    flash_info.cbSize = ctypes.sizeof(flash_info)
    flash_info.hwnd = hwnd

    flags = 0
    if caption:
        flags |= FLASHW.CAPTION
    if tray:
        flags |= FLASHW.TRAY
    if count is None:
        flags |= FLASHW.TIMERNOFG
        count = 0
    elif count == -1:
        flags |= FLASHW.TIMER
        count = 0

    flash_info.dwFlags = flags
    flash_info.uCount = count
    flash_info.dwTimeout = 0

    user32.FlashWindowEx(ctypes.byref(flash_info))

def unflash_window(hwnd: int):
    """
    Stops window flashing
    """
    flash_info = FlashWInfo()
    flash_info.cbSize = ctypes.sizeof(flash_info)
    flash_info.hwnd = hwnd
    flash_info.dwFlags = FLASHW.STOP
    flash_info.uCount = 0
    flash_info.dwTimeout = 0
    user32.FlashWindowEx(ctypes.byref(flash_info))


def set_active_window(hwnd: int):
    """
    Sets focus to a new window
    NOTE:
        A process may or may not allow to change "foreground" window
            to other processes
        It's impossible to "activate" a window from another process
    """
    # Also tried:
    # - linking threads, no result
    # - emulating input, no result
    user32.SetFocus(hwnd)# err 5
    user32.BringWindowToTop(hwnd)# no err, but no result
    user32.SetForegroundWindow(hwnd)# err 1400
    # user32.SetActiveWindow(hwnd)# err 1400


def get_active_window_hwnd() -> int|None:
    """
    Returns active window title hwnd (id)
    """
    active_win_hwnd = user32.GetForegroundWindow()
    if not active_win_hwnd or not user32.IsWindowVisible(active_win_hwnd):
        return None

    return active_win_hwnd

def get_active_window_title() -> str|None:
    """
    Returns active window title as a str
    """
    hwnd = get_active_window_hwnd()
    if hwnd is None:
        return None

    return get_window_title(hwnd)

def get_active_window_rect() -> Rect|None:
    """
    Returns active window rect
    """
    hwnd = get_active_window_hwnd()
    if hwnd is None:
        return None

    return get_window_rect(hwnd)
