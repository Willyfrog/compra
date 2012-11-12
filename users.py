import pymongo
from basemodule import BaseDocument
from utils import log, get_mongodb
import datetime

ESTADO_ACTIVO = 1
ESTADO_BORRADA = 0

#TODO: gestion de errores de operaciones sobre mongo

def users_list(get_p):
    db = get_mongodb()
    return UsersManager(db).lista_de_listas()

def users_add(get_p, post_p):
    pass

class UsersManager(object):
    '''gestion de usuarios'''

    def __init__(self, db):
        ''' almacena la bb.dd. a usar'''
        self.db = db
  
    def crear_usuario(self, datos):
        datos['fecha_creacion'] = datetime.date.now()
        datos['activo'] = True
        # no se establecen los datos
        # listas, porque no tiene ninguna
        # lastlogin porque no ha hecho login aun


class User(BaseDocument):
    def hateoas(self):
        hateoas = {
            'user': '/%s/%s' % (self.__module__, self._id),
            'friends': '/%s/%s/friends' % (self.__module__, self._id),
            'lists': '/listas/',  # TODO: definir
            'parent': '%s' % self.__module__,
            }
        return hateoas
