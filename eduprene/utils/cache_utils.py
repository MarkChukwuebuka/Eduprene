from django.core.cache import cache


class CacheUtil:
    @staticmethod
    def generate_cache_key(prefix, key):
        return f"{prefix}:{key}"

    @staticmethod
    def set_cache_value(prefix, key, value, timeout=None):
        if timeout is None:
            timeout = 600  # Store key for 10 minutes in cache

        cache_key = CacheUtil.generate_cache_key(prefix, key)
        cache.set(cache_key, value, timeout)

        return cache_key

    @staticmethod
    def get_cache_value_or_default(prefix, key, value_callback=None, require_fresh=False, timeout=600):
        data = None
        error = None

        cache_key = CacheUtil.generate_cache_key(prefix, key)

        if not require_fresh:
            data = cache.get(cache_key)

        if not data:
            value_data, error = value_callback

            if value_data is not None:
                data = cache.get_or_set(cache_key, value_data, timeout)
                
        return data, error
