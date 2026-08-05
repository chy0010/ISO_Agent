"""Tiny in-memory TTL cache for the grid data tools.

Real-time ISO data doesn't change faster than its own reporting interval
(MISO/SPP fuel mix and load refresh every ~5 min, EIA is hourly), so a short
cache avoids re-downloading the same dataset for follow-up questions in the
same session without risking meaningfully stale answers.
"""

import time
from functools import wraps


def ttl_cache(seconds: int):
    def decorator(fn):
        cache = {}

        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()
            cached = cache.get(key)
            if cached is not None and now - cached[1] < seconds:
                return cached[0]
            value = fn(*args, **kwargs)
            cache[key] = (value, now)
            return value

        return wrapper

    return decorator
