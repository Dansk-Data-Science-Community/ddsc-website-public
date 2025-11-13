from functools import wraps
from django.core.cache import cache
import hashlib
import pickle


def make_hash_key(*args, **kwargs):
    pickled_arguments = pickle.dumps((args, kwargs))
    return hashlib.md5(pickled_arguments).hexdigest()


def cache_function_result(timeout: int):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            cache_key = f"function:{func.__name__}"
            result = cache.get(cache_key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout)
            return result

        return inner

    return decorator


def cache_query_result(timeout: int):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            cache_key = f"query:{func.__name__}:{make_hash_key(*args, **kwargs)}"
            result = cache.get(cache_key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout)
            return result

        return inner

    return decorator
