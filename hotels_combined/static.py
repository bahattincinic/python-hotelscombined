from base import BaseApi


class StaticSearch(BaseApi):
    """
    The static search finds places and hotels without dates.
    This is the equivalent of the websites universal search.
    """

    def search(self, query, *args, **kwargs):
        params = {'query': query}
        params.update(self._underscore_to_camelcase(kwargs))
        return self._perform_request(url='search/full', params=params)
