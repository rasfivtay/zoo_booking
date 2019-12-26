import bson

from helpers.db_helper import db_conn

def get_hotel_by_id(args: dict):
    id = args.get('id')

    if not id:
        return 'No hotel id provided', 400
    
    conn = db_conn()
    coll = conn.hotels.hotel
    try:
        bson_id = bson.ObjectId(id)
    except bson.errors.InvalidId:
        return 'Incorrect hotel id', 400

    query = {'_id': bson_id}
    hotel = coll.find_one(query)

    if not hotel:
        return 'Пыщ Пыщ ололо меня похитил НЛО, Hotel not found', 404

    hotel.pop('_id')
    return hotel

#print(get_hotel_by_id({'id': '5e024b73bc8b282d94ebebb3'}))