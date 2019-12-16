import threading
import os
import pickle
from json import dumps
from flask import Flask, request

APP = Flask(__name__)

data = {
    "names" : [],
}
if os.path.exists('dataStore.p'):
    data = pickle.load(open('dataStore.p', 'rb'))

def save():
    global data
    print("Saving!")
    with open('dataStore.p', 'wb') as FILE:
        pickle.dump(data, FILE)

def timerAction():
    timer = threading.Timer(1.0, timerAction)
    timer.start() 
    save()
timerAction()
        
@APP.route('/names', methods=['GET'])
def get():
    global data
    return dumps({
        'names' : data['names'],
    })

@APP.route('/add', methods=['POST'])
def create():
    global data
    data['names'].append(request.form.get('name'))
    return dumps({})

if __name__ == '__main__':
    APP.run(port=20000)

