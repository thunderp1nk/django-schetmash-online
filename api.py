from json import JSONDecodeError

import requests
from django.conf import settings

from onlinekassa.errors import SchetmashJsonError
from onlinekassa.cachewrapper import onlinekassa_cache_wrapper


class SchetmashApi(object):
    _api_root = 'https://online.schetmash.com/lk/{0}'

    def __init__(self):
        self.cache = onlinekassa_cache_wrapper

    @property
    def token(self):
        return self.cache.get_token() if self.cache.get_token() else self.get_token()

    def _request(self, url, method='GET', params=None, json=None):
        request_url = self._api_root.format(url)
        method_list = {
            'GET': (requests.get, {'params': params}),
            'POST': (requests.post, {'params': params, 'json': json}),
        }
        requests_method, kwargs = method_list[method]
        result = requests_method(request_url, **kwargs)
        try:
            return result.json()
        except JSONDecodeError:
            raise SchetmashJsonError(result, self._api_root.format(url))

    def get_token(self):
        result = self._request(
            'api/v1/token',
            method='POST',
            json={
                'login': settings.ONLINEKASSA_LOGIN,
                'password': settings.ONLINEKASSA_LOGIN
            })
        self.cache.set_token(result['token'])
        return result['token']

    def register_receipt(self, data):
        return self._request(
            'api/v1/{0}/sell'.format(12),
            method='POST',
            json=data,
            params={'token': self.token}
        )

    def get_receipt_status(self, ticket_id):
        return self._request(
            'api/v1/{0}/report/{1}'.format(12, ticket_id),
            method='GET',
            params={'token': self.token}
        )


schetmash = SchetmashApi()
