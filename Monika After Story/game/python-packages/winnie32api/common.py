from __future__ import annotations

import ctypes
from ctypes.wintypes import (
    INT
)
from dataclasses import dataclass

from typing import (
    Any,
    NamedTuple
)


user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


Coord = int

class Point(NamedTuple):
    """
    Represents a point on a screen
    """
    x: Coord
    y: Coord

class Rect(NamedTuple):
    """
    Represents a rectangle on a screen
    """
    top_left: Point
    bottom_right: Point

    @classmethod
    def from_coords(cls, left: Coord, top: Coord, right: Coord, bottom: Coord) -> Rect:
        """
        Constructs a rect from 4 coordinates
        """
        return cls(
            Point(left, top),
            Point(right, bottom)
        )


@dataclass
class Pack():
    """
    Class that we use as a pointer to the inner value
    """
    value: Any


def _reset_last_err():
    """
    Clears the last error
    """
    kernel32.SetLastError(INT(0))

def _get_last_err() -> int:
    """
    Returns the last error code
    """
    return kernel32.GetLastError()
