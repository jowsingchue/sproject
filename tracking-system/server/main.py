from bottle import route, run

@route('/hello', method='GET')
def hello_get():
    return "Hello World!"

@route('/hello', method='POST')
def hello_post():
    return "Hello World!"


run(host='localhost', port=8080, debug=True)