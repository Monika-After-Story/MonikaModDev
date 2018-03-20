"""
This module provides functions to check information for the battery and
the AC Line on Linux systems.
"""

import os

"""
Path to the Linux power supply class directory
"""
LINUX_POWER_SUPPLY_CLASS = '/sys/class/power_supply/'


def _get_battery():
    """
    Return the path to the systems' battery class, None otherwise.
    """
    for file in os.listdir(LINUX_POWER_SUPPLY_CLASS):
        if file.startswith('BAT'):
            return os.path.join(LINUX_POWER_SUPPLY_CLASS, file)

    return None


def _read_battery(what):
    """
    Return content from a file in the battery class.
    """
    bat = _get_battery()

    if bat == None:
        raise RuntimeError('Battery not found')

    path = os.path.join(bat, what)

    with open(path, 'r') as f:
        content = f.read()

    return content


def get_level():
    """
    Return the system battery level from the battery class in percentage,
    otherwise None if the system doesn't have any batteries.
    """
    level = int(_read_battery('capacity'))

    return level


def is_charging():
    """
    Check if the system is charging based on the battery class

    :return: True if it's charging, false otherwise
    """
    status = _read_battery('status')

    return status == 'Charging\n'


def is_battery_present():
    """
    Check if the system have a battery present

    :return: True if there's a battery, false otherwise
    """
    return _get_battery() != None
