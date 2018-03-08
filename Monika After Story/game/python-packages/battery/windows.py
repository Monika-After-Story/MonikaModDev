"""
This module provides functions to check information for the battery and
the AC Line on Windows systems.

It may only work on Windows Server 2003 / Windows XP and above.

For more information see the following:
https://msdn.microsoft.com/en-us/library/windows/desktop/aa373232(v=vs.85).aspx
"""

import ctypes

try:
    from ctypes import wintypes
except:  # pragma: no cover
    wintypes = None


def _system_power_status():
    """
    Return 'SYSTEM_POWER_STATUS' C structure with the values set by
    GetSystemPowerStatus.
    """

    class SYSTEM_POWER_STATUS(ctypes.Structure):
        """
        This class is a representation of the SYSTEM_POWER_STATUS C structure
        used by GetSystemPowerStatus.
        """
        _fields_ = [
            ('ACLineStatus', wintypes.BYTE),
            ('BatteryFlag', wintypes.BYTE),
            ('BatteryLifePercent', wintypes.BYTE),
            ('Reserved1', wintypes.BYTE),
            ('BatteryLifeTime', wintypes.DWORD),
            ('BatteryFullLifeTime', wintypes.DWORD),
        ]

    pointer = ctypes.POINTER(SYSTEM_POWER_STATUS)

    GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
    GetSystemPowerStatus.argtypes = [pointer]
    GetSystemPowerStatus.restype = wintypes.BOOL

    status = SYSTEM_POWER_STATUS()

    if not GetSystemPowerStatus(ctypes.pointer(status)):
        raise ctypes.WinError()

    return status


def _get_ac_status():
    """
    Return the ACLineStatus from SYSTEM_POWER_STATUS
    """
    return _system_power_status().ACLineStatus


def _get_battery_flag():
    """
    Return the BatteryFlag from SYSTEM_POWER_STATUS
    """
    return _system_power_status().BatteryFlag


def get_level():
    """
    Return the system battery level in percentage, otherwise None
    if the value is unknown
    """
    percentage = _system_power_status().BatteryLifePercent

    if percentage == 255:
        return None

    return percentage


def is_charging():
    """
    Check if the system is charging based on the ACLineStatus.

    :return: True if it's charging, false otherwise
    """
    return _get_ac_status() == 1 or _get_ac_status() == 255


def is_battery_present():
    """
    Check if the system have a battery present

    :return: True if there's a battery, false otherwise
    """
    return _get_battery_flag() != 128 or _get_battery_flag() != 255
