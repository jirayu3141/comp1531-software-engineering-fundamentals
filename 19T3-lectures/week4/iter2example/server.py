from json import dumps
from flask import Flask, request

from search import search_fn

APP = Flask(__name__)

@APP.route('/search', methods=['GET'])
def search():
    return dumps(search_fn(request.args.get('token'), request.args.get('query_str')))

if __name__ == '__main__':
    APP.run()
