# -*- coding: utf-8 -*-
#
# This module implements LFU cache in python using just one class,
# nevertheless, for the most basic operations (add/get) should be still quite fast.
# You can also remove cache entries by priority or key, although, this may be slow depending on the size.
# Uneless you're making something fancy, usually it should be enough to just use the `create_lfu_cache` decorator
# on your function.
# Example:
#
# from lfu_cache import create_lfu_cache
#
# @create_lfu_cache(limit=1024, typed=True)
# def expensive_function(arg):
#     *heavy processing*
#     return arg
#
# That'll cache 1024 precisely stored inputs (since `typed` is set `True`) and outputs. Bear in mind,
# the first execution may take more time, but you save more time with each next call.
# You can access the original (w/o the decorator, not affected by the cache system) function using
# the `__wrapped__` property, the `__cache__` property can be used to access the LFUCache object of the function.
# The cache object has 2 useful property for debugging: `hits` and `misses`, showing how effective the cache was reused.

### START LFU Cache implementation

from threading import RLock
from collections import namedtuple

_CacheEntry = namedtuple("CacheEntry", ("key", "value", "access_count"))

class LFUCache(object):
    """
    Python implementation of LFU (Least Frequently Used) cache

    PROPERTIES:
        limit - (int/None) maximum number of entries in the cache
            (if we exceed, we start removing the least used ones)
            None - unlimited, 0 - blocked for writing new entries
            NOTE: It is safe to adjust limit after init
        hits - (int) number of times the cache was reused
        misses - (int) number of times the cache was written
    """
    def __init__(self, limit=128):
        """
        Constructor for cache instances

        IN:
            limit - maximum number of entries in this cache, unlimited if None
                (NOTE: if not None, it must be more or equal to zero)
                (Default: 128)
        """
        if not (
            limit is None
            or (
                isinstance(limit, int)
                and limit >= 0
            )
        ):
            raise Exception("LFUCache expects its limit to be an intenger >= 0 or NoneType.")

        self._limit = limit
        # key: [queue_id + value]
        self._cache_entries = dict()
        # queue_id: [access_count + key]
        self._priority_queue = list()
        self._hits = 0
        self._misses= 0
        self._lock = RLock()

    def __repr__(self):
        """
        Representation of this object
        """
        return "<LFUCache ({0}/{1} entries) at {2}>".format(
            len(self._priority_queue),
            self._limit,
            hex(int(id(self))).upper()
        )

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, new_limit):
        with self._lock:
            # If the new limit is smaller than the current,
            # we may need to remove some of our cache entries
            if new_limit is not None:
                excessive_entries = len(self._priority_queue) - new_limit
                while excessive_entries > 0:
                    item = self._priority_queue.pop()
                    del self._cache_entries[item[0]]
                    excessive_entries -= 1

            # Set the limit
            self._limit = new_limit

    @property
    def hits(self):
        return self._hits

    @property
    def misses(self):
        return self._misses

    def clear(self):
        """
        Clears this cache
        """
        with self._lock:
            self._cache_entries.clear()
            self._priority_queue[:] = []

    def add(self, key, value, update=False):
        """
        Adds a new entry with the given key and value.

        IN:
            key - key to save entry to
            value - value to save
            update - whether or not we should update the value if the key
                already exists
                (Default: False)

        OUT:
            boolean whether or not the entry was added to the cache
        """
        with self._lock:
            if self._limit == 0:
                return False

            if not self.has_cache(key):
                queue_len = len(self._priority_queue)
                if self._limit is not None and queue_len >= self._limit:
                    self._remove_by_id(self._limit - 1)
                    queue_len -= 1

                self._priority_queue.append([key, 1])
                self._cache_entries[key] = [queue_len, value]
                self._misses += 1
                return True

            elif update:
                self._increment_access_count(key)
                self._cache_entries[key][1] = value
                self._misses += 1
                return True

            return False

    def has_cache(self, key):
        """
        Checks if we have a cache for the given key
        """
        with self._lock:
            return key in self._cache_entries

    def get(self, key, default=None):
        """
        Retrieves an entry by key

        IN:
            key - key to get
            default - value to return if the key doesn't exist
                (Default: None)

        OUT:
            cached value
        """
        with self._lock:
            if not self.has_cache(key):
                return default

            self._hits += 1
            self._increment_access_count(key)
            return self._cache_entries[key][1]

    def remove(self, key):
        """
        Removes an entry by key

        IN:
            key - key to remove

        OUT:
            boolean whether or not the entry was removed from the cache
        """
        with self._lock:
            if not self.has_cache(key):
                return False

            queue_id = self._cache_entries[key][0]

            del self._priority_queue[queue_id]
            del self._cache_entries[key]

            # We need to update the ids for the keys after this one because of potential shift
            for item in self._priority_queue[queue_id:]:
                # Access each entry and "increment" its priority
                self._cache_entries[item[0]][0] -= 1

            return True

    def _remove_by_id(self, queue_id):
        """
        Removes an entry by id

        IN:
            queue_id - entry id in queue

        OUT:
            boolean whether or not the entry was removed from the cache
        """
        with self._lock:
            if not (len(self._priority_queue) > queue_id >= 0):
                return False

            key = self._priority_queue[queue_id][0]

            del self._cache_entries[key]
            del self._priority_queue[queue_id]

            for item in self._priority_queue[queue_id:]:
                self._cache_entries[item[0]][0] -= 1

            return True

    def _increment_access_count(self, key):
        """
        Increments counter for the entry with the given key
        and adjusts its priority

        IN:
            key - key to use
                (NOTE: must exist)
        """
        with self._lock:
            queue_id = self._cache_entries[key][0]
            next_queue_id = queue_id - 1
            # Kick up access count
            self._priority_queue[queue_id][1] += 1
            # Move this entry in the queue if needed
            while (
                queue_id > 0
                and self._priority_queue[queue_id][1] > self._priority_queue[next_queue_id][1]
            ):
                # Update cache for the next entry
                next_entry_key = self._priority_queue[next_queue_id][0]
                self._cache_entries[next_entry_key][0] = next_queue_id + 1
                # Swap positions in the queue
                self._priority_queue[queue_id], self._priority_queue[next_queue_id] = self._priority_queue[next_queue_id], self._priority_queue[queue_id]

                queue_id -= 1
                next_queue_id -= 1

            # Update cache for this entry
            value = self._cache_entries[key][1]
            self._cache_entries[key] = [queue_id, value]

    def retrieve(self, start=None, end=None):
        """
        Retrieves keys, their values and access counters
        NOTE: this may be very slow depending on size
        NOTE: NOT thread safe

        IN:
            start - start position. If None, retrieves from 0
                (Default: None)
            end - end position. If None, retrieves to -1
                (Default: None)

        OUT:
            list with cache entries
        """
        return [
            _CacheEntry(key, self._cache_entries[key][1], access_count)
            for key, access_count in self._priority_queue[start:end]
        ]

### END LFU Cache implementation
### START functools stuff

from functools import wraps

FASTTYPES = {int, str}
KWD_MARK = (object(),)

class _HashedSeq(list):
    """
    This class guarantees that hash() will be called no more than once
    per element.
    """

    __slots__ = "hashvalue"

    def __init__(self, tup, hash=hash):
        self[:] = tup
        self.hashvalue = hash(tup)

    def __hash__(self):
        return self.hashvalue

def _make_key(args, kwargs, typed):
    """
    Make a cache key from optionally typed positional and keyword arguments.
    The key is constructed in a way that is flat as possible rather than
    as a nested structure that would take more memory.
    If there is only a single argument and its data type is known to cache
    its hash value, then that argument is returned without a wrapper.  This
    saves space and improves lookup speed.
    """
    # All of code below relies on kwds preserving the order input by the user.
    # Formerly, we sorted() the kwds before looping. The new way is *much*
    # faster; however, it means that f(x=1, y=2) will now be treated as a
    # distinct call from f(y=2, x=1) which will be cached separately.
    key = args
    if kwargs:
        key += KWD_MARK
        for item in kwargs.items():
            key += item

    if typed:
        key += tuple(type(v) for v in args)
        if kwargs:
            key += tuple(type(v) for v in kwargs.values())

    elif len(key) == 1 and type(key[0]) in FASTTYPES:
        return key[0]

    return _HashedSeq(key)

### END functools stuff
### START decorators

funcs_cache_map = dict()

def create_lfu_cache(limit=128, typed=False):
    """
    Decorator to create LFU cache for a function
    NOTE: Arguments to the cached function must be hashable
    NOTE: The original function can be accessed using the __wrapped__ property
    NOTE: the cache can be accessed using the __cache__ property

    IN:
        limit - max number of entries in the cache,
            If None, the cache can grow infinitely
            (Default: 128)
        typed - whether or not we respect types of parameters,
            which allows more precise caching, but demands more performance
            (Default: False)

    OUT:
        decorated function
    """
    def decorator(func):
        """
        The decorator

        IN:
            func - function

        OUT:
            decorated function
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            The wrapper

            IN:
                args - function position arguments
                kwargs - function keyword arguments

            OUT:
                value returned by the function
            """
            cache = funcs_cache_map[func]
            key = _make_key(args, kwargs, typed)

            if cache.has_cache(key):
                return cache.get(key)

            value = func(*args, **kwargs)
            cache.add(key, value)

            return value

        if func in funcs_cache_map:
            raise Exception("Function '{0}' already has an associated LFU cache object.".format(func))

        cache = LFUCache(limit)
        funcs_cache_map[func] = cache
        setattr(wrapper, "__wrapped__", func)
        setattr(wrapper, "__cache__", cache)

        return wrapper

    return decorator

### End decorators
