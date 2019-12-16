"""
Run the flask server, and access /go to start the timer.
While the timer is valid, all calls to /check will
return "Still happening!", and then once the timer
is complete, it will return "Done" instead
"""

import datetime
from flask import Flask

APP = Flask(__name__)

timer = None

def timerStart():
    global timer
    timer = datetime.datetime.now()

def timerGoing():
    global timer
    now = datetime.datetime.now()
    return (now - timer).total_seconds() < (5)

@APP.route('/go')
def go():
    timerStart()
    return "Starting"

@APP.route('/check')
def check():
    if timerGoing():
        return "Still happening!"
    else:
        return "Done"

if __name__ == '__main__':
    APP.run()
