from decouple import config

DB_URI = config('DB_URI')

def conn(): # return db_uri_connection_string
    return DB_URI