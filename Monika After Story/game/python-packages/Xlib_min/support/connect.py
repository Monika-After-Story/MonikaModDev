_C='OpenVMS'
_B='unix_connect'
_A='vms_connect'
import sys,importlib
_display_mods={_C:_A}
_default_display_mod=_B
_socket_mods={_C:_A}
_default_socket_mod=_B
_auth_mods={_C:_A}
_default_auth_mod=_B
_parts=sys.platform.split('-')
platform=_parts[0]
del _parts
def _relative_import(modname):return importlib.import_module('..'+modname,__name__)
def get_display(display):'dname, protocol, host, dno, screen = get_display(display)\n\n    Parse DISPLAY into its components.  If DISPLAY is None, use\n    the default display.  The return values are:\n\n      DNAME    -- the full display name (string)\n      PROTOCOL -- the protocol to use (None if automatic)\n      HOST     -- the host name (string, possibly empty)\n      DNO      -- display number (integer)\n      SCREEN   -- default screen number (integer)\n    ';A=_display_mods.get(platform,_default_display_mod);B=_relative_import(A);return B.get_display(display)
def get_socket(dname,protocol,host,dno):'socket = get_socket(dname, protocol, host, dno)\n\n    Connect to the display specified by DNAME, PROTOCOL, HOST and DNO, which\n    are the corresponding values from a previous call to get_display().\n\n    Return SOCKET, a new socket object connected to the X server.\n    ';A=_socket_mods.get(platform,_default_socket_mod);B=_relative_import(A);return B.get_socket(dname,protocol,host,dno)
def get_auth(sock,dname,protocol,host,dno):'auth_name, auth_data = get_auth(sock, dname, protocol, host, dno)\n\n    Return authentication data for the display on the other side of\n    SOCK, which was opened with DNAME, HOST and DNO, using PROTOCOL.\n\n    Return AUTH_NAME and AUTH_DATA, two strings to be used in the\n    connection setup request.\n    ';A=_auth_mods.get(platform,_default_auth_mod);B=_relative_import(A);return B.get_auth(sock,dname,protocol,host,dno)