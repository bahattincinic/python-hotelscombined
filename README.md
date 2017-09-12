python-hotelscombined
=================================

Python Client for Hotels Combined


## Installation

using pip

    $ pip install python-hotelscombined

or via sources:

    $ wget https://github.com/bahattincinic/python-hotelscombined/archive/python-hotelscombined-xxx.zip
    $ unzip python-hotelscombined-xxx.zip
    $ cd python-hotelscombined-xxx
    $ python setup.py install


## Features

* Static Search
* Autocomplete Search
* Multible Hotel Search
* Single Hotel Search


## To run the tests

    $ nosetests hotels_combined


## Usage

### Autocomplete Search

    from hotels_combined.autocomplete import AutocompleteSearch

    instance = AutocompleteSearch(token='<TOKEN>', debug=True)
    instance.suggest(query='istanbul', languageCode='TR')

### Static Search

    from hotels_combined.static import StaticSearch

    instance = StaticSearch(token='<TOKEN>', debug=True)
    instance.search(query='istanbul eresin')

## Multible Hotel Search

    from hotels_combined.hotel import HotelSearch

    instance = HotelSearch(token='<TOKEN>', debug=True)
    instance.destination_search(destination='Place:Istanbul', session_id='1235',
                                language_code='TR', room=1)

## Basic Multible Hotel Search

    from hotels_combined.hotel import HotelSearch

    instance = HotelSearch(token='<TOKEN>', debug=True)
    instance.basic_destination_search(destination='Place:Istanbul',
                                      session_id='1235',
                                      language_code='TR', room=1)


## Multible Hotel Search Results Summary

    from hotels_combined.hotel import HotelSearch

    instance = HotelSearch(token='<TOKEN>', debug=True)
    instance.destination_search_summary(destination='Place:Istanbul',
                                        session_id='1235',
                                        language_code='TR', room=1)

## Single Hotel Search

    from hotels_combined.hotel import HotelSearch

    instance = HotelSearch(token='<TOKEN>', debug=True)
    instance.single_search(hotel='hotel:Hotel_Sapphire_Istanbul',
                           session_id='1235', language_code='TR', room=1)


## HTTP Response Codes

|       Response Code       |                                                                                                                              Description                                                                                                                             |
|:-------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|           200 OK          |                                                                                     Valid query and response. Note: the answer for a valid query may still contain zero results.                                                                                     |
|        202 Accepted       | Valid query but response is still being processed by the server. This response is returned for queries, such as hotel searches, when the client requests only a complete query results. See the individual API methods for cases when this response may be provided. |
|      400 Bad Request      |                                                                                                        The query is not valid (e.g. check-in after check-out.)                                                                                                       |
| 401 Unauthorized          | The API key is invalid or the User Agent is empty.                                                                                                                                                                                                                   |
| 403 Forbidden             | The user is banned.                                                                                                                                                                                                                                                  |
| 404 Not Found             | The requested place is not searchable or unknown to the system, or the request path is not recognized as part of the API.                                                                                                                                            |
| 500 Internal Server Error | Any other error.                                                                                                                                                                                                                                                     |
