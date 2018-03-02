"""
This module provides functions to check information for the battery and
the AC Line for various systems by running commands onto a shell.
"""

import platform
import re
import subprocess

"""
List of commands that can be used to check for the battery level.
"""
BATTERY_LEVEL_COMMANDS = {
    'FreeBSD': 'sysctl hw.acpi.battery.life',
    'Darwin': 'pmset -g batt',
}

"""
List of regex patterns to be used with BATTERY_LEVEL_COMMANDS to extract
the battery level
"""
BATTERY_LEVEL_REGEX = {
    'FreeBSD': r'hw\.acpi\.battery\.life: (\d+)',
    'Darwin': r'(\d+%)',
}

"""
List of commands that can be used to check for the AC Line status.
"""
AC_LINE_CHECK_COMMANDS = {
    'FreeBSD': 'sysctl hw.acpi.acline',
    'Darwin': 'pmset -g batt',
}

"""
List of regex patterns to be used with AC_LINE_CHECK_COMMANDS to extract
the AC Line status.
"""
AC_LINE_CHECK_REGEX = {
    'FreeBSD': r'hw\.acpi\.acline: (\d)',
    'Darwin': r'\d+%; (\w+);'
}

_system = platform.system()


class RegexDidNotMatchError(RuntimeError):
    pass


def _run_command_based_by_system(cmddict, regexdict):
    """
    Runs a command based on the system running.

    Raises RegexDidNotMatchError if the regex provided did not match
    the output of the command.

    :param cmddict: Dictionary of commands to run by system
    :param regexdict: Dictionary of regex patterns to filter the output
                      by system

    :return: The output from the command filtered by the regex pattern
             if provided
    """
    cmd = cmddict[_system]

    output = subprocess.check_output(cmd, shell=True)

    if _system in regexdict:
        regex = regexdict[_system]
        res = re.search(regex, output)
        if res:
            output = res.group(1)
        else:
            raise RegexDidNotMatchError("Regex failure for '%s' on %s" %
                                        (output, _system))

    return output


def _run_function_based_by_system(funcdict):
    """
    Executes a function based on the system running

    :param funcdict: Dictionary of functions by system
    """
    func = funcdict[_system]

    return func()


def get_level():
    """
    Return the system battery level based on the command output in percentage,
    otherwise None if the system doesn't have any batteries.
    """
    try:
        output = _run_command_based_by_system(BATTERY_LEVEL_COMMANDS,
                                              BATTERY_LEVEL_REGEX)
        value = int(output.rstrip())
    except RegexDidNotMatchError:
        return None

    return int(output.rstrip())


def get_supported_systems():
    """
    Returns a list of supported systems.
    """
    return BATTERY_LEVEL_COMMANDS.keys()


def can_check():
    """
    Check if this module can check the battery.
    """
    return _system in get_supported_systems()


def _freebsd_is_battery_present():
    """
    Check if there's a battery present for FreeBSD systems.
    """
    try:
        level = get_level()
    except RegexDidNotMatchError:
        return False
    return level != -1


def _darwin_is_battery_present():
    """
    Check if there's a battery present for macOS systems.
    """
    try:
        get_level()
    except RegexDidNotMatchError:
        return False
    return True


"""
List of functions that can be used to check if the battery is present.
"""
BATTERY_CHECK_FUNCTIONS = {
    'FreeBSD': _freebsd_is_battery_present,
    'Darwin': _darwin_is_battery_present,
}


def is_battery_present():
    """
    Check if the system has a battery present.
    """
    return _run_function_based_by_system(BATTERY_CHECK_FUNCTIONS)


def _get_ac_line_status():
    """
    Return the output of the AC Line command
    """
    output = _run_command_based_by_system(AC_LINE_CHECK_COMMANDS,
                                          AC_LINE_CHECK_REGEX)
    return output


def _freebsd_is_charging():
    """
    Check if it's charging for FreeBSD systems.
    """
    return bool(int(_get_ac_line_status().rstrip()))


def _darwin_is_charging():
    """
    Check if it's charging for macOS systems.
    """
    charging_statuses = ['charging', 'charged']

    return _get_ac_line_status() in charging_statuses


"""
List of functions that can be used to check if the system is charging.
"""
AC_LINE_CHECK_FUNCTIONS = {
    'FreeBSD': _freebsd_is_charging,
    'Darwin': _darwin_is_charging,
}


def is_charging():
    """
    Check if the system is charging.
    """
    return _run_function_based_by_system(AC_LINE_CHECK_FUNCTIONS)
