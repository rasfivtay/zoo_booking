import typing

from webapp.helpers.db_helper import db_conn
from webapp.helpers.geo_helper import Point


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

def get_hotels(animal: str, point: Point, distance):
    conn = db_conn()
    coll = conn.hotels.hotel
    query = make_db_query(animal, point, distance)
    hotels = [hotel for hotel in coll.find(query)]

#    for hotel in hotels:
#        print(hotel)

    return hotels

#print('Check_1')
#get_hotels_impl('cat', Point(55.746437, 38.014696), 100000)
#print('Check_2')
#get_hotels_impl('parrot', Point(55.746437, 38.014696), 100000)