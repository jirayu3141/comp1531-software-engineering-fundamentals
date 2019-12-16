from werkzeug.exceptions import HTTPException

class ValueError_http(HTTPException):
    code = 400
    message = 'No message specified'
class AccessError(HTTPException):
    code = 404
    message = 'No message specified'

# class ValueError_http(Exception):
#     code = 400
#     message = 'No message specified'
#     pass
# class AccessError(Exception):
#     code = 404
#     message = 'No message specified'
#     pass