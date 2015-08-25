import unittest
import httpretty
import json
import re

from hotels_combined.base import BaseApi
from hotels_combined.autocomplete import AutocompleteSearch
from hotels_combined.exceptions import QueryException
from hotels_combined.static import StaticSearch
from hotels_combined.hotel import HotelSearch


class BaseApiTestCase(unittest.TestCase):

    def test_token(self):
        instance = BaseApi(token='123456')
        self.assertEqual(instance.token, '123456')

    def test_version(self):
        instance = BaseApi(token='123456', version='2.0')
        self.assertEqual(instance.version, '2.0')

    def test_debug(self):
        instance = BaseApi(token='123456', version='2.0', debug=False)
        self.assertEqual(instance.debug, False)

    def test_api_endpoint(self):
        instance = BaseApi(token='123456', version='2.0', debug=False)
        live_url = '%s2.0' % instance.live_api_root
        self.assertEqual(instance._api_endpoint, live_url)

        instance = BaseApi(token='123456', version='2.0', debug=True)
        sandbox_url = '%s2.0' % instance.sandbox_api_root
        self.assertEqual(instance._api_endpoint, sandbox_url)

    @httpretty.activate
    def test_perform_request(self):
        instance = BaseApi(token='123456', version='2.0', debug=True)

        url = 'http://sandbox.hotelscombined.com/api/2.0/'
        httpretty.register_uri(
            httpretty.GET,
            re.compile(url + 'test/200?(\w+)'),
            body=json.dumps({'test': 'ok'}),
            content_type="application/json",
            status=200
        )
        httpretty.register_uri(
            httpretty.GET,
            re.compile(url + 'test/400?(\w+)'),
            body=json.dumps({'test': 'fail'}),
            content_type="application/json",
            status=400
        )
        self.assertEqual(instance._perform_request('test/200', {}),
                         {'test': 'ok'})
        self.assertEqual(httpretty.last_request().querystring,
                         {'apiKey': ['123456']})
        self.assertRaises(QueryException, instance._perform_request,
                          url='test/400', params={})

        instance.token = ''
        self.assertRaises(QueryException, instance._perform_request,
                          url='test/500', params={})


class AutocompleteSearchTestCase(unittest.TestCase):

    def setUp(self):
        self.response = [{"cc": "TR", "n": "Istanbul", "k": "pla",
                          "ce": "Istanbul",
                          "hc": "3592", "h": "3,592 hotels", "s": 1,
                          "p": ["Turkey"], "ri": 0, "si": -876239730,
                          "t": "cities", "tn": "Cities"}]
        self.instance = AutocompleteSearch(token='123456')
        self.url = 'http://www.hotelscombined.com/AutoUniversal.ashx?(\w+)'

    @httpretty.activate
    def test_suggest(self):
        httpretty.register_uri(
            httpretty.GET,
            re.compile(self.url),
            body=json.dumps(self.response),
            content_type="application/json",
            status=200
        )

        self.assertEqual(len(self.instance.suggest('istanbul')), 1)
        self.assertEqual(httpretty.last_request().querystring,
                         {'search': ['istanbul'], 'apiKey': ['123456']})
        self.assertEqual(httpretty.last_request().method, 'GET')

    @httpretty.activate
    def test_extra_params(self):
        httpretty.register_uri(
            httpretty.GET,
            re.compile(self.url),
            body=json.dumps(self.response),
            content_type="application/json",
            status=200
        )
        self.instance.suggest(query='istanbul', limit=5, languageCode='EN')
        self.assertEqual(httpretty.last_request().querystring,
                         {'search': ['istanbul'], 'apiKey': ['123456'],
                          'limit': ['5'], 'languageCode': ['EN']})

    def test_api_endpoint(self):
        self.assertEqual(self.instance._api_endpoint,
                         'http://www.hotelscombined.com')


class StaticSearchTestCase(unittest.TestCase):

    def setUp(self):
        self.instance = StaticSearch(token='123456', debug=True)
        self.response = [{"id": "place:Istanbul", "name": "Istanbul",
                          "type": 2, "typeName": "Cities",
                          "placeName": "Turkey",
                          "hotelCount": 3592,
                          "isSearchable": "true"}]
        self.url = self.instance._api_endpoint + '/search/full?(\w+)'

    @httpretty.activate
    def test_search(self):
        httpretty.register_uri(
            httpretty.GET,
            re.compile(self.url),
            body=json.dumps(self.response),
            content_type="application/json",
            status=200
        )
        self.assertEqual(len(self.instance.search('istanbul')), 1)
        self.assertEqual(httpretty.last_request().querystring,
                         {'query': ['istanbul'], 'apiKey': ['123456']})

    @httpretty.activate
    def test_extra_params(self):
        httpretty.register_uri(
            httpretty.GET,
            re.compile(self.url),
            body=json.dumps(self.response),
            content_type="application/json",
            status=200
        )
        self.instance.search(query='istanbul', limit=5, languageCode='EN')
        self.assertEqual(httpretty.last_request().querystring,
                         {'query': ['istanbul'], 'apiKey': ['123456'],
                          'limit': ['5'], 'languageCode': ['EN']})

    @httpretty.activate
    def test_search_error(self):
        httpretty.register_uri(
            httpretty.GET,
            re.compile(self.url),
            body=json.dumps(self.response),
            content_type="application/json",
            status=400
        )
        self.assertRaises(QueryException, self.instance.search,
                          query='istanbul')


class HotelSearchTestCase(unittest.TestCase):

    def setUp(self):
        self.instance = HotelSearch(token='123456', debug=True)

    def _assertQuerystring(self, querstring, limit=None, page=None, **kwargs):
        self.assertEqual(querstring['pageSize'], [limit or '25'])
        self.assertEqual(querstring['pageIndex'], [page or '0'])
        self.assertEqual(querstring['sortDirection'], ['descending'])
        self.assertEqual(querstring['SortField'], ['popularity'])
        self.assertEqual(querstring['apiKey'], [self.instance.token])
        for key, val in kwargs.items():
            self.assertEqual(querstring[key], [val])

    def test_int_or_default(self):
        self.assertEqual(self.instance._int_or_default('dfd', 1), 1)
        self.assertEqual(self.instance._int_or_default(2, 1), 2)
        self.assertEqual(self.instance._int_or_default('2/', 1), 1)
        self.assertEqual(self.instance._int_or_default('-2', 1), 2)

    def test_default_build_query(self):
        query = self.instance._build_query(query={})
        self.assertEqual(query['pageSize'], 25)
        self.assertEqual(query['pageIndex'], 0)
        self.assertEqual(query['sortDirection'], 'descending')
        self.assertEqual(query['SortField'], 'popularity')

    def test_build_query(self):
        query = self.instance._build_query(query={}, limit=20, page=1,
                                           order_by='-id')
        self.assertEqual(query['pageSize'], 20)
        self.assertEqual(query['pageIndex'], 1)
        self.assertEqual(query['sortDirection'], 'descending')
        self.assertEqual(query['SortField'], 'id')

    @httpretty.activate
    def test_destination_search(self):
        url = self.instance._api_endpoint + '/hotels?(\w+)'
        response = [{"id": "place:Istanbul"}]
        httpretty.register_uri(
            httpretty.GET,
            re.compile(url),
            body=json.dumps(response),
            content_type="application/json",
            status=200
        )
        self.assertEqual(
            len(self.instance.destination_search('istanbul', 'fdfdf')),
            1
        )
        self.assertEqual(
            self.instance.destination_search('istanbul', 'fdfdf', page=2)[0],
            {"id": "place:Istanbul"}
        )
        self._assertQuerystring(httpretty.last_request().querystring,
                                destination='istanbul', page='2')

    @httpretty.activate
    def test_basic_destination_search(self):
        url = self.instance._api_endpoint + '/hotels/basic?(\w+)'
        response = [{"name": "place:Ankara"}]
        httpretty.register_uri(
            httpretty.GET,
            re.compile(url),
            body=json.dumps(response),
            content_type="application/json",
            status=200
        )
        self.assertEqual(
            len(self.instance.basic_destination_search('ankara', 'fdfdf')),
            1
        )
        self.assertEqual(
            self.instance.basic_destination_search('ankara', 'fdfdf')[0],
            {"name": "place:Ankara"}
        )
        self._assertQuerystring(httpretty.last_request().querystring,
                                destination='ankara')

    @httpretty.activate
    def test_destination_search_summary(self):
        url = self.instance._api_endpoint + '/hotels/summary?(\w+)'
        response = {"totalResults": 3591, "totalFilteredResults": 0,
                    "currencyCode": "TRY", "languageCode": "EN"}
        httpretty.register_uri(
            httpretty.GET,
            re.compile(url),
            body=json.dumps(response),
            content_type="application/json",
            status=200
        )
        result = self.instance.destination_search_summary(
            'ankara', 'fdfdf', languageCode='TR')
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result.keys()), 4)
        self._assertQuerystring(httpretty.last_request().querystring,
                                destination='ankara', languageCode='TR')

    @httpretty.activate
    def test_single_search(self):
        url = self.instance._api_endpoint + '/hotel?(\w+)'
        response = {"name": "place:Ankara"}
        httpretty.register_uri(
            httpretty.GET,
            re.compile(url),
            body=json.dumps(response),
            content_type="application/json",
            status=200
        )
        result = self.instance.single_search(
            'four seasons hotel', 'fdfdf', languageCode='EN')
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result.keys()), 1)
        self._assertQuerystring(httpretty.last_request().querystring,
                                hotel='four seasons hotel', languageCode='EN')
