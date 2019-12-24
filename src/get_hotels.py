import typing

from helpers.db_helper import db_conn
from helpers.geo_helper import Point

def make_db_query(
        animal: typing.Optional[str], 
        point: typing.Optional[Point], 
        distance: typing.Optional[int],
    ) -> dict:
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

    return {
        'hotels': get_hotels_impl(
            animal, point, distance,
        )
    }

def get_hotels_impl(animal: str, point: Point, distance):
    conn = db_conn()
    coll = conn.hotels.hotel
    query = make_db_query(animal, point, distance)
    response = [hotel for hotel in coll.find(query)]

    for hotel in response:
        hotel = hotel.pop('_id')

#    for hotel in response:
#        print(hotel['name'])

    return response 

#print('Check_1')
#get_hotels_impl('cat', Point(55.746437, 38.014696), 100000)
#print('Check_2')
#get_hotels_impl('parrot', Point(55.746437, 38.014696), 100000)