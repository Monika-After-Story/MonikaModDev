import ctypes
import ctypes.wintypes as wt

from typing import (
    Optional
)

from .common import (
    HWND,
    Rect,
    Pack,
    WinAPIError,
    _get_last_err,
    _reset_last_err
)


user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


WNDENUMPROC = ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)


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

user32.GetForegroundWindow.argtypes = ()
user32.GetForegroundWindow.restype = wt.HWND


def get_hwnd_by_title(title: str) -> Optional[HWND]:
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

def get_window_title(hwnd: HWND) -> str:
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

def get_window_rect(hwnd: HWND) -> Rect:
    """
    Returns a window rect
    """
    c_rect = wt.RECT()
    result = user32.GetWindowRect(hwnd, ctypes.byref(c_rect))
    if not result:
        raise WinAPIError("failed to get window rect", _get_last_err())

    return Rect.from_coords(c_rect.left, c_rect.top, c_rect.right, c_rect.bottom)


def get_active_window_hwnd() -> Optional[HWND]:
    """
    Returns active window title hwnd (id)
    """
    active_win_hwnd = user32.GetForegroundWindow()
    if not active_win_hwnd or not user32.IsWindowVisible(active_win_hwnd):
        return None

    return active_win_hwnd

def get_active_window_title() -> Optional[str]:
    """
    Returns active window title as a str
    """
    hwnd = get_active_window_hwnd()
    if hwnd is None:
        return None

    return get_window_title(hwnd)

def get_active_window_rect() -> Optional[Rect]:
    """
    Returns active window rect
    """
    hwnd = get_active_window_hwnd()
    if hwnd is None:
        return None

    return get_window_rect(hwnd)
