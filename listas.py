import pymongo

def listas_listas():
    return "funciona!"

class Listas(object):
    '''gestor de listas'''
    def __init__(self, db):
        self.db = db
