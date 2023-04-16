from fastapi_cache import decorator
from fastapi_cache import TTLCacheBackend

# Create a cache with a max size of 1000 entries and a TTL of 1 hour
cache_backend = TTLCacheBackend(max_size=1000, ttl=3600)

# Create a cache for solutions with the "solutions" cache key
solutions_cache = decorator.cache(
    cache_key="solutions", cache_backend=cache_backend)
