# -*- coding: utf-8 -*-
from bottle import route, run, debug, request, abort, redirect,static_file
import pymongo
from json import loads, dumps
from importlib import import_module
from config import log, DEBUG, RELOAD_SERVER
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

@route('/favicon.ico')
def favicon():
    #TODO: prevent accessing .. or any other thing
    return static_file('favicon.ico', root='./static/')

@route('/static/<file:path>')
def static(file):
    #TODO: prevent accessing .. or any other thing
    return static_file(file, root='./static/')

@route('/404')
def error_page():
    abort(404,"Sorry! I have none of that")

@route('/400')
def error_method():
    abort(400,
          "Sorry user, but the action you are looking for is in another castle!")


# Rutas dinamicas del server

def get_module(module_name):
    '''
    recupera el modulo
    '''
    try:
        m = import_module(module_name)
        log.debug("modulo %s cargado" % module_name)
    except ImportError, e:
        log.error("No se pudo importar %s: %s" % (module_name, e))
        m = None
    return m

def call_action(module, action_name, method='GET', get_p=None, post_p=None, item=None):
    '''
    Intenta llamar a la funcion y pasar los parametros apropiados
    '''
    try:
        a = getattr(module, action_name)
    except AttributeError, e:  # diferencia entre fallo por modulo o accion
        log.error( "module %s doesn't have a %s function" % (module.__name__, action_name))
        log.error( "%s" % e)
        redirect('/400')
    #TODO: añadir autenticacion
    # por simplificar, pasamos siempre 4 parametros:
    #   - metodo: GET,POST,PUT,DELETE
    #   - item: identificador del elemento
    #   - get_p: parametros de la query (?cosa=otracosa)
    #   - post_p: parametros de post-data
    # por lo que cada funcion debera comprobar que tiene todo
    if method == "GET":
        if item is None:
            return a(get_p)
        else:
            return a(item, get_p)
    else:
        if item is None:
            return a(method, get_p, post_p)
        else:
            return a(method, item, get_p, post_p)

@route('/<module>')
def run_default_action(module):
    log.debug("run_default_action %s" % module)
    m = get_module(module)
    if m is None:
        redirect('/404')
    #como acciones simples solo se aceptan 2 opciones
    #  - GET: devuelve un listado, pasando por parametros los filtros apropiados
    #  - POST: crea un nuevo elemento
    action = "new" if request.method == "POST" else "list"
    action_call = module + '_' + action
    log.debug( "tenemos el modulo, ahora llamaremos a %s" % action_call)
    return call_action(m,action_call, request.method, request.query, request.forms)

@route('/<module>/<item:int>')
def run_default_action_on_item(module,item):
    log.debug("run_default_action_on_item %s, %s" % module, item)
    m = get_module(module)
    if m is None:
        redirect('/404')
    if request.method == "GET":
        action_call = module + '_show'
    elif request.method == "DELETE":
        action_call = module + "_del"
    elif request.method == "PUT":
        action_call = module + "_modify"
    else:
        redirect('/400')
    log.debug( "DEBUG: tenemos el modulo, ahora llamaremos a %s" % action_call)
    return call_action(m, action_call, request.method, request.query, request.forms,item)

@route('/<module>/<item:int>/<action>')
def run_action_on_item(module,item,action):
    log.debug("run_action_on_item %s, %s, %s" % module, item, action)
    m = get_module(module)
    if m is None:
        redirect('/404')
    action_call = module + '_' + action
    log.debug( "DEBUG: tenemos el modulo, ahora llamaremos a %s" % action_call)
    return call_action(m, action_call, request.method, request.query, request.forms,item)

@route('/<module>/<action>')
def run_module_action(module,action):
    log.debug("run_module_action %s, %s" % module, action)
    m = get_module(module)
    if m is None:
        redirect('/404')
    action_call = module + '_' + action
    log.debug( " Tenemos el modulo, ahora llamaremos a %s" % action_call)
    return call_action(m, action_call, request.method, request.query, request.forms)

if __name__ == '__main__':
    debug(RELOAD_SERVER)
    run(host='localhost', port='8080', reloader=True)
