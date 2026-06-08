import os


def cache_size() -> int:
    """Return the cache size"""
    return int(os.environ.get("FANDANGO_CACHE_SIZE", 10_000))
