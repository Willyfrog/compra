# -*- coding: utf-8 -*-

class BaseDocument(object):
    """
    Establece las funciones basicas para la abstraccion del documento
    de mongodb y el json usado para la api
    """

    def __init__(self, document):
        """
        guarda el documento para su uso posterior

        Arguments:
        - `document`:
        """
        self._document = document

    def __getattr__(self, name):
        """
        si no es un atributo que ya tuvieramos definido
        buscamos en _document para devolverlo
        Esto nos permite acceder a los atributos del documento
        """
        if name in self._document:
            return self._document['name']
        else:
            raise AttributeError("%r object has no attribute %r" %
                                 (type(self)._name, name))

    def save(self,db,fields=[]):
        """
        Almacena en base de datos
        Arguments:
        - `db`: mongodb donde guardar los datos
        - `fields`: si tiene valor, solo se actualizan las claves indicadas
        """
        keys = self._document.keys()
        datos = dict()
        if len(fields)>0:
            field_list = fields
        else:
            field_list = keys
        for f in field_list:
            if f in keys:
                datos[f] = self._document[f]
        col = getattr(db,self.__module__)  # funcionara al heredar la clase?
        if len(fields>0):
            col.update({'_id':self._document._id},{'$set':datos})
        else:
            col.update({'_id':self._document._id},datos)


    def show(self, showonly=None):
        """
        Muestra el objeto completo si no se le pasan parametros
        o solo los seleccionados si showonly es dtto de None

        Arguments:
        - `showonly`:
        """
        res = dict()
        for key in self._document.keys():
            if key!="_id":  # nos saltamos esta que no le interesa al usuario
                if showonly is None or getattr(showonly,key,False):
                    res[key] = self._document[key]
        if showonly is None or getattr(showonly,'_methods',False):
            res['_methods'] = self.hateoas()

    def hateoas(self):
        """
        Hypertext as the engine of application state
        das los enlaces para facilitar la navegacion (padre, hijos, el propio elemento, lo que haga falta donde se apliquen los metodos de http)
        """
        raise NotImplementedError("Someone forgot to implement me, I don't even have an empty value")

    def __unicode__(self):
        """
        Crea la representacion del objeto de cara a mostrarlo
        """
        self.show()

    def __str__(self):
        '''
        Recupera de unicode la representacion
        '''
        return unicode(self).encode('utf-8')
