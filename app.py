# -*- coding: utf-8 -*-
from bottle import route, run, debug, request, abort, redirect
import pymongo
from json import loads, dumps
from importlib import import_module

# string de conexion a la bb.dd. mongodb
MONGODB = "mongodb://localhost"


# Rutas estaticas del server

@route('/')
def index():
    return "Bienvenido a mi pequeña aplicacion, disfruta jugando con ella!"

@route('/register')
def register():
    return "registro de usuario"

@route('/login')
def login():
    return "login"

@route('/logout')
def logout():
    return "login"

@route('/static/<file:path>')
def static(file):
    #TODO: prevent accessing .. or any other thing
    return static_file(file, root='./static/')

@route('/404')
def error_page():
    abort(404,"Sorry! I have none of that")

@route('/400')
def error_method():
    abort(404,
          "Sorry user, but the action you are looking for is in another castle!")


# Rutas dinamicas del server

@route('/<module>/<item:int>/<action>')
def run_action_on_item(module,item,action):
    try:
        m = import_module(module)
    except ImportError:
        redirect('/404')
    action_call = module + '_' + action
    print "DEBUG: tenemos el modulo, ahora llamaremos a %s" % action_call
    try:
        a = getattr(m, action_call)
    except AttributeError, e:  # diferencia entre fallo por modulo o accion
        print "ERROR: module %s doesn't have a %s function" % (module, action_call)
        print "ERROR: %s" % e
        redirect('/400')
    #TODO: añadir autenticacion
    metodo = request.method
    get_p = request.query
    post_p = request.forms
    # por simplificar, pasamos siempre 4 parametros:
    #   - metodo: GET,POST,PUT,DELETE
    #   - item: identificador del elemento
    #   - get_p: parametros de la query (?cosa=otracosa)
    #   - post_p: parametros de post-data
    # por lo que cada funcion debera comprobar que tiene todo
    return a(metodo, item, get_p, post_p)

@route('/<module>/<action>')
def run_action(module,action):
    try:
        m = import_module(module)
    except ImportError:
        redirect('/404')
    action_call = module + '_' + action
    print "DEBUG: tenemos el modulo, ahora llamaremos a %s" % action_call
    try:
        a = getattr(m, action_call)
    except AttributeError, e:  # diferencia entre fallo por modulo o accion
        print "ERROR: module %s doesn't have a %s function" % (module, action_call)
        print "ERROR: %s" % e
        redirect('/400')
    #TODO: añadir autenticacion
    metodo = request.method
    get_p = request.query
    post_p = request.forms
    # por simplificar, pasamos siempre 3 parametros:
    #   - metodo: GET,POST,PUT,DELETE
    #   - get_p: parametros de la query (?cosa=otracosa)
    #   - post_p: parametros de post-data
    # por lo que cada funcion debera comprobar que tiene todo
    return a(metodo, get_p, post_p)


if __name__ == '__main__':
    debug(True)
    run(host='localhost', port='8080', reloader=True)
