#!/usr/bin/env python3
"""Implement an expiring web cache and tracker"""
from datetime import timedelta
from typing import Callable
import requests
from functools import wraps
import redis


def cache_track_response(method: Callable):
    """Cache and track function response"""

    @wraps(method)
    def wrapper(url: str, *args, **kwargs):
        """Implement the caching and tracking"""
        count_key = "count:{}".format(url)
        _redis = redis.Redis()
        _redis.incr(count_key)
        result = method(url, *args, **kwargs)
        _redis.setex(url, timedelta(seconds=10), str(result))
        return result

    return wrapper


@cache_track_response
def get_page(url: str) -> str:
    """Return HTML content of the `url` specified"""
    response = requests.get(url)
    return response.text
