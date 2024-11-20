import hashlib

CACHE = {}

def get_cache_key(data: str) -> str:
    """
    Generates a unique cache key based on the hash of the input data.

    Args:
        data (str): Input data to hash.

    Returns:
        str: MD5 hash of the input data.
    """
    return hashlib.md5(data.encode()).hexdigest()

def fetch_from_cache(key: str) -> str:
    """
    Fetches the cached result for a given key.

    Args:
        key (str): Cache key.

    Returns:
        str: Cached result or None if not found.
    """
    return CACHE.get(key)

def store_in_cache(key: str, value: str):
    """
    Stores a value in the cache with the given key.

    Args:
        key (str): Cache key.
        value (str): Value to store.
    """
    CACHE[key] = value
