import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import time
from functions_channel import channels_create, channel_join
from functions_standup import *
from data_structure import *
import pytest

def reset_data_standup():
    data = getData()
    data['users'] = []
    user1 = auth_register('user1@gmail.com', 'password', 'Sally', 'name')
    user2 = auth_register('user2@gmail.com', 'password', 'Bob', 'name')	
    user3 = auth_register('user3@gmail.com', 'password', 'Bob2', 'name')	
    global channel_id
    data['channel'] = []
    for user in data['users']:
        user['joined_channels'] = []
    channel_id = 0
    ch_id = channels_create(user1['token'], 'ch1', True)['channel_id']
    channel_join(user2['token'], ch_id)
    return user1, user2,user3, ch_id


def test_standup_start_valid():
    user1, *_, ch = reset_data_standup()
    standup_start(user1['token'], ch, 2)
    assert getChannelDetails(ch)["standup_active"] == True
    assert getChannelDetails(ch)["standup_started_by"] == user1['u_id']

def test_standup_start_invalid_channel():
    user1, *_, ch = reset_data_standup()
    with pytest.raises(ValueError_http):
        standup_start(user1['token'], ch+2 , 2)

def test_standup_start_already_started():
    user1, *_, ch = reset_data_standup()
    standup_start(user1['token'], ch, 2)
    with pytest.raises(ValueError_http):
        standup_start(user1['token'], ch, 2)

def test_standup_send_vaid():
    user1, *_, ch = reset_data_standup()
    standup_start(user1['token'], ch, 2)
    standup_send(user1['token'], ch, 'message')

def test_standup_send_message_too_long():
    user1, *_, ch = reset_data_standup()
    standup_start(user1['token'], ch, 2)
    with pytest.raises(ValueError_http):
        standup_send(user1['token'], ch, 'a'*1001)

def test_standup_send_not_active_standup():
    user1, *_, ch = reset_data_standup()
    with pytest.raises(ValueError_http):
        standup_send(user1['token'], ch, 'a')

def test_standup_send_invalid_channel():
    user1, *_, ch = reset_data_standup()
    standup_start(user1['token'], ch, 2)
    with pytest.raises(ValueError_http):
        standup_send(user1['token'], ch+2, 'a')

def test_standup_active_not_active():
    user1, *_, ch = reset_data_standup()
    assert standup_active(user1['token'], ch)['is_active'] == False

def test_standup_active_active():
    user1, *_, ch = reset_data_standup()
    standup_start(user1['token'], ch, 2)
    assert standup_active(user1['token'], ch)['is_active'] == True

def test_standup_just_ended():
    user1, user2, _, ch = reset_data_standup()
    standup_start(user1['token'], ch, 1)
    standup_send(user1['token'], ch, 'msg1')
    standup_send(user2['token'], ch, 'msg2')
    assert getChannelDetails(ch)["standup_active"] == True
    time.sleep(2)
    standup_active(user1['token'], ch)
    assert getChannelDetails(ch)["standup_active"] == False

