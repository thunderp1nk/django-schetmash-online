from django.core.cache import cache


class CacheWrapper(object):

    ONLINEKASSA_KEY = 'schetmash:token'

    def __init__(self, cache=None):
        self.cache = cache
        if not self.cache:
            raise Exception('no cache driver')

    def set_token(self, token):
        self.cache.set(self.ONLINEKASSA_KEY, token, timeout=60*60*24)

    def get_token(self):
        result = self.cache.get(self.ONLINEKASSA_KEY)
        return result


onlinekassa_cache_wrapper = CacheWrapper(cache=cache)
