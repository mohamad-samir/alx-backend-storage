#!/usr/bin/env python3

import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()


def url_access_count(method: Callable) -> Callable:
    """Decorator to track the number of times a URL is accessed."""
    @wraps(method)
    def wrapper(url):
        """Wrapper function."""
        key_count = f"count:{url}"
        redis_store.incr(key_count)
        return method(url)

    return wrapper


def data_cacher(method: Callable) -> Callable:
    """Decorator to cache the result of the get_page function."""
    @wraps(method)
    def invoker(url):
        """Wrapper function for caching."""
        key_result = f"result:{url}"
        cached_value = redis_store.get(key_result)
        if cached_value:
            return cached_value.decode("utf-8")

        result = method(url)
        redis_store.setex(key_result, 10, result)
        return result

    return invoker


@url_access_count
@data_cacher
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL."""
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    print(get_page('http://slowwly.robertomurray.co.uk'))
