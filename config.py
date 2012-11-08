import logging
import sys
import pymongo
from bottle import abort

# estamos debuggeando?
DEBUG = True
RELOAD_SERVER = True

# gestion de logs
log = logging
LOGLEVEL = log.DEBUG if DEBUG else log.WARNING
log.basicConfig(filename='api.log', level=LOGLEVEL, format='%(asctime)s:%(levelname)s %(message)s')

# string de conexion a la bb.dd. mongodb
MONGO_URL = "mongodb://localhost"
MONGO_SAFE = True  # Safe mode
MONGO_DB = "compra"

def get_mongodb():
    try:
        return pymongo.Connection(MONGO_URL, MONGO_SAFE)[MONGO_DB]
    except pymongo.errors.AutoReconnect,e:
        log.error("Can't connect to the database: %s" % e)
        abort(500, "The database seems off")
