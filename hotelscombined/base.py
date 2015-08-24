# -*- coding: utf-8 -*-
import requests
import json
try:
    from urlparse import urljoin
except:
    from urllib.parse import urljoin

from .exceptions import TokenException, QueryException


class BaseAPi(object):
    token = ""
    version = ""
    debug = False
    live_api_root = "http://hotelscombined.com/api/"
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
    def __api_endpoint(self):
        if self.debug:
            return urljoin(self.sandbox_api_root, self.version)
        return urljoin(self.live_api_root, self.version)

    def __perform_request(self, url, params, method='GET'):
        if not self.token:
            raise TokenException("No token provided. Please use a valid token")

        if not isinstance(params, dict):
            raise QueryException("invalid params.")

        payload = {'apiKey': self.token}
        payload.update(params)

        url = urljoin(self.__api_endpoint(), url)
        headers = {'Content-type': 'application/json',
                   'Accept': 'application/json'}
        response = requests.request(method, url, params=payload,
                                    headers=headers)

        if response.status_code == 401:
            raise TokenException("Please use a valid token",
                                 errors=response.content)

        if response.status_code in (400, 404):
            raise QueryException("The query/url is not valid",
                                 errors=response.content)

        return json.load(response.content)
