import pymongo
from basemodule import BaseDocument
from utils import log, get_mongodb

ESTADO_ACTIVO = 1
ESTADO_LECTURA = 2
ESTADO_BORRADA = 0

def listas_list(get_p):
    db = get_mongodb()
    return ListasManager(db).lista_de_listas()

class ListasManager(object):
    '''gestor de listas'''
    def __init__(self, db):
        '''recibe db como una conexion a la base de datos para usarla'''
        self.db = db

    def lista_de_listas(self):
        """
        recupera las listas disponibles y las muestra
        """
        listas = self.db.listas.find()
        log.debug("elementos en la lista: %r" % listas.count())
        return "%r" % [Lista(l).show() for l in listas]

    def busca_listas(self,identificador):
        '''
        recupera una lista en base a un elemento pasado como identificador o un diccionario mediante el que filtrar
        '''
        if identificador is None:
            raise ValueError
        if hasattr(identificador,"keys"):  # ducktype dict
            busqueda = identificador
        else:
            busqueda["_id"] = "%s" % identificador  # el identificador sera un string entonces
        
        return "%r" % self.db.listas.find(busqueda)

    def get_lista(self, identificador):
        '''
        Como busca_listas pero solo devuelve 1 elemento
        '''
        res = self.get_items(identificador)
        if res is not None:
            return res[0]
        else:
            return None

    def delete_item(self, list_id, do_remove=False):
        if do_remove:
            self.db.listas.remove({"_id": list_id})
        else:
            self.db.listas.update({"_id":list_id},{"$set":{"estado": ESTADO_BORRADA}})
                                  
        

class Lista(BaseDocument):
    """
    Abstracion entre el documento de mongo y el json de la web
    """
    def hateoas(self):
        hateoas = {
            'list': 'user': '/%s/%s' % (self.__module__, self._id),
            }
        return hateoas
