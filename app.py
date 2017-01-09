import moblee.controller as controller
from bottle import route, run, request, static_file


@route('/getdata', method="GET")
def getdata():
    controller.prepare_data()


@route('/', method="GET")
def page():
    return static_file("index.html", root="template")


@route('/stack_moblee/v1/question', method="GET")
def search():
    return controller.get_data(request)


run(host='localhost', port=8080, debug=True, reloader=True)
