from bottle import route, run, debug


@route('/')
def index():
    return "Hey!"


if __name__ == '__main__':
    debug(True)
    run(host='localhost', port='8080')
