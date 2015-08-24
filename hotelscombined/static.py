from base import BaseApi


class StaticSearch(BaseApi):
    """
    The static search finds places and hotels without dates.
    This is the equivalent of the websites universal search.
    """

    def search(self, query, *args, **kwargs):
        params = {'query': query}
        if kwargs:
            params.update(kwargs)
        return self.__perform_request(url='search/full', params=params)
