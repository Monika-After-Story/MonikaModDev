import ctypes
import ctypes.wintypes as wt
import weakref
from collections import deque
from typing import Optional

from .common import WinAPIError, Winnie32APIError, _get_last_err


user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
shell32 = ctypes.windll.shell32


LRESULT = wt.LPARAM#ctypes.c_long
WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM)

CW_USEDEFAULT = -2147483648
WM_USER = 0x0400
HWND_MESSAGE = -3
APP_ID = 922

NOTIFS_LIMIT = 100


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
    BITMAP = wt.UINT(0)
    CURSOR = wt.UINT(2)
    ICON = wt.UINT(1)


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


class MaxNotifsReachedError(Winnie32APIError):
    """
    An error raised when spawned too many WindowsNotif
    """
    def __str__(self) -> str:
        return "too many notification"

class InvalidNotifAccessError(Winnie32APIError):
    """
    An error raised when tried to use a cleared WindowsNotif
    """
    def __str__(self) -> str:
        return "can't use notification after it's been cleared"

class WindowsNotif():
    """
    Class reprensets a windows notification
    """
    _NOTIF_ID_POOL = deque(
        map(str, range(NOTIFS_LIMIT)),
        maxlen=NOTIFS_LIMIT
    )

    def __init__(
        self,
        app_name: str,
        icon_path: Optional[str],
        title: str,
        body: str
    ):
        """
        Constructs a new windows notification

        IN:
            app_name - the name of the app
            icon_path - path to optional icon for this notif
            title - the notif title
            body - the notif body
        """
        # Predefine in case we crash
        self._hinstance = None
        self._win_cls = None
        self._cls_atom = None
        self._hicon = None
        self._hwnd = None
        self._nid = None
        self._notif_id = None

        if not self._NOTIF_ID_POOL:
            raise MaxNotifsReachedError()

        self._app_name = app_name
        self._icon_path = icon_path
        self._title = title
        self._body = body

        self._used = False
        self._notif_id = self._NOTIF_ID_POOL.popleft()

        self._after_init()

    def _after_init(self):
        self._set_hinstance()
        self._register_win_cls()
        self._load_icon()
        self._create_win()

    def _deinit(self):
        self._hide_notif()
        self._destroy_win()
        self._unload_icon()
        self._unregister_win_cls()

    def __del__(self):
        """
        Cleanup on gc
        """
        if self._notif_id is not None:
            self._deinit()
            self._NOTIF_ID_POOL.append(self._notif_id)
            self._notif_id = None

    def __call__(self):
        """
        Shortcut for the send method
        """
        if self._notif_id is None:
            raise InvalidNotifAccessError()
        if not self._used:
            self._used = True
            self._display_notif()

    def send(self):
        """
        Sends this notif, once
        """
        self()

    def reset(self):
        """
        Resets this notif allowing it to be send again
        """
        if self._notif_id is None:
            raise InvalidNotifAccessError()
        self._deinit()
        self._after_init()
        self._used = False

    def clear(self):
        """
        Clears this notif freeing the resources
        The notif can't be used anymore after it's been cleared
        """
        self.__del__()

    def _load_icon(self):
        """
        Loads the notification icon
        """
        if self._icon_path:
            icon_flags = LR.LOADFROMFILE | LR.DEFAULTSIZE
            hicon = user32.LoadImageW(
                None,# Use NULL since we're loading a "stand-alone" resource
                self._icon_path,
                IMAGE.ICON,
                0,
                0,
                icon_flags
            )

        else:
            hicon = 0

        self._hicon = hicon

    def _unload_icon(self):
        """
        Unloads the notification icon
        """
        if self._hicon:
            user32.DestroyIcon(self._hicon)

    def _set_hinstance(self):
        """
        Gets the handler of this dll
        """
        self._hinstance = handle = kernel32.GetModuleHandleW(None)
        if not handle:
            raise WinAPIError("failed to get module handle", _get_last_err())

    def _register_win_cls(self):
        """
        Registers a window class
        """
        def winproc(hwnd: wt.HWND, msg: wt.UINT, wparam: wt.WPARAM, lparam: wt.LPARAM) -> LRESULT:
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
        win_cls.lpszClassName = self._app_name + self._notif_id

        self._cls_atom = cls_atom = user32.RegisterClassExW(ctypes.byref(win_cls))
        if not cls_atom:
            raise WinAPIError("failed to create class ATOM", _get_last_err())

    def _unregister_win_cls(self):
        """
        Unregisters a window class
        """
        if self._win_cls:
            user32.UnregisterClassW(self._win_cls.lpszClassName, self._hinstance)

    def _create_win(self):
        """
        Creates a notification window
        """
        win_style = WS.OVERLAPPED | WS.SYSMENU
        hwnd = user32.CreateWindowExW(
            0,
            self._cls_atom,
            # self._win_cls.lpszClassName,
            # self._app_name,
            self._win_cls.lpszClassName,
            win_style,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            None,
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
        Destroys the notification window
        """
        if self._hwnd:
            user32.DestroyWindow(self._hwnd)

    def _display_notif(self):
        """
        Displays this notification
        """
        self._nid = nid = NotifyIconDataW()
        nid.cbSize = ctypes.sizeof(nid)
        nid.hWnd = self._hwnd
        nid.uID = APP_ID
        nid.uFlags = (
            NIF.ICON | NIF.INFO | NIF.STATE | NIF.MESSAGE | NIF.TIP | NIF.SHOWTIP
        )
        nid.uCallbackMessage = WM_USER + 2
        nid.hIcon = self._hicon
        nid.szTip = self._app_name[:128]
        nid.szInfo = self._body[:256]
        nid.uVersion = 4
        nid.szInfoTitle = self._title[:64]
        nid.dwInfoFlags = NIIF.NOSOUND | NIIF.USER | NIIF.LARGE_ICON | NIIF.RESPECT_QUIET_TIME

        shell32.Shell_NotifyIconW(NIM.ADD, ctypes.byref(nid))
        shell32.Shell_NotifyIconW(NIM.SETVERSION, ctypes.byref(nid))

    def _hide_notif(self):
        """
        Hides this notification
        """
        if self._nid:
            shell32.Shell_NotifyIconW(NIM.DELETE, ctypes.byref(self._nid))
            user32.UpdateWindow(self._hwnd)

class WindowsNotifManager():
    """
    Notification manager
    """
    def __init__(self, app_name: str, icon_path: Optional[str]):
        """
        Constructor

        IN:
            app_name - the app name shared by the notifs
            icon_path - the path to the icon shared by the notifs
        """
        self._app_name = app_name
        self._icon_path = icon_path

        self._notifs: deque[weakref.ReferenceType[WindowsNotif]] = deque(maxlen=NOTIFS_LIMIT)

    def spawn(self, title: str, body: str) -> WindowsNotif:
        """
        Spawns a notif, but doesn't send it

        IN:
            title - the title of the notification
            body - the body of the notification
        """
        notif = WindowsNotif(self._app_name, self._icon_path, title, body)
        self._notifs.append(weakref.ref(notif))
        return notif

    def send(self, title: str, body: str) -> WindowsNotif:
        """
        Spawns and sends a notif

        IN:
            title - the title of the notification
            body - the body of the notification
        """
        notif = self.spawn(title, body)
        notif.send()
        return notif

    def clear(self):
        """
        Clears all notification this manager has access to
        """
        for notif_ref in self._notifs:
            notif = notif_ref()
            if notif:
                notif.clear()
        self._notifs.clear()
