import jwt
import hashlib
from json import dumps
from flask import Flask, request

APP = Flask(__name__)
        
SECRET = 'sempai'

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
    global SECRET
    encoded = jwt.encode({'username': username}, SECRET, algorithm='HS256')
    print(encoded)
    return str(encoded)

def getUserFromToken(token):
    global SECRET
    decoded = jwt.decode(token, SECRET, algorithms=['HS256'])
    return decoded['username']

def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

@APP.route('/secrets', methods=['GET'])
def get():
    if getUserFromToken(request.args.get('token')) is None:
        return sendError('Invalid token')
    return sendSuccess({
        'secrets' : ['I', 'like', 'rats'],
    })

@APP.route('/register', methods=['POST'])
def create():
    data = getData()
    username = request.form.get('username')
    password = request.form.get('password')
    data['users'].append({
        'username': username,
        'password': hashPassword(password),
    })
    print(data)
    return sendSuccess({
        'token': generateToken(username),
    })

@APP.route('/login', methods=['PUT'])
def connect():
    data = getData()
    username = request.form.get('username')
    password = request.form.get('password')
    for user in data['users']:
        if user['username'] == username and user['password'] == hashPassword(password):
            return sendSuccess({
                'token': generateToken(username),
            })
    return sendError('Username or password incorrect')    

if __name__ == '__main__':
    APP.run()

