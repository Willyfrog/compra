import pymongo
from basemodule import Document

def listas_listas():
    return "funciona!"

class Listas(object):
    '''gestor de listas'''
    def __init__(self, db):
        '''recibe db como una conexion a la base de datos para usarla'''
        self.db = db

        def list():
            """
            """

class Lista(BaseDocument):
    """
    Abstracion entre el documento de mongo y el json de la web
    """
    def show_methods(self):
        return dict('delete': 'DELETE /%s/%s/%s' % (self.__module__,))
