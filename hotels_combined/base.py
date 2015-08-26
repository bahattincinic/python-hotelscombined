# -*- coding: utf-8 -*-
import requests
import json
import re
try:
    from urlparse import urljoin
except:
    from urllib.parse import urljoin

from .exceptions import QueryException


class BaseApi(object):
    live_api_root = "https://hotelscombined.com/api/"
    sandbox_api_root = "http://sandbox.hotelscombined.com/api/"

    def __init__(self, token, version='1.0', debug=False, *args, **kwargs):
        self.token = token
        self.version = version
        self.debug = debug

    def __str__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.token)

    def __unicode__(self):
        return u"%s" % self.__str__()

    @property
    def api_endpoint(self):
        if self.debug:
            return urljoin(self.sandbox_api_root, self.version)
        return urljoin(self.live_api_root, self.version)

    def _perform_request(self, url, params, method='GET'):
        if not self.token:
            raise QueryException("No token provided. Please use a valid token")

        payload = {'apiKey': self.token}
        payload.update(params)

        url = '%s/%s' % (self.api_endpoint, url)
        headers = {'Content-type': 'application/json',
                   'Accept': 'application/json'}
        response = requests.request(method, url, params=payload,
                                    headers=headers)

        errors = {
            '400': 'The query is not valid (e.g. check-in after check-out.)',
            '401': 'The API key is invalid or the User Agent is empty.',
            '403': 'The user is banned.',
            '404': 'The requested place is not searchable or unknown to '
                   'the system, or the request path is not recognized '
                   'as part of the API.',
            '500': 'Any other error.'
        }

        if str(response.status_code) in errors.keys():
            raise QueryException(errors[str(response.status_code)],
                                 errors=response.content,
                                 status_code=response.status_code)

        return json.loads(response.content)

    def _to_camelcase(self, value):
        return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), value)

    def _underscore_to_camelcase(self, context):
        """
        Convert underscore to CamelCase.

        For example:
            >>> {'language_code': 'TR'} ==> {'languageCode': 'TR'}
        """
        return {
            self._to_camelcase(key): val
            for key, val in context.items()
        }
