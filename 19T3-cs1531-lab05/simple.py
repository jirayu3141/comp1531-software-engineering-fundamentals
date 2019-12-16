from flask import Flask, request
from json import dumps

APP = Flask(__name__)

data = {
    'users' : []
}

def getData():
    global data
    return data

@APP.route('/name/add', methods=['POST'])
def add():
    data = getData()
    name = request.form.get('name')
    data['users'].append(name)
    return dumps({})

@APP.route('/names', methods=['GET'])
def get():
    data = getData()
    return dumps({
        'names' : data['users']
    })

@APP.route('/delete', methods=['DELETE'])
def delete():
    data = getData()
    name = request.form.get('name')
    fn_delete(name)
    return dumps({})


def fn_delete(name):
    data = getData()
    for user in data['users']:
        if name == user:
            data['users'].remove(name)

if __name__ == "__main__":
    APP.run(debug = True)

