import logging
import pymongo
from bottle import abort

from config import DEBUG, MONGO_SAFE, MONGO_DB, MONGO_URL

# gestion de logs
log = logging
LOGLEVEL = log.DEBUG if DEBUG else log.WARNING
log.basicConfig(filename='api.log', level=LOGLEVEL, format='%(asctime)s:%(levelname)s %(message)s')

# establecer conexion a db
def get_mongodb():
    try:
        return pymongo.Connection(MONGO_URL, safe=MONGO_SAFE)[MONGO_DB]
    except pymongo.errors.AutoReconnect,e:
        log.error("Can't connect to the database: %s" % e)
        abort(500, "The database seems off")
