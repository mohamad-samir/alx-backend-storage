#!/usr/bin/env python3
"""
Redis module
"""
import sys
from functools import wraps
from typing import Union, Optional, Callable
from uuid import uuid4

import redis

UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    A decorator to count how many times methods of the Cache class are called.
    :param method:
    :return:
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function
        :param self:
        :param args:
        :param kwargs:
        :return:
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator to add its input parameters to one list in redis,
    and store its output into another list.
    :param method:
    :return:
    """
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function """
        self._redis.rpush(i, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(o, str(res))
        return res

    return wrapper


class Cache:
    """
    Cache redis class
    """

    def __init__(self):
        """
        Constructor of the redis model
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: UnionOfTypes) -> str:
        """
        Generate a random key (e.g., using uuid),
        store the input data in Redis using the random key and return the key.
        :param data:
        :return:
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> UnionOfTypes:
        """
        Convert the data back to the desired format.
        :param key:
        :param fn:
        :return:
        """
        if fn:
            return fn(self._redis.get(key))
        data = self._redis.get(key)
        return data

    def get_int(self, data: bytes) -> int:
        """Get a number"""
        return int.from_bytes(data, sys.byteorder)

    def get_str(self, data: bytes) -> str:
        """Get a string"""
        return data.decode("utf-8")
