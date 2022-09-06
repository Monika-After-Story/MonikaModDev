"""
winnie32api - minimalistic Windows API

Provides a small number of utils, allowing to not include big dependencies like pywin32/win32api
"""

from __future__ import annotations

__title__ = "winnie32api"
__author__ = "Booplicate"
__version__ = "0.1.2"

from .mouse import *
from .windows import *
from .notifs import *
