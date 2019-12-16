from datetime import datetime, timedelta
import pytest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from Error import AccessError, ValueError_http
from functions_message import *
from functions_channel import channels_create, channel_join
from functions_auth import auth_register
from data_structure import getData
import smtplib

@pytest.fixture(scope='session')
def reg1(request):
    data = getData()
    message_id = 0
    authRegDic1 = auth_register("user1@gmail.com", "password", "name1", "name2")
    return authRegDic1

@pytest.fixture(scope='session')
def reg2(request):
    data = getData()
    authRegDic2 = auth_register("user2@gmail.com", "password", "name1", "name2")
    return authRegDic2

@pytest.fixture(scope='session')
def reg3(request):
    data = getData()
    return auth_register("user3@gmail.com", "password", "name1", "name2")

@pytest.fixture(scope='session')
def reg4(request):
    data = getData()
    return auth_register("user4@gmail.com", "password", "name1", "name2")

@pytest.fixture(scope='session')
def channel_id1(request,reg1,reg2,reg3,reg4):
    data = getData()
    #user1 create a public channel
    channel_id_1 = channels_create(reg1['token'], 'channel1', True)['channel_id']
    #user2 joins the public channel
    channel_join(reg2['token'], channel_id_1)
    #user4 joins channel 1
    channel_join(reg4['token'], channel_id_1)
    return channel_id_1

@pytest.fixture(scope='session')
def channel_id2(request,reg2):
    data = getData()
    #channel 3 create a private channel
    channel_id_2 = channels_create(reg2['token'], "channel2", False)['channel_id']
    return channel_id_2

# SETUP ENDS

def reset():
    data = getData()
    for channel in data['channel']:
        channel['messages'] = []

def test_message_sendlater_too_long(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    time_sent = datetime.datetime.now(datetime.timezone.utc).astimezone().timestamp()+1
    with pytest.raises(ValueError_http):
        message_sendlater(reg1['token'], channel_id1, "H!"*1000, time_sent)

def test_message_sendlater_unauthorized(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    time_sent = datetime.datetime.now(datetime.timezone.utc).astimezone().timestamp()+1
    with pytest.raises(AccessError):
        message_sendlater(reg3['token'], channel_id1, "Hi!", time_sent)

def test_message_sendlater_past(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    time_sent = datetime.datetime.now(datetime.timezone.utc).astimezone().timestamp()-0.5
    with pytest.raises(ValueError_http):
        message_sendlater(reg1['token'], channel_id1, "Hi!", time_sent)

def test_message_sendlater_success(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    time_sent = datetime.datetime.now(datetime.timezone.utc).astimezone().timestamp()+0.001
    message_id = message_sendlater(reg1['token'], channel_id1, "Hi!", time_sent)

def test_message_send_valid(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    #valid users are able to send messages
    message_send(reg1['token'], channel_id1, "Hello World!!!")
    message_send(reg1['token'], channel_id1, "I love pizza")
    message_send(reg1['token'], channel_id1, "Hello World3! :D")
    message_send(reg2['token'], channel_id1, "Hi World1! :D")
    message_send(reg2['token'], channel_id1, "Bye!!")
    assert channel_messages(reg1['token'], channel_id1, 0)['messages'][0]['message'] == "Bye!!"
    assert channel_messages(reg1['token'], channel_id1, 0)['messages'][3]['message'] == "I love pizza"
    assert channel_messages(reg1['token'], channel_id1, 0)['messages'][4]['message'] == "Hello World!!!"

def test_message_send_invalid_user(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    #checking for invalid/unauthorised user (user3 is not in the group)
    print(data)
    with pytest.raises(AccessError, match=r".*"):
        message_send(reg3['token'], channel_id1, "I am invalid")
    with pytest.raises(AccessError, match=r".*"):
        message_send(reg1['token'], channel_id2, "I am invalid")

def test_message_send_invalid_message_length(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    #ValueError_http when msg length > 1000
    with pytest.raises(ValueError_http):
       message_send(reg2['token'], channel_id1, "A" * 1001)

def test_message_remove_no_message(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    message_send(reg1['token'], channel_id1, "Hello World!!!")
    message_send(reg1['token'], channel_id1, "I love pizza")
    with pytest.raises(ValueError_http):
       message_remove(reg1['token'], -1)

def test_message_remove_unauthorized(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    message_id1 = message_send(reg1['token'], channel_id1, "Hello World!!!")['message_id']
    with pytest.raises(AccessError):
       message_remove(reg2['token'], message_id1)

def test_message_remove_success(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    message_id1 = message_send(reg1['token'], channel_id1, "Hello World!!!")['message_id']
    message_remove(reg1['token'], message_id1)
    assert channel_messages(reg1['token'], channel_id1, 0)['messages'] == []

def test_message_edit_valid_edit(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    message_id = message_send(reg2['token'], channel_id1, "hi")['message_id']
    message_edit(reg2['token'], message_id, 'edited message')
    assert getMessageInfo(message_id)['message'] == 'edited message'
    
def test_message_edit_msg_too_long(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    message_id = message_send(reg2['token'], channel_id1, "hi")['message_id']
    with pytest.raises(ValueError_http, match='Message cannot be longer than 1000 characters'):
        message_edit(reg2['token'], message_id, 'a' * 1001)

def test_message_edit_invalid_id(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    message_id = message_send(reg2['token'], channel_id1, "hi")['message_id']
    '''invalid message_id'''
    with pytest.raises(ValueError_http):
        message_edit(reg1['token'], 2345, "Editing message")


def test_message_edit_not_authorized(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    message_id = message_send(reg2['token'], channel_id1, "hi")['message_id']
    #user3 not in the channel
    with pytest.raises(AccessError, match='User not authorized to edit message'):
        message_edit(reg3['token'], message_id, "Editing message")
    #user4 in cahnnel but did not send message
    with pytest.raises(AccessError, match='User not authorized to edit message'):
        message_edit(reg4['token'], message_id, "Editing message")

def test_message_react_valid(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    message_id = message_send(reg1['token'], channel_id1, "hi")['message_id']
    #user2 react message
    message_react(reg2['token'], message_id, channel_id1)
    assert getMessageInfo(message_id)['reacts'] == [{'react_id': 1, 'u_ids': [reg2['u_id']], 'is_this_user_reacted': True}]
    #user1 react message
    message_react(reg1['token'], message_id, channel_id1)
    assert getMessageInfo(message_id)['reacts'] == [{'react_id': 1, 'u_ids': [reg2['u_id'], reg1['u_id']],'is_this_user_reacted': True}]

def test_message_react_already_reacted(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    message_id = message_send(reg1['token'], channel_id1, "hi")['message_id']
    #user2 react message
    message_react(reg2['token'], message_id, channel_id1)
    with pytest.raises(ValueError_http):
        message_react(reg2['token'], message_id, channel_id1)

def test_message_react_user_not_in_channel(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    message_id = message_send(reg1['token'], channel_id1, "hi")['message_id']
    #user3 who is not in the channel try to react
    with pytest.raises(ValueError_http):
        message_react(reg3['token'], message_id, channel_id1)

def test_message_unreact_valid(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    message_id = message_send(reg1['token'], channel_id1, "hi")['message_id']
    #user2 react message
    message_react(reg1['token'], message_id, channel_id1)
    message_react(reg2['token'], message_id, channel_id1)
    #user1 unreact message
    message_unreact(reg2['token'], message_id, channel_id1)
    assert getMessageInfo(message_id)['reacts'] == [{'react_id': 1, 'u_ids': [reg1['u_id']], 'is_this_user_reacted': False}]
    
def test_message_unreact_already_unreacted(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    message_id = message_send(reg1['token'], channel_id1, "hi")['message_id']
    #user2 react message
    message_react(reg2['token'], message_id, channel_id1)
    message_unreact(reg2['token'], message_id, channel_id1)
    with pytest.raises(ValueError_http):
        message_unreact(reg2['token'], message_id, channel_id1) 

def test_message_unreact_unauthorized(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    message_id = message_send(reg1['token'], channel_id1, "hi")['message_id']
    #user2 react message
    message_react(reg2['token'], message_id, channel_id1)
    message_unreact(reg2['token'], message_id, channel_id1)
    with pytest.raises(ValueError_http):
        message_unreact(reg3['token'], message_id, channel_id1)      

def test_message_pin_valid(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    #user 2 post
    message_id = message_send(reg2['token'], channel_id1, "hi")['message_id']
    #user 1 pin
    message_pin(reg1['token'], message_id)
    assert getMessageInfo(message_id)['is_pinned'] == True

def test_message_pin_not_admin(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    #user 2 post
    message_id = message_send(reg2['token'], channel_id1, "hi")['message_id']
    with pytest.raises(ValueError_http):
        message_pin(reg2['token'], message_id)

def test_message_pin_already_pinned(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    #user 2 post
    message_id = message_send(reg2['token'], channel_id1, "hi")['message_id']
    message_pin(reg1['token'], message_id)
    with pytest.raises(ValueError_http):
        message_pin(reg1['token'], message_id)

def test_message_pin_unauthorized(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    #user 2 post
    message_id = message_send(reg2['token'], channel_id1, "hi")['message_id']
    with pytest.raises(AccessError):
        message_pin(reg3['token'], message_id)

def test_message_unpin_valid(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    #user 2 post
    message_id = message_send(reg2['token'], channel_id1, "hi")['message_id']
    #user 1 pin
    message_pin(reg1['token'], message_id)
    message_unpin(reg1['token'], message_id)
    assert getMessageInfo(message_id)['is_pinned'] == False

def test_message_unpin_unauthorized(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    #user 2 post
    message_id = message_send(reg2['token'], channel_id1, "hi")['message_id']
    #user 1 pin
    message_pin(reg1['token'], message_id)
    with pytest.raises(AccessError):
        message_unpin(reg3['token'], message_id)

def test_message_unpin_not_admin(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    #user 2 post
    message_id = message_send(reg2['token'], channel_id1, "hi")['message_id']
    #user 1 pin
    message_pin(reg1['token'], message_id)
    with pytest.raises(ValueError_http):
        message_unpin(reg2['token'], message_id)

def test_message_unpin_already_unpinned(reg1, reg2, reg3, reg4, channel_id1, channel_id2):
    reset()
    #user 2 post
    message_id = message_send(reg2['token'], channel_id1, "hi")['message_id']
    message_pin(reg1['token'], message_id)
    message_unpin(reg1['token'], message_id)
    with pytest.raises(ValueError_http):
        message_unpin(reg1['token'], message_id)
