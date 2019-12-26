import typing

from flask import render_template

from webapp.helpers.geo_helper import Point
from webapp.views.get_hotels import get_hotels as get_hotels_impl

def make_hotel_ref(id):
    return 'http://127.0.0.1:5000/hotel?id=' + id

def make_response(hotels: typing.List):

    result = []
    for hotel in hotels:
        cur_hotel = {
            'url': make_hotel_ref(str(hotel['_id'])),
            'name': hotel['name'],
            'image': hotel.get('main_image'),
            'address': hotel.get('address'),
            'animals': hotel['animals']
        }
        result.append(cur_hotel)

    return render_template('hotels_list.html', hotels=result)


def get_hotels(args: dict):
    animal = args.get('animal')
    point = None
    try:
        lat = float(args.get('lat'))
        lon = float(args.get('lon'))
        if lat and lon:
            point = Point(lat=lat, lon=lon)
    except (ValueError, TypeError):
        pass

    distance = None
    try:
        distance = int(args.get('dist'))
    except (ValueError, TypeError):
        pass

    return make_response(get_hotels_impl(animal, point, distance))
