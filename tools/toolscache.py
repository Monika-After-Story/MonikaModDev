# saves stuff to the .toolscache file for usage later
# stuff is saved via json

import json
import os

from typing import Any, Optional, Dict

__CACHE: Optional[Dict[str, Any]] = None
CACHE_FILE = ".toolscache"

def get(key: str, default: Any) -> Any:
    """
    Gets item from cache
    :param key: key of item to get
    :param default: default value if cache could not be loaded or data not in cache
    :returns: item from cache
    """
    if __CACHE is None:
        if not _load_cache():
            return default

    return __CACHE.get(key, default)


def put(key: str, value: Any):
    """
    Puts item in the cache
    :param key: key to use for the value
    :param value: value to put in the cache
    """
    if __CACHE is None:
        if not _load_cache():
            return

    __CACHE[key] = value


def _load_cache() -> bool:
    """
    Loads the tools cache
    :returns: True if cache loaded, false if not
    """
    global __CACHE
    if not os.access(CACHE_FILE, os.F_OK):
        __CACHE = {}
        return True

    if not os.access(CACHE_FILE, os.R_OK):
        return False

    try:
        with open(CACHE_FILE, "r") as cache_file:
            __CACHE = json.load(cache_file)
    except json.JSONDecodeError:
        __CACHE = {}
    except Exception:
        return False

    return True


def _save_cache():
    """
    Saves the tools cache
    """
    if __CACHE is None or len(__CACHE) < 1:
        return

    try:
        with open(CACHE_FILE, "w") as cache_file:
            json.dump(__CACHE, cache_file, indent=4)

    except Exception as e:
        print("error saving tools cache: {0}".format(e))