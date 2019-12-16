"""Flask server"""
import sys
sys.path.insert(0, 'server')
from werkzeug.exceptions import HTTPException
from data_structure import sendSuccess, data, getUserFromToken
from functions_message import *
from functions_channel import *
from functions_auth import *
from functions_user import *
from functions_standup import *
from functions_others import *
from flask import Flask, request, jsonify, send_from_directory
from flask_mail import Mail, Message
from json import dumps
from flask_cors import CORS

def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.description,
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__, static_url_path='/static/')
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(HTTPException, defaultHandler)
CORS(APP)

@APP.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('', path)

''' AUTH FUNCTIONS '''
@APP.route('/auth/register', methods=['POST'])
def register_auth():
    # arguments
    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')

    registerDict = auth_register(email, password, name_first, name_last)
    return sendSuccess({
        'u_id': registerDict['u_id'],
        'token': str(registerDict['token']),
    })


@APP.route('/auth/login', methods=['POST'])
def login_auth():
    loginDict = auth_login(request.form.get(
        'email'), request.form.get('password'))

    return sendSuccess({
        'u_id': loginDict['u_id'],
        'token': str(loginDict['token'])
    })


@APP.route('/auth/logout', methods=['POST'])
def logout_auth():
    is_success = auth_logout(request.form.get('token'))
    return sendSuccess({'is_success' : is_success})

APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'two.oh.oh@gmail.com',
    MAIL_PASSWORD = "Brain_Is_Found"
)

@APP.route('/auth/passwordreset/request', methods=['POST'])
def passwordreset_request_auth():
    email = request.form.get('email')
    foundUser = getUserByEmail(email)
    if foundUser == None:
        return ValueError("Email is not registered.")
    reset_code = auth_passwordreset_request(email)
    mail = Mail(APP)
    try:
        msg = Message("Send reset code!",
            sender="my.gmail@gmail.com",
            recipients=[email])   #change it to the valid user's email address
        msg.body = "Reset code is: " + reset_code 
        mail.send(msg)
        return 'Mail sent!'
    except Exception as e:
        return (str(e))

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def password_reset_auth():
    auth_passwordreset_reset(request.form.get('reset_code'), request.form.get('new_password'))
    return dumps({})


# ''' Message Functions '''
@APP.route('/message/sendlater', methods=['POST'])
def msg_send_later():
    channel_id = int(request.form.get('channel_id'))
    message_sendlater(request.form.get('token'), channel_id, request.form.get(
        'message'), request.form.get('time_sent'))
    return sendSuccess({})


@APP.route('/message/send', methods=['POST'])
def msg_send():
    channel_id = int(request.form.get('channel_id'))
    msg_dict = message_send(request.form.get('token'), channel_id,
                 request.form.get('message'))
    return sendSuccess(msg_dict)


@APP.route('/message/remove', methods=['DELETE'])
def msg_remove():
    message_id = int(request.form.get('message_id'))
    message_remove(request.form.get('token'), message_id)
    return sendSuccess({})


@APP.route('/message/edit', methods=['PUT'])
def msg_edit():
    message_edit(request.form.get('token'), int(request.form.get('message_id')), request.form.get('message'))
    return sendSuccess({})


@APP.route('/message/react', methods=['POST'])
def react():
    message_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    message_react(request.form.get('token'), message_id, react_id)
    return sendSuccess({})


@APP.route('/message/unreact', methods=['POST'])
def unreact():
    message_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    message_unreact(request.form.get('token'), message_id, react_id)
    return sendSuccess({})


@APP.route('/message/pin', methods=['POST'])
def pin():
    message_id = int(request.form.get('message_id'))
    message_pin(request.form.get('token'), message_id)
    return sendSuccess({})


@APP.route('/message/unpin', methods=['POST'])
def unpin():
    message_id = int(request.form.get('message_id'))
    message_unpin(request.form.get('token'), message_id)
    return sendSuccess({})


# ''' Channel Functions '''


@APP.route('/channel/invite', methods=['POST'])
def invite_channel():
    channel_id = int(request.form.get('channel_id'))
    channel_invite(request.form.get('token'),
                   channel_id, int(request.form.get('u_id')))
    return sendSuccess({
    })


@APP.route('/channel/details', methods=['GET'])
def details_channel():
    channel_id = int(request.args.get('channel_id'))
    details = channel_details(request.args.get('token'), channel_id)
    return sendSuccess(
        details
    )

@APP.route('/channel/messages', methods=['GET'])
def messages_channel():
    channel_id = int(request.args.get('channel_id'))
    #channel_id = 1
    #print('ch_id is :{channel_id}')
    messages = channel_messages(request.args.get(
        'token'), channel_id, int(request.args.get('start')))
    return sendSuccess(
        messages
    )


@APP.route('/channel/leave', methods=['POST'])
def leave_channel():
    channel_id = int(request.form.get('channel_id'))
    channel_leave(request.form.get('token'), channel_id)
    return sendSuccess({
    })


@APP.route('/channel/join', methods=['POST'])
def join_channel():
    channel_id = int(request.form.get('channel_id'))
    channel_join(request.form.get('token'), channel_id)
    return sendSuccess({
    })


@APP.route('/channel/addowner', methods=['POST'])
def addowner_channel():
    channel_id = int(request.form.get('channel_id'))
    channel_addowner(request.form.get('token'),
                     channel_id, int(request.form.get('u_id')))
    return sendSuccess({
    })


@APP.route('/channel/removeowner', methods=['POST'])
def removeowner_channel():
    channel_id = int(request.form.get('channel_id'))
    channel_removeowner(request.form.get('token'),
                        channel_id, int(request.form.get('u_id')))
    return sendSuccess({
    })


@APP.route('/channels/list', methods=['GET'])
def list_channels():
    user_channel_list = channels_list(request.args.get('token'))
    return sendSuccess(
        user_channel_list
    )


@APP.route('/channels/listall', methods=['GET'])
def listall_channels():
    all_channels = channels_listall(request.args.get('token'))
    return sendSuccess(
        all_channels
    )


@APP.route('/channels/create', methods=['POST'])
def create_channels():
    is_public = stringToBoolean(request.form.get('is_public'))
    channel_id = channels_create(request.form.get('token'), request.form.get('name'), is_public)['channel_id']
    return sendSuccess({
        'channel_id' : channel_id
    })

'''User functions'''
@APP.route('/user/profile', methods=['GET'])
def user_profile_fn(): 
    user_dict = user_profile(request.args.get('token'), int(request.args.get('u_id')))
    return dumps(user_dict)

@APP.route('/user/profile/setname', methods=['PUT'])
def user_profile_setname_fn():
    
    token = request.form.get('token')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    user_profile_setname(token, name_first, name_last)
    return dumps({})

@APP.route('/user/profile/setemail', methods=['PUT'])
def user_profile_seteamil_fn():
    token = request.form.get('token')
    email = request.form.get('email')
    user_profile_setemail(token, email)
    return dumps({})

@APP.route('/user/profile/sethandle', methods=['PUT'])
def user_profile_sethandle_fn():
    user_profile_sethandle(request.form.get('token'), request.form.get('handle_str'))
    return dumps({}) 

@APP.route('/user/profiles/uploadphoto', methods=['POST'])
def user_profiles_uploadphoto_fn():
    token = request.form.get('token')
    img_url = request.form.get('img_url')
    x_start = request.form.get('x_start')
    y_start = request.form.get('y_start')
    x_end = request.form.get('x_end')
    y_end = request.form.get('y_end')

    
    return dumps(
        user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end)
    )

@APP.route('/users/all', methods=['GET'])
def users_all_fn():
    return dumps(users_all(request.args.get('token')))


@APP.route('/standup/start', methods=['POST'])
def standup_start_fn():
    return dumps(
       standup_start(request.form.get('token'), int(request.form.get('channel_id')), int(request.form.get('length')))
       ) 


@APP.route('/standup/active', methods=['GET'])
def standup_active_fn():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return dumps(
       standup_active(token, channel_id) 
    ) 

@APP.route('/standup/send', methods=['POST'])
def standup_send_fn():
    return dumps(
       standup_send(request.form.get('token'), int(request.form.get('channel_id')), request.form.get('message'))
       ) 


@APP.route('/search', methods=['GET'])
def search_fn():
    msg_dict = search(request.args.get('token'), request.args.get('query_str'))
    return sendSuccess({'messages' : msg_dict})

@APP.route('/admin/userpermission/change', methods=['POST'])
def admin_userpermission_change_fn():
    admin_userpermission_change(request.form.get('token'), int(request.form.get('u_id')), int(request.form.get('permission_id')))
    return sendSuccess({})

if __name__ == '__main__':
    #print("the port is :", sys.argv[1])
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000), debug=True)
    # APP.run(port=5009, debug=True)
