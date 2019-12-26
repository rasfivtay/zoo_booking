import typing

from flask import render_template

from webapp.helpers.db_helper import db_conn
from webapp.helpers.geo_helper import Point

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

    return get_hotels_impl(animal, point, distance)


def make_hotel_ref(id):
    return 'http://127.0.0.1:5000/hotel?id=' + id

def make_db_query(
        animal: typing.Optional[str], 
        point: typing.Optional[Point], 
        distance: typing.Optional[int],
    ) -> dict:
    if not point and not animal:
        return {}

    result = {'$and': []}
    
    if point:
        geo_filter = {
            'location':
                { 
                    '$near':
                        {
                            '$geometry': 
                            { 
                                'type': "Point",  
                                'coordinates': [point.lon, point.lat] 
                            }
                        }
                }
        }
        if distance:
            geo_filter['location']['$near']['$maxDistance'] = distance
        result['$and'].append(geo_filter)

    if animal:
        animal_filter = {'animals': animal}
        result['$and'].append(animal_filter)

    return result

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

def get_hotels_impl(animal: str, point: Point, distance):
    conn = db_conn()
    coll = conn.hotels.hotel
    query = make_db_query(animal, point, distance)
    hotels = [hotel for hotel in coll.find(query)]

#    for hotel in hotels:
#        print(hotel)

    return make_response(hotels) 

#print('Check_1')
#get_hotels_impl('cat', Point(55.746437, 38.014696), 100000)
#print('Check_2')
#get_hotels_impl('parrot', Point(55.746437, 38.014696), 100000)