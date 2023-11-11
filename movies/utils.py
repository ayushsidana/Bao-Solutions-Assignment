from django.core.cache import cache

def get_cached_data(cache_key):
    """
    Retrieve data from the cache using the specified cache key.

    Parameters:
    - cache_key (str): The key to identify the data in the cache.

    Returns:
    - data: The data stored in the cache corresponding to the provided key.
    """
    return cache.get(cache_key)

def set_cached_data(cache_key, data):
    """
    Set data in the cache with the specified cache key.

    Parameters:
    - cache_key (str): The key to identify the data in the cache.
    - data: The data to be stored in the cache.

    Returns:
    None
    """
    cache.set(cache_key, data)
