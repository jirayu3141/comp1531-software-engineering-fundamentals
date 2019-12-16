import datetime
from functions_auth import auth_register
from functions_channel import channels_create, channel_messages
from data_structure import getData, tokenize, getUserFromToken, user_is_in_channel, getUidFromToken, getChannelFromChannelId, getChannelDetails
from functions_message import message_send, message_id
from Error import AccessError, ValueError_http

def standup_start (token, channel_id, length):
    channel = getChannelFromChannelId(channel_id)
    #check for started standup
    if channel['standup_active'] is True:
        raise ValueError_http('Standup has already started')
    
    #change standup status to active
    channel['standup_active'] = True
    channel['standup_started_by'] = getUidFromToken(token)
    #store the time finish
    finish_time = datetime.datetime.now(datetime.timezone.utc).astimezone().timestamp() + length

    channel['standup_finish'] = finish_time
    return {'time_finish' : finish_time}

def standup_active(token, channel_id):
    channel = getChannelFromChannelId(channel_id)
    #check if standup_finish time is in the future
    if channel['standup_finish'] > datetime.datetime.now(datetime.timezone.utc).astimezone().timestamp():
        is_active = True
    else:
        is_active = False
        channel['standup_active'] = is_active
        send_compiled_standup_msg(getUidFromToken(token), channel_id)

    return {
        'is_active' : is_active, #channel['standup_active'],
        'time_finish' : channel['standup_finish']
    }

def standup_send(token, channel_id, message):
    channel = getChannelFromChannelId(channel_id)
    if channel['standup_active'] is False:
        raise ValueError_http('Standup not currently active')

    #send message normally
    message_send(token, channel_id, message)

    #add message to a list
    msg_with_names = getUserFromToken(token)['handle_str'] + ": " + message + "\n"
    getChannelFromChannelId(channel_id)['standup_msg'] += msg_with_names

def send_compiled_standup_msg(u_id, channel_id):
    global message_id
    channel = getChannelDetails(channel_id)
    #check if it already has been sent
    if channel['standup_msg'] is not "":
        message_id += 1
        channel['messages'].insert(0, {
            'message_id': message_id,
            'u_id': u_id,
            'message': channel['standup_msg'][:-1],
            'time_created': str(datetime.datetime.now(datetime.timezone.utc).astimezone().timestamp()),     #convert to sydney timezone
            'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted' : False}],
            'is_pinned': False
        })
        #remove standup msg
        channel['standup_msg'] = ""
