from json import dumps
import jwt, pickle, os, threading, datetime, random
from Error import AccessError, ValueError_http

# Global Variable
'''
user schema = 'users': [{'email': 'user1@gmail.com', 
                        'password': '123456',
                        'name_first': 'nameFirst',
                        'name_last': 'nameLast', 
                        'token': 1234',
                        'u_id': 1,
                        'permission_id' : 1,
                        'joined_channels' : [
                            'channel_id': channel_id,
                            'name' : 'channel_name'
                        ]}]

resetCode schema = [{'reset_code' : '12345',
                    'email' : 'name@gmail.com'}]

channel schema = [{
            'channel_id' : 1,
            'name' : name,
            'is_public' : is_public,
            'all_members' : [u_id],
            'owner_members' : [u_id],
            'messages' : [{
                'message_id' : 1,
                'u_id' : 123,
                'message' : 'hi!',
                'time_created' : datetime(now),
                'reacts' : [{react_id: 1,  u_ids: [u_id1, u_id2], is_this_user_reacted=(boolean)}],
                'is_pinned' : True
            }]
            'standup_msg' : "STANDUP"
            'standup_active' : False
            'standup_finish' : None
        }]


'''
#import data
data = {
    'users': [],
    'resetCode' : [],
    'channel' : [],
}

unique_uid = []

SECRET = 'secret'
# ownerName = getUserByEmail("x@x.com")["name"]

def generateUid():
    data = getData()
    randomNum = random.randint(10000,99999)
    for user in data['users']:
        if randomNum == user['u_id']:
            generateUid()
    return randomNum

def getUserByEmail(email):
    global data
    for user in data["users"]:
        if user["email"] == email:
            return user
    raise ValueError_http("Email not found")

def userExists(email):
    global data
    for user in data["users"]:
        if user["email"] == email:
            return True
    return False

# def showUsers():
#     global data
#     for user in data['users']:
#         print(user)


def getData():
    global data
    return data

def sendSuccess(data):
    return dumps(data)


def sendError(message):
    return dumps({
        '_error' : message,
    })

def getUidFromToken(token):
    global data
    for users in data['users']:
        if token == users['token']:
            return users['u_id']
    raise ValueError_http("u_id not found")

def stringToBoolean(is_public):
    if is_public.lower() == "true":
        return True
    elif is_public.lower() == "false":
        return False

def getDetailsFromUid(u_id):
    global data
    for users in data['users']:
        if u_id == users['u_id']:
            return {
                'u_id' : u_id,
                'name_first' : users['name_first'],
                'name_last' : users['name_last'],
                'profile_img_url' : users['profile_img_url']
            }

def getMessages(u_id, messages_list, start, end):
    message_dict_list = []
    if end == -1:
        message_slice = messages_list[start:]
    else:
        message_slice = messages_list[start:end]
    for x in message_slice:
        # check if this user has reacted        
        if u_id in x['reacts'][0]['u_ids']:
            x['reacts'][0]['is_this_user_reacted'] = True
        else:
            x['reacts'][0]['is_this_user_reacted'] = False

        # message has to be in the past
        message_dict = {
            'message_id' : x['message_id'],
            'u_id' : x['u_id'],
            'message' : x['message'],
            'time_created' : x['time_created'],
            'reacts' : x['reacts'],
            'is_pinned' : x['is_pinned']
        }
        if datetime.datetime.now(datetime.timezone.utc).astimezone().timestamp() >= float(x['time_created']):
            message_dict_list.append(message_dict)
    return message_dict_list

def getChannelDetailsSimple(channel_id):
    data = getData()
    for channel in data['channel']:
        if channel['channel_id'] == channel_id:
            channel_dic = {
                'channel_id' : channel_id,
                'name' : channel['name']
            }
            return channel_dic
    return None

def user_is_in_channel(u_id, channel_id):
    channel = getChannelDetails(channel_id)
    if u_id in channel['all_members']:
        return True
    else:
        return False
            

def messageExists(message_id):
    for channels in data['channel']:
        for message in channels['messages']:
            if message['message_id'] == message_id:
                return True
    return False


def getMessageInfo(message_id):
    data = getData()
    for channel in data['channel']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                return message
    raise ValueError_http("Message not found")

def getChannelFromMsgId(message_id):
    data = getData()
    for channels in data['channel']:
        for message in channels['messages']:
            if message_id == message['message_id']:
                return channels
    raise ValueError_http("channel not found")

def getUserFromToken(token):
    data = getData()
    for user in data['users']:
        if token == user['token']:
            return user
    raise ValueError_http("Invalid token")

def getChannelDetails(channel_id):
    data = getData()
    for channel in data['channel']:
        if channel['channel_id'] == channel_id:
            return channel
    raise ValueError_http('Channel not found')

def isAdmin(token, channel_id):
    user_id = getUserFromToken(token)['u_id']
    channel = getChannelDetails(channel_id)
    if user_id in channel['owner_members']:
        return True
    return False
    
def message_belong_to_user(token, message_id):
    info = getMessageInfo(message_id)
    user_email = getUserFromToken(token)['email']
    if info['u_id'] == getUidFromToken(token):
        return True
    return False

def tokenize(email):
    return str(jwt.encode({'email': email}, SECRET, algorithm='HS256'))


def findMessage(message_id):
    data = getData()
    for channels in data['channel']:
        for message in channels['messages']:
            if message['message_id'] == message_id:
                return channels
    return None


def getUserFromUid(u_id):
    data = getData()
    for user in data['users']:
        if user['u_id'] == u_id:
            return user
    return None

def getChannelFromChannelId(channel_id):
    data = getData()
    for channel in data['channel']:
        if channel['channel_id'] == channel_id:
            return channel
    raise ValueError_http("Invalid channel ID")

def isUidValid(u_id):
    data = getData()
    for user in data['users']:
        if user['u_id'] == u_id:
            return 1
    raise ValueError_http("Invalid user_id")


def checkUserPermission(u_id):
    data = getData()
    for user in data['users']:
        if user['u_id'] == u_id:
            return user['permission_id']
    raise ValueError_http("Invalid user_id")

def checkFirstUserPermission():
    data = getData()
        # first user that signs up is an owner
    if data['users'] == []:
        return 1
    else:
        return 3

def reset_resetCode(email):
    for dicts in data['resetCode']:
        if dicts['email'] == email:
            data['resetCode'].remove(dicts)

def getUserById(u_id):
    data = getData()
    for i in data['users']:
        if i['u_id'] == u_id:
            return i
    raise ValueError_http('User not found')
    
    
def getUserByHandle(handle_str):
    global data
    for i in data['users']:
        if i['handle_str'] == handle_str:
            return i 
    return None 

def findResetcodeMatch(reset_code):
    data = getData()
    for dicts in data['resetCode']:
        if dicts['reset_code'] == reset_code:
            return dicts['email']
    raise ValueError_http("Invalid reset_code") 

def getChannelByChannelName(name):
    data = getData()
    for ch in data['channel']:
        if ch['name'] == name:
            return ch
    raise ValueError_http("Channel name not found")

def reset_data():
    global data 
    data = {
    'users': [],
    'resetCode' : [],
    'channel' : [],
    }
    return data

def getDictFromResetCode(reset_code):
    data = getData()
    for dicts in data['resetCode']:
        if dicts['reset_code'] == reset_code:
            return dicts
    raise ValueError_http("Reset_code not found")
