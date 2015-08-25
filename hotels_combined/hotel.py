from base import BaseApi


class HotelSearch(BaseApi):
    """
    The hotel search returns rates and availability for hotels
    matching the criteria.
    """

    def destination_search(self, destination, session_id,
                           order_by=None, page=None,
                           limit=None, *args, **kwargs):
        """
        The multiple hotel search returns summary details and rates
        for hotels within a place.

        :param destination str  (Example: place:Istanbul)
        :param session_id str
        :param order_by str (consumerRating, distance, name, minRate,
                             popularity, rating)
        :param page int (default 0)
        :param limit int (default 25)
        """
        params = {'destination': destination, 'sessionID': session_id}
        params = self._build_query(params, order_by=order_by, page=page,
                                   limit=limit, **kwargs)

        return self._perform_request(url='hotels', params=params)

    def basic_destination_search(self, destination, session_id,
                                 order_by=None, page=None,
                                 limit=None, *args, **kwargs):
        """
        The basic multiple hotel search returns very basic summary details
        and rates for hotels within a place.

        :param destination (Example: place:Istanbul)
        :param session_id str
        :param order_by str (consumerRating, distance, name, minRate,
                             popularity, rating)
        :param page int (default 0)
        :param limit int (default 25)
        """
        params = {'destination': destination, 'sessionID': session_id}
        params = self._build_query(params, order_by=order_by, page=page,
                                   limit=limit, **kwargs)

        return self._perform_request(url='hotels/basic', params=params)

    def destination_search_summary(self, destination, session_id,
                                   order_by=None, page=None,
                                   limit=None, *args, **kwargs):
        """
        The multiple hotel search summary returns the metadata portion of the
        results returned by the Multiple Hotel Search method without returning
        hotels or rates. This is useful for updating hotel counts as a user
        changes filters without having to load the full result set
        until they have applied all the filters they wish to.

        :param destination (Example: place:Istanbul)
        :param session_id str
        :param order_by str (consumerRating, distance, name, minRate,
                             popularity, rating)
        :param page int (default 0)
        :param limit int (default 25)
        """
        params = {'destination': destination, 'sessionID': session_id}
        params = self._build_query(params, order_by=order_by, page=page,
                                   limit=limit, **kwargs)

        return self._perform_request(url='hotels/summary', params=params)

    def single_search(self, hotel, session_id, order_by=None,
                      page=None, limit=None, *args, **kwargs):
        """
        The single hotel search returns the full details for a single hotel
        and all available rates for the given criteria. This would
        typically be called when a user selects a hotel from the
        results of the multiple hotel search.

        :param hotel (Example: hotel:Hotel_Sapphire_Istanbul)
        :param session_id str
        :param order_by str (consumerRating, distance, name, minRate,
                             popularity, rating)
        :param page int (default 0)
        :param limit int (default 25)
        """
        params = {'hotel': hotel, 'sessionID': session_id}
        params = self._build_query(params, order_by=order_by, page=page,
                                   limit=limit, **kwargs)

        return self._perform_request(url='hotel', params=params)

    def _int_or_default(self, value, default):
        try:
            value = abs(int(value))
        except (ValueError, TypeError):
            value = default
        return value

    def _build_query(self, query, **kwargs):
        # the default is 25
        query['pageSize'] = self._int_or_default(kwargs.pop('limit', 25), 25)
        # the default is 0
        query['pageIndex'] = self._int_or_default(kwargs.pop('page', 0), 0)

        # The default is popularity.
        order_by = kwargs.pop('order_by', '-popularity') or '-popularity'
        if order_by.startswith('-'):
            query['sortDirection'] = 'descending'
            query['SortField'] = order_by.split('-')[1]
        else:
            query['sortDirection'] = 'ascending'
            query['SortField'] = order_by

        query.update(kwargs)
        return query
