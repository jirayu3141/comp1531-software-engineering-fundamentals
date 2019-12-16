from json import dumps
from flask import Flask, request

APP = Flask(__name__)
        
data = {
    'users': [],
}

def getData():
    global data
    return data

def sendSuccess(data):
    return dumps(data)

def sendError(message):
    return dumps({
        '_error' : message,
    })

def generateToken(username):
    return 'example12345abcd'

def getTokenFromPass(password):
    data = getData()
    for user in data['users']:
        if password == user['password']:
            return user['token']
    return None
        #return user


@APP.route('/user/create', methods=['POST'])
def create():
    data = getData()
    password = request.form.get('password')
    secret = request.form.get('secret')
    data['users'].append({
        'password': password,
        'secret': secret,
        'token' : generateToken(password)
    })

    return sendSuccess({
        'token': getTokenFromPass(password),
    })

@APP.route('/user/connect', methods=['PUT'])
def connect():
    data = getData()
    password = request.form.get('password')
    for user in data['users']:
        if user['password'] == password:
            return sendSuccess({
                'token': getTokenFromPass(password),
            })
    return sendError('password does not exist')


@APP.route('/user/secret', methods=['GET'])
def secret():
    data = getData()
    token = request.args.get('token')
    for user in data['users']:
        if user['token'] == token:
            return sendSuccess({
                'secret': user['secret'],
            })
    return sendError('password not matched')

if __name__ == '__main__':
    APP.run(debug=True)

