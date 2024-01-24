#!/usr/bin/env python3
"""Expiring web cache and tracker module"""

import redis
import requests
from typing import Callable
from functools import wraps

redis_connection = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """
    Decorator that wraps around HTTP request functions to provide caching.
    """

    @wraps(method)
    def wrapper(url):
        """Wrapper function for the count_requests decorator."""
        redis_connection = redis.Redis()
        redis_connection.incr(f"count:{url}")
        cached_response = redis_connection.get(url)
        if cached_response:
            return cached_response.decode("utf-8")
        response = method(url)
        redis_connection.set(url, response, 10)
        return response

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    Retrieves a web page, and caches the response for 10 seconds.
    """
    response = requests.get(url)
    return response.text
