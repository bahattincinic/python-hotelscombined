from base import BaseApi


class AutocompleteSearch(BaseApi):
    """
    Searches for places that might match the string being searched,
    this method is intended for used for
    auto-completion/suggestions in search boxes for place names.
    """

    @property
    def __api_endpoint(self):
        return 'http://www.hotelscombined.com/'

    def suggest(self, query, *args, **kwargs):
        params = {'query': query}
        if kwargs:
            params.update(kwargs)
        return self.__perform_request(url='AutoUniversal.ashx', params=params)
