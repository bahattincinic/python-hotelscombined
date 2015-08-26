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

    def test_to_camelcase(self):
        self.assertEqual(self.instance._to_camelcase('language_code'),
                         'languageCode')
        self.assertEqual(self.instance._to_camelcase('min_price'),
                         'minPrice')
        self.assertEqual(self.instance._to_camelcase('checkin'),
                         'checkin')
        self.assertEqual(self.instance._to_camelcase(
            'include_local_taxes_in_total'), 'includeLocalTaxesInTotal')

    def test_underscore_to_camelcase(self):
        self.assertEqual(self.instance._underscore_to_camelcase(
            {'language_code': 'TR'}), {'languageCode': 'TR'})
        self.assertEqual(self.instance._underscore_to_camelcase(
            {'language_code': 'TR', 'checkin': '323'}),
            {'languageCode': 'TR', 'checkin': '323'})

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
            self.instance.destination_search(
                'istanbul', 'fdfdf', page_size=2)[0],
            {"id": "place:Istanbul"}
        )

        querystring = httpretty.last_request().querystring
        self.assertEqual(querystring['destination'], ['istanbul'])
        self.assertEqual(querystring['pageSize'], ['2'])

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

        querystring = httpretty.last_request().querystring
        self.assertEqual(querystring['destination'], ['ankara'])

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
            'ankara', 'fdfdf', language_code='TR')

        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result.keys()), 4)

        querystring = httpretty.last_request().querystring
        self.assertEqual(querystring['destination'], ['ankara'])
        self.assertEqual(querystring['languageCode'], ['TR'])

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
            'four seasons hotel', 'fdfdf', language_code='EN')

        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result.keys()), 1)

        querystring = httpretty.last_request().querystring
        self.assertEqual(querystring['hotel'], ['four seasons hotel'])
        self.assertEqual(querystring['sessionID'], ['fdfdf'])
        self.assertEqual(querystring['languageCode'], ['EN'])
