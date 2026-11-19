import os


def cache_size() -> int:
    """Return the number of entries each internal cache may hold"""
    return int(os.environ.get("FANDANGO_CACHE_SIZE", 500))
