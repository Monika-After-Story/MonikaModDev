# pylint: disable=attribute-defined-outside-init
# pylint: disable=invalid-name
from __future__ import annotations

__all__ = (
    "NotifManager",
)

import ctypes
import ctypes.wintypes as wt
import weakref
import threading
import atexit
from collections.abc import Callable

from .common import _get_last_err
from .errors import WinAPIError, ManagerAlreadyExistsError


user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
shell32 = ctypes.windll.shell32


APP_ID = 922


# This is missing from wintypes
LRESULT = wt.LPARAM#ctypes.c_long
# This has undocumented value, but seems to work
CW_USEDEFAULT = -2147483648
# There's literally only one place on the internet where it says the value is -3
# and it's not microsoft docs. At least it seems to work...
HWND_MESSAGE = -3
# Undocumented, but probably is correct
NOTIFYICON_VERSION_4 = 4
# The base value of user-defined msgs
WM_USER = 0x0400


WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM)

class NotifyIconDataW(ctypes.Structure):
    """
    Docs: https://docs.microsoft.com/en-us/windows/win32/api/shellapi/ns-shellapi-notifyicondataw#syntax
    """
    _fields_ = [
        ("cbSize", wt.DWORD),
        ("hWnd", wt.HWND),
        ("uID", wt.UINT),
        ("uFlags", wt.UINT),
        ("uCallbackMessage", wt.UINT),
        ("hIcon", wt.HICON),
        ("szTip", wt.WCHAR * 128),
        ("dwState", wt.DWORD),
        ("dwStateMask", wt.DWORD),
        ("szInfo", wt.WCHAR * 256),
        ("uVersion", wt.UINT),
        ("szInfoTitle", wt.WCHAR * 64),
        ("dwInfoFlags", wt.DWORD),
        ("guidItem", ctypes.c_char * 16),
        ("hBalloonIcon", wt.HICON)
    ]

class WndClassExw(ctypes.Structure):
    """
    Docs: https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-wndclassexw#syntax
    """
    _fields_ = [
        ("cbSize", wt.UINT),
        ("style", wt.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", wt.INT),
        ("cbWndExtra", wt.INT),
        ("hInstance", wt.HINSTANCE),
        ("hIcon", wt.HICON),
        ("hCursor", wt.HANDLE),
        ("hbrBackground", wt.HBRUSH),
        ("lpszMenuName", wt.LPCWSTR),
        ("lpszClassName", wt.LPCWSTR),
        ("hIconSm", wt.HICON),
    ]

class Msg(ctypes.Structure):
    """
    Docs: https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-msg
    """
    _fields_ = [
        ("hwnd", wt.HWND),
        ("message", wt.UINT),
        ("wParam", wt.WPARAM),
        ("lParam", wt.LPARAM),
        ("time", wt.DWORD),
        ("pt", wt.POINT),
        ("lPrivate", wt.DWORD)
    ]


class NIF():
    """
    0x00000001. The uCallbackMessage member is valid.
    0x00000002. The hIcon member is valid.
    0x00000004. The szTip member is valid.
    0x00000008. The dwState and dwStateMask members are valid.
    0x00000010. Display a balloon notification.
        The szInfo, szInfoTitle, dwInfoFlags, and uTimeout members are valid.
        Note that uTimeout is valid only in Windows 2000 and Windows XP.
        To display the balloon notification, specify NIF_INFO and provide text in szInfo.
        To remove a balloon notification, specify NIF_INFO and provide an empty
        string through szInfo.
        To add a notification area icon without displaying a notification,
        do not set the NIF_INFO flag.
    0x00000020.
        Windows 7 and later: The guidItem is valid.
        Windows Vista and earlier: Reserved.
    0x00000040. Windows Vista and later.
        If the balloon notification cannot be displayed immediately, discard it.
    0x00000080. Windows Vista and later. Use the standard tooltip.
    """
    MESSAGE = 0x00000001
    ICON = 0x00000002
    TIP = 0x00000004
    STATE = 0x00000008
    INFO = 0x00000010
    GUID = 0x00000020
    REALTIME = 0x00000040
    SHOWTIP = 0x00000080

class NIS():
    """
    The state of the icon. One or both of the following values
    0x00000001. The icon is hidden.
    0x00000002. The icon resource is shared between multiple icons.
    """
    HIDDEN = 0x00000001
    SHAREDICON = 0x00000002

class NIIF():
    """
    0x00000000. No icon.
    0x00000001. An information icon.
    0x00000002. A warning icon.
    0x00000003. An error icon.
    0x00000004. Windows XP SP2 and later.
        Windows XP: Use the icon identified in hIcon
            as the notification balloon's title icon.
        Windows Vista and later: Use the icon identified in hBalloonIcon
            as the notification balloon's title icon.
    0x00000010. Windows XP and later.
        Do not play the associated sound. Applies only to notifications.
    0x00000020. Windows Vista and later.
        The large version of the icon should be used as the notification icon.
    0x00000080. Windows 7 and later.
        Do not display the balloon notification if the current user is in "quiet time"
    0x0000000F. Windows XP and later. Reserved.
    """
    NONE = 0x00000000
    INFO = 0x00000001
    WARNING = 0x00000002
    ERROR = 0x00000003
    USER = 0x00000004
    NOSOUND = 0x00000010
    LARGE_ICON = 0x00000020
    RESPECT_QUIET_TIME = 0x00000080
    ICON_MASK = 0x0000000F

class NIM():
    """
    0x00000000. Adds an icon to the status area.
    0x00000001. Modifies an icon in the status area.
    0x00000002. Deletes an icon from the status area.
    0x00000003. Shell32.dll version 5.0 and later only.
        Returns focus to the taskbar notification area.
    0x00000004. Shell32.dll version 5.0 and later only.
        Instructs the notification area to behave according to the version number
        specified in the uVersion member of the structure pointed to by lpdata.
    """
    ADD = 0x00000000
    MODIFY = 0x00000001
    DELETE = 0x00000002
    SETFOCUS = 0x00000003
    SETVERSION = 0x00000004


class LR():
    """
    0x00002000. When the uType parameter specifies IMAGE_BITMAP,
        causes the function to return a DIB section bitmap rather than a compatible bitmap.
        This flag is useful for loading a bitmap without mapping it
        to the colors of the display device.
    0x00000000. The default flag; it does nothing. All it means is "not LR_MONOCHROME".
    0x00000040. Uses the width or height specified by the system metric values
        for cursors or icons, if the cxDesired or cyDesired values are set to zero.
    0x00000010. Loads the stand-alone image from the file specified by lpszName
        (icon, cursor, or bitmap file).
    0x00001000. Searches the color table for the image and replaces
        the following shades of gray with the corresponding 3-D color.
            Dk Gray, RGB(128,128,128) with COLOR_3DSHADOW
            Gray, RGB(192,192,192) with COLOR_3DFACE
            Lt Gray, RGB(223,223,223) with COLOR_3DLIGHT
        Do not use this option if you are loading a bitmap with a color depth greater than 8bpp.
    0x00000020. Retrieves the color value of the first pixel in the image
        and replaces the corresponding entry in the color table with
        the default window color (COLOR_WINDOW).
    0x00000001. Loads the image in black and white.
    0x00008000. Shares the image handle if the image is loaded multiple times.
    0x00000080. Uses true VGA colors.
    """
    CREATEDIBSECTION = 0x00002000
    DEFAULTCOLOR = 0x00000000
    DEFAULTSIZE = 0x00000040
    LOADFROMFILE = 0x00000010
    LOADMAP3DCOLORS = 0x00001000
    LOADTRANSPARENT = 0x00000020
    MONOCHROME = 0x00000001
    SHARED = 0x00008000
    VGACOLOR = 0x00000080

class WS():
    """
    Docs: https://docs.microsoft.com/en-us/windows/win32/winmsg/window-styles
    """
    BORDER = 0x00800000
    CAPTION = 0x00C00000
    CHILD = 0x40000000
    CHILDWINDOW = 0x40000000
    CLIPCHILDREN = 0x02000000
    CLIPSIBLINGS = 0x04000000
    DISABLED = 0x08000000
    DLGFRAME = 0x00400000
    GROUP = 0x00020000
    HSCROLL = 0x00100000
    ICONIC = 0x20000000
    MAXIMIZE = 0x01000000
    MAXIMIZEBOX = 0x00010000
    MINIMIZE = 0x20000000
    MINIMIZEBOX = 0x00020000
    OVERLAPPED = 0x00000000
    SYSMENU = 0x00080000
    THICKFRAME = 0x00040000
    OVERLAPPEDWINDOW = (
        OVERLAPPED | CAPTION | SYSMENU | THICKFRAME | MINIMIZEBOX | MAXIMIZEBOX
    )
    POPUP = 0x80000000
    POPUPWINDOW = POPUP | BORDER | SYSMENU
    SIZEBOX = 0x00040000
    TABSTOP = 0x00010000
    TILED = 0x00000000
    TILEDWINDOW = (
        OVERLAPPED | CAPTION | SYSMENU | THICKFRAME | MINIMIZEBOX | MAXIMIZEBOX
    )
    VISIBLE = 0x10000000
    VSCROLL = 0x00200000

class IMAGE():
    """
    0. Copies a bitmap.
    2. Copies a cursor.
    1. Copies an icon.
    """
    BITMAP = 0
    CURSOR = 2
    ICON = 1

# class WM():
#     """
#     The documentation is to scattered for these
#     constants, so I implemented only the minimal set
#     Docs: https://docs.microsoft.com/en-us/windows/win32/winmsg/window-notifications
#     """
#     CREATE = 0x0001
#     DESTROY = 0x0002
#     GETMINMAXINFO = 0x0024
#     NCCALCSIZE = 0x0083
#     NCCREATE = 0x0081
#     NCDESTROY = 0x0082
#     CLOSE = 0x0010
#     QUIT = 0x0012

# class PM():
#     """
#     NOREMOVE. Messages are not removed from the queue
#         after processing by PeekMessage
#     REMOVE. Messages are removed from the queue after processing
#     NOYIELD. Prevents the system from releasing any thread that is waiting
#         for the caller to go idle (see WaitForInputIdle).
#         Combine this value with either PM_NOREMOVE or PM_REMOVE
#     """
#     NOREMOVE = 0x0000
#     REMOVE = 0x0001
#     NOYIELD = 0x0002

class MsgValue():
    """
    A namespace for msg values constants
    """
    TRAY_ICON_EVENT = WM_USER + 1
    SHUTDOWN_THREAD = WM_USER + 999

class LParamValue():
    """
    A namespace for LPARAM values constants
    these are only some I was able to get via try and fail
    sadly they have no documented values
    """
    NOTIF_SHOW = 60425218
    NOTIF_HIDE = 60425220
    # Not sure about this one
    NOTIF_DISMISS = 60425221
    HOVER = 60424704
    LMB_PRESS = 60424705
    LMB_DPRESS = 60424707# double press
    # Not sure about this one
    LMB_HOLD = 60425216
    LMB_RELEASE = 60424706
    MMB_PRESS = 60424711
    MMB_RELEASE = 60424712
    RMB_PRESS = 60424708
    RMB_DPRESS = 60424710# double press
    # Not sure about this one
    RMB_HOLD = 60424315
    RMB_RELEASE = 60424709


user32.LoadImageW.argtypes = (
    wt.HINSTANCE, wt.LPCWSTR, wt.UINT, wt.INT, wt.INT, wt.UINT
)
user32.LoadImageW.restype = wt.HANDLE

user32.DestroyIcon.argtypes = (wt.HICON,)
user32.DestroyIcon.restype = wt.BOOL

kernel32.GetModuleHandleW.argtypes = (wt.LPCWSTR,)
kernel32.GetModuleHandleW.restype = wt.HMODULE

user32.DefWindowProcW.argtypes = (wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM)
user32.DefWindowProcW.restype = LRESULT

user32.RegisterClassExW.argtypes = (ctypes.POINTER(WndClassExw),)
user32.RegisterClassExW.restype = wt.ATOM

user32.UnregisterClassW.argtypes = (wt.LPCWSTR, wt.HINSTANCE)
user32.UnregisterClassW.restype = wt.BOOL

user32.CreateWindowExW.argtypes = (
    wt.DWORD,
    wt.ATOM,# This could be LPCWSTR instead of ATOM, but we'd have to use cls name
    wt.LPCWSTR, wt.DWORD,
    wt.INT, wt.INT, wt.INT, wt.INT,
    wt.HWND, wt.HMENU, wt.HINSTANCE, wt.LPVOID
)
user32.CreateWindowExW.restype = wt.HWND

user32.UpdateWindow.argtypes = (wt.HWND,)
user32.UpdateWindow.restype = wt.BOOL

user32.DestroyWindow.argtypes = (wt.HWND,)
user32.DestroyWindow.restype = wt.BOOL

shell32.Shell_NotifyIconW.argtypes = (wt.DWORD, ctypes.POINTER(NotifyIconDataW))
shell32.Shell_NotifyIconW.restype = wt.BOOL

user32.GetMessageW.argtypes = (ctypes.POINTER(Msg), wt.HWND, wt.UINT, wt.UINT)
user32.GetMessageW.restype = wt.INT

# user32.PeekMessageW.argtypes = (ctypes.POINTER(Msg), wt.HWND, wt.UINT, wt.UINT, wt.UINT)
# user32.PeekMessageW.restype = wt.BOOL

user32.TranslateMessage.argtypes = (ctypes.POINTER(Msg),)
user32.TranslateMessage.restype = wt.BOOL

user32.DispatchMessageW.argtypes = (ctypes.POINTER(Msg),)
user32.DispatchMessageW.restype = LRESULT

user32.PostMessageW.argtypes = (wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM)
user32.PostMessageW.restype = wt.BOOL


NotifCallback = Callable[[], None]

class _App():
    """
    Private class to represent an app
    """
    def __init__(
        self,
        name: str,
        icon_path: str|None,
        on_show: NotifCallback|None,
        on_hide: NotifCallback|None,
        on_dismiss: NotifCallback|None,
        on_hover: NotifCallback|None,
        on_lmb_click: NotifCallback|None,
        on_lmb_dclick: NotifCallback|None,
        on_mmb_click: NotifCallback|None,
        on_rmb_click: NotifCallback|None,
        on_rmb_dclick: NotifCallback|None
    ):
        """
        Constructor

        IN:
            name - the name of the app
            icon_path - path to optional icon for this notif
            on_hover - on hover event callback
            on_lmb_click - on left click event callback
            on_lmb_dclick - on left double click event callback
            on_mmb_click - on middle click event callback
            on_rmb_click - on right click event callback
            on_rmb_dclick - on right double click event callback
        """
        self._name = name
        self._icon_path = icon_path

        self._callback_map = {
            LParamValue.NOTIF_SHOW: on_show,
            LParamValue.NOTIF_HIDE: on_hide,
            LParamValue.NOTIF_DISMISS: on_dismiss,
            LParamValue.HOVER: on_hover,
            LParamValue.LMB_PRESS: on_lmb_click,
            LParamValue.LMB_DPRESS: on_lmb_dclick,
            LParamValue.MMB_PRESS: on_mmb_click,
            LParamValue.RMB_PRESS: on_rmb_click,
            LParamValue.RMB_DPRESS: on_rmb_dclick
        }

        self._thread: threading.Thread | None = None
        self._is_shown = False

        self._hinstance = None
        self._win_cls = None
        self._cls_atom = None
        self._hicon = None
        self._hwnd = None

    def _init(self):
        """
        Allocated resources for the app
        """
        self._set_hinstance()
        self._register_win_cls()
        self._load_icon()
        self._create_win()
        self._show_tray_icon()

    def _deinit(self):
        """
        Deallocated the app resources
        """
        self._hide_tray_icon()
        self._destroy_win()
        self._unload_icon()
        self._unregister_win_cls()
        self._unset_hinstance()

    def __del__(self):
        """
        Cleanup on gc
        """
        self.stop()
        # Just in case
        self._deinit()

    def _load_icon(self):
        """
        Loads the app icon
        """
        if self._icon_path:
            icon_flags = LR.DEFAULTCOLOR | LR.LOADFROMFILE | LR.DEFAULTSIZE | LR.SHARED
            hicon = user32.LoadImageW(
                None,# Use NULL since we're loading a "stand-alone" resource
                self._icon_path,
                IMAGE.ICON,
                0,
                0,
                icon_flags
            )
            if not hicon:
                raise WinAPIError("failed to load icon", _get_last_err())

        else:
            hicon = 0# TODO: doesn't work

        self._hicon = hicon

    def _unload_icon(self):
        """
        Unloads the app icon
        """
        if self._hicon:
            user32.DestroyIcon(self._hicon)
            self._hicon = None

    def _set_hinstance(self):
        """
        Gets the handler of this dll
        """
        handle = kernel32.GetModuleHandleW(None)
        if not handle:
            raise WinAPIError("failed to get module handle", _get_last_err())
        self._hinstance = handle

    def _unset_hinstance(self):
        """
        Removes the pointer to the handler of this dll
        """
        self._hinstance = None

    def _register_win_cls(self):
        """
        Registers a window class
        """
        def winproc(hwnd: wt.HWND, msg: wt.UINT, wparam: wt.WPARAM, lparam: wt.LPARAM) -> LRESULT:
            cb = self._callback_map.get(lparam, None)# type: ignore
            if cb:
                cb()
            # print(f"{hex(msg)}: {wparam} | {lparam}")# type: ignore
            return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

        self._win_cls = win_cls = WndClassExw()
        win_cls.cbSize = ctypes.sizeof(win_cls)
        win_cls.style = 0
        win_cls.lpfnWndProc = WNDPROC(winproc)
        win_cls.cbClsExtra = 0
        win_cls.cbWndExtra = 0
        win_cls.hInstance = self._hinstance
        win_cls.hIcon = 0
        win_cls.hCursor = 0
        win_cls.hbrBackground = 0
        win_cls.lpszClassName = self._name

        cls_atom = user32.RegisterClassExW(ctypes.byref(win_cls))
        if not cls_atom:
            raise WinAPIError("failed to create class ATOM", _get_last_err())
        self._cls_atom = cls_atom

    def _unregister_win_cls(self):
        """
        Unregisters the window class
        """
        if self._win_cls:
            user32.UnregisterClassW(self._win_cls.lpszClassName, self._hinstance)
            self._win_cls = None
            self._cls_atom = None

    def _create_win(self):
        """
        Creates a tray window
        """
        win_style = WS.OVERLAPPED | WS.SYSMENU
        hwnd = user32.CreateWindowExW(
            0,
            self._cls_atom,
            # self._win_cls.lpszClassName,
            # self._name,
            self._win_cls.lpszClassName,
            win_style,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            HWND_MESSAGE,
            None,
            self._hinstance,
            None
        )
        if not hwnd:
            raise WinAPIError("failed to create a window", _get_last_err())
        user32.UpdateWindow(hwnd)
        self._hwnd = hwnd

    def _destroy_win(self):
        """
        Destroys the tray window
        """
        if self._hwnd:
            user32.DestroyWindow(self._hwnd)
            self._hwnd = None

    def _get_base_nid(self) -> NotifyIconDataW:
        """
        Constructs and returns "base" version of NotifyIconDataW
        """
        nid = NotifyIconDataW()
        nid.cbSize = ctypes.sizeof(nid)
        nid.hWnd = self._hwnd
        nid.uID = APP_ID
        nid.uFlags = NIF.ICON | NIF.STATE | NIF.MESSAGE | NIF.TIP
        nid.uCallbackMessage = MsgValue.TRAY_ICON_EVENT
        nid.hIcon = self._hicon
        nid.szTip = self._name[:128]
        # nid.szInfo = body[:256]
        nid.uVersion = NOTIFYICON_VERSION_4
        # nid.szInfoTitle = title[:64]
        nid.dwInfoFlags = NIIF.NOSOUND | NIIF.USER | NIIF.LARGE_ICON | NIIF.RESPECT_QUIET_TIME

        return nid

    def _run_event_loop(self):
        msg = Msg()
        msg_p = ctypes.byref(msg)
        hwnd = self._hwnd
        # both 0s == no filter
        filter_min = 0
        filter_max = 0
        # print("starting")
        while (rv := user32.GetMessageW(msg_p, hwnd, filter_min, filter_max)) != 0:
            # print("pumped")
            if rv == -1:
                raise WinAPIError("GetMessageW returned an error code", _get_last_err())
            if msg.message == MsgValue.SHUTDOWN_THREAD:
                # print("shutting down")
                break
            user32.TranslateMessage(msg_p)
            user32.DispatchMessageW(msg_p)

        # print("exiting")

    def _run(self):
        """
        Shows the app + runs the event loop + hides the app
        NOTE: Blocking call
        """
        self._init()
        try:
            self._run_event_loop()
        finally:
            self._deinit()

    def start(self):
        """
        Runs the app
        """
        if not self._thread:
            self._thread = thread = threading.Thread(target=self._run, daemon=True)
            thread.start()

    def stop(self):
        """
        Stops the app
        NOTE: this will block until the app is stopped
        """
        if self._hwnd:
            user32.PostMessageW(self._hwnd, MsgValue.SHUTDOWN_THREAD, 0, 0)
            if self._thread:
                self._thread.join()
                self._thread = None

    def _show_tray_icon(self) -> bool:
        """
        Shows tha app tray icon
        """
        rv = False

        if not self._is_shown:
            nid = self._get_base_nid()
            rv = bool(shell32.Shell_NotifyIconW(NIM.ADD, ctypes.byref(nid)))
            if rv:
                shell32.Shell_NotifyIconW(NIM.SETVERSION, ctypes.byref(nid))
                self._is_shown = True

        return rv

    def _hide_tray_icon(self) -> bool:
        """
        Hides tha app tray icon
        """
        rv = False

        if self._is_shown:
            nid = self._get_base_nid()
            rv = bool(shell32.Shell_NotifyIconW(NIM.DELETE, ctypes.byref(nid)))

            self._is_shown = False

        return rv

    def send_notif(self, title: str, body: str) -> bool:
        """
        Sends a notification

        IN:
            title - the title of the notification
            body - the body of the notification
        """
        if not self._is_shown:
            return False

        nid = self._get_base_nid()

        nid.uFlags |= NIF.INFO | NIF.SHOWTIP
        nid.szInfo = body[:256]
        nid.szInfoTitle = title[:64]

        return bool(shell32.Shell_NotifyIconW(NIM.MODIFY, ctypes.byref(nid)))

    def clear_notifs(self):
        """
        Clears notifications
        """
        if not self._is_shown:
            return

        # According to microsoft docs this should work
        # but it works 1 out of 20 times...
        # nid = self._get_base_nid()
        # nid.uFlags = NIF.INFO
        # nid.szInfo = ""
        # nid.szInfoTitle = ""
        # shell32.Shell_NotifyIconW(NIM.MODIFY, ctypes.byref(nid))

        # So we're doing this hack
        self._hide_tray_icon()
        self._show_tray_icon()


class NotifManager():
    """
    Notification manager
    """
    _instance = None

    def __new__(cls, *args, **kwargs) -> NotifManager:# pylint: disable=unused-argument
        """
        Singleton implementation
        """
        if cls._instance is not None:
            raise ManagerAlreadyExistsError()

        self = super().__new__(cls)
        cls._instance = weakref.ref(self)

        return self

    def __init__(
        self,
        app_name: str,
        icon_path: str|None = None,
        on_show: NotifCallback|None = None,
        on_hide: NotifCallback|None = None,
        on_dismiss: NotifCallback|None = None,
        on_hover: NotifCallback|None = None,
        on_lmb_click: NotifCallback|None = None,
        on_lmb_dclick: NotifCallback|None = None,
        on_mmb_click: NotifCallback|None = None,
        on_rmb_click: NotifCallback|None = None,
        on_rmb_dclick: NotifCallback|None = None
    ):
        """
        Constructor

        IN:
            app_name - the app name shared by the notifs
            icon_path - the path to the icon shared by the notifs
            on_show - on notif show event callback
                (Default: None)
            on_hide - on notif hide event callback
                (Default: None)
            on_dismiss - on notif dismiss event callback
                if a dismiss event has been fired, hide won't be fired
                (Default: None)
            on_hover - on hover event callback
                NOTE: hover callback may run event during click events
                (Default: None)
            on_lmb_click - on left click event callback
                (Default: None)
            on_lmb_dclick - on left double click event callback
                NOTE: before a double click event, a click event will still be fired
                (Default: None)
            on_mmb_click - on middle click event callback
                (Default: None)
            on_rmb_click - on right click event callback
                (Default: None)
            on_rmb_dclick - on right double click event callback
                NOTE: before a double click event, a click event will still be fired
                (Default: None)
        """
        # Ask the interpreter for cleanup
        atexit.register(self.shutdown)

        self._app: _App|None = _App(
            app_name,
            icon_path,
            on_show=on_show,
            on_hide=on_hide,
            on_dismiss=on_dismiss,
            on_hover=on_hover,
            on_lmb_click=on_lmb_click,
            on_lmb_dclick=on_lmb_dclick,
            on_mmb_click=on_mmb_click,
            on_rmb_click=on_rmb_click,
            on_rmb_dclick=on_rmb_dclick
        )
        self._app.start()

    def __del__(self):
        self.shutdown()

    def is_ready(self) -> bool:
        """
        Checks if the manager and app are ready to send notifications
        """
        return self._app is not None and self._app._is_shown# pylint: disable=protected-access

    def send(self, title: str, body: str) -> bool:
        """
        Sends a notifification

        IN:
            title - the title of the notification
            body - the body of the notification

        OUT:
            boolean - success status
        """
        if not self._app:
            return False
        return self._app.send_notif(title, body)

    def clear(self):
        """
        Clears all notification this manager has access to
        To completely free the resources on quit, use
            the 'shutdown' method
        """
        if self._app:
            self._app.clear_notifs()

    def shutdown(self):
        """
        A method to call on shutdown of your app
        Gracefully clears notifs, hides the icon, frees the resources
        """
        if self._app:
            self._app.stop()
            # Incase you're a clever laf and run the cleanup, we can abort it
            atexit.unregister(self.shutdown)
            self._app = None
