import pymongo

class db_conn:
    def __new__(cls, host: str = 'localhost', port: int = 27017):
        if not hasattr(cls, 'conn'):
            cls.conn = pymongo.MongoClient(host, port)
        return cls.conn
