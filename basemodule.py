# -*- coding: utf-8 -*-p

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
            res['_methods'] = self.show_methods()

    def show_methods(self):
        """
        Completar en cada objeto con las llamadas apropiadas
        de manera que cada objeto ofrezca la navegacion a interactuar con el
        """
        raise NotImplementedError("Someone forgot to implement me, at least with an empty value")

    def __unicode__():
        """
        Crea la representacion del objeto de cara a mostrarlo
        """
        self.show()
