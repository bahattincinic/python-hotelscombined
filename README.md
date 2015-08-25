python-hotelscombined
=================================

Python Client for Hotels Combined


## Installation

using pip

    $ pip install python-hotelscombined

or via sources:

    $ wget https://github.com/metglobal/python-hotelscombined/archive/python-hotelscombined-xxx.zip
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

## Examples

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
                                languaceCode='TR', room=1)

## Basic Multible Hotel Search

    from hotels_combined.hotel import HotelSearch

    instance = HotelSearch(token='<TOKEN>', debug=True)
    instance.basic_destination_search(destination='Place:Istanbul',
                                      session_id='1235',
                                      languaceCode='TR', room=1)


## Multible Hotel Search Results Summary

    from hotels_combined.hotel import HotelSearch

    instance = HotelSearch(token='<TOKEN>', debug=True)
    instance.destination_search_summary(destination='Place:Istanbul',
                                        session_id='1235',
                                        languaceCode='TR', room=1)

## Single Hotel Search

    from hotels_combined.hotel import HotelSearch

    instance = HotelSearch(token='<TOKEN>', debug=True)
    instance.single_search(hotel='hotel:Hotel_Sapphire_Istanbul',
                           session_id='1235', languaceCode='TR', room=1)