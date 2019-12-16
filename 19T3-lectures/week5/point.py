from json import dumps
from flask import Flask, request

from pointutil import fn_get, fn_create, fn_update, fn_delete

APP = Flask(__name__)

@APP.route('/point/get', methods=['GET'])
def get():
    x, y = fn_get()
    return dumps({
        'x' : x,
        'y' : y,
    })

@APP.route('/point/create', methods=['POST'])
def create():
    fn_create(request.form.get('x'), request.form.get('y'))
    return dumps({})

@APP.route('/point/update', methods=['PUT'])
def update():
    fn_update(request.form.get('x'), request.form.get('y'))
    return dumps({})

@APP.route('/point/delete', methods=['DELETE'])
def delete():
    fn_delete()
    return dumps({})

if __name__ == '__main__':
    APP.run(port=20000)


