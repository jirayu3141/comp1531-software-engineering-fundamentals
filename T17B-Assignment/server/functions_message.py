from data_structure import *
from Error import AccessError, ValueError_http
from functions_channel import channels_create, channel_join, channel_details, channel_messages
from functions_auth import auth_register
from functions_user import user_profile
from functions_others import *
import datetime

message_id = 0

def message_sendlater(token, channel_id, message, time_sent):
    global message_id
    # check for access error (user must be in the channel)
    if user_is_in_channel(getUidFromToken(token), channel_id) is False:
        raise AccessError('User not in the channel')

    if len(message) > 1000:
        raise ValueError_http("Message cannot be longer than 1000 characters")

    #time sent has to be in the future
    if float(time_sent) < datetime.datetime.now(datetime.timezone.utc).astimezone().timestamp():
        raise ValueError_http("Time set has to be in the future")

    # add message details
    channel = getChannelDetails(channel_id)
    message_id += 1
    channel['messages'].insert(0, {
        'message_id': message_id,
        'u_id': getUidFromToken(token),
        'message': message,
        'time_created': str(time_sent),
        'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted' : False}],
        'is_pinned': False
    })
    return {'message_id': message_id}

def message_send(token, channel_id, message):
    global message_id
    # check for access error (user must be in the channel)
    if user_is_in_channel(getUidFromToken(token), channel_id) == False:
        raise AccessError('User not in the channel')

    if len(message) > 1000:
        raise ValueError_http("Message cannot be longer than 1000 characters")

    #if message contains /satndup add to standup dict

    # add message details
    channel = getChannelDetails(channel_id)
    message_id += 1
    channel['messages'].insert(0, {
        'message_id': message_id,
        'u_id': getUidFromToken(token),
        'message': message,
        'time_created': str(datetime.datetime.now(datetime.timezone.utc).astimezone().timestamp()),     #convert to sydney timezone
        'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted' : False}],
        'is_pinned': False
    })
    return {'message_id': message_id}

def message_remove(token, message_id):
    # message doesnt exist
    if messageExists(message_id) is False:
        raise ValueError_http('Message does not exist')
    channel_id = findMessage(message_id)['channel_id']
    # user must be authorized
    if isAdmin(token, channel_id) is True or message_belong_to_user(token, message_id):
        channel = findMessage(message_id)
        channel['messages'].remove(getMessageInfo(message_id))
    else:
        raise AccessError('User not authorized to remove message')


def message_edit(token, message_id, message):
    # message doesnt exist
    if messageExists(message_id) is False:
        raise ValueError_http('Message does not exist')
    if len(message) > 1000:
        raise ValueError_http('Message cannot be longer than 1000 characters')
    channel_id = findMessage(message_id)['channel_id']
    # user must be authorized
    if isAdmin(token, channel_id) is True or message_belong_to_user(token, message_id):
        getMessageInfo(message_id)['message'] = message
    else:
        raise AccessError('User not authorized to edit message')
    pass


def message_react(token, message_id, react_id):
    message = getMessageInfo(message_id)
    channel_id = findMessage(message_id)['channel_id']
    u_id = getUidFromToken(token)
    #check that user in part of the channel
    if user_is_in_channel(u_id, channel_id) is False:
        raise ValueError_http('User not in the channel')
    #check if message has been reacted
    if u_id in message['reacts'][0]['u_ids']:
        raise ValueError_http('Already reacted')
    
    message['reacts'][0]['u_ids'].append(u_id)
    message['reacts'][0]['is_this_user_reacted'] = True
    #print("###############")
    #print(message)


def message_unreact(token, message_id, react_id):
    message = getMessageInfo(message_id)
    channel_id = findMessage(message_id)['channel_id']
    u_id = getUidFromToken(token)

    if user_is_in_channel(u_id, channel_id) is False:
        raise ValueError_http('User not in channel')
    if u_id not in message['reacts'][0]['u_ids']:
        raise ValueError_http(description='Message already unreacted')
    message['reacts'][0]['u_ids'].remove(u_id)
    message['reacts'][0]['is_this_user_reacted'] = False
    print(message)
        


def message_pin(token, message_id):
    # user has to be admin
    message = getMessageInfo(message_id)
    channel_id = findMessage(message_id)['channel_id']
    channel = getChannelDetails(channel_id)
    u_id = getUidFromToken(token)
    if u_id not in channel['all_members']:
        raise AccessError('User is not a member ofo the channel')
    if isAdmin(token, channel_id) is True and message['is_pinned'] is False:
        message['is_pinned'] = True
    elif isAdmin(token, channel_id) is False:
        raise ValueError_http('User has to be admin to pin')
    elif message['is_pinned'] is True:
        raise ValueError_http('Message is already pinned')


def message_unpin(token, message_id):
    # user has to be admin
    message = getMessageInfo(message_id)
    channel_id = findMessage(message_id)['channel_id']
    channel = getChannelDetails(channel_id)
    u_id = getUidFromToken(token)
    if u_id not in channel['all_members']:
        raise AccessError('User is not a member ofo the channel')
    if isAdmin(token, channel_id) is True and message['is_pinned'] is True:
        message['is_pinned'] = False
    elif isAdmin(token, channel_id) is False:
        raise ValueError_http('User has to be admin to pin')
    elif message['is_pinned'] is False:
        raise ValueError_http('Message is already unpinned')
