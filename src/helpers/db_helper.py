import pymongo

class db_conn:
    def __new__(cls):
        if not hasattr(cls, 'conn'):
            cls.conn = pymongo.MongoClient('localhost', 27017)
        return cls.conn
