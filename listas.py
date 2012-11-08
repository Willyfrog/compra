import pymongo
from basemodule import BaseDocument
from config import log, get_mongodb

def listas_list(get_p):
    db = get_mongodb()
    return Listas(db).get_list()

class Listas(object):
    '''gestor de listas'''
    def __init__(self, db):
        '''recibe db como una conexion a la base de datos para usarla'''
        self.db = db

        def get_list():
            """
            recupera las listas disponibles y las muestra
            """
            listas = self.db.listas.find()
            return [Lista(l) for l in listas]

class Lista(BaseDocument):
    """
    Abstracion entre el documento de mongo y el json de la web
    """
    def show_methods(self):
        return {'show': 'GET /%s/%s' % (self.__module__, self._id),
            'delete': 'DELETE /%s/%s' % (self.__module__, self._id)}
