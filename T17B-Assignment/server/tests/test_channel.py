import pytest
import os 
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from functions_channel import channel_id, channel_addowner, channel_details, channel_invite, channel_join, channel_leave, channel_messages, channel_removeowner, channels_create, channels_list, channels_listall
from functions_auth import auth_register
from functions_message import message_send
from data_structure import data, getData, tokenize
from Error import AccessError, ValueError_http
import smtplib

def reset_channels():
	data = getData()
	global channel_id
	data['channel'] = []
	for user in data['users']:
		user['joined_channels'] = []
	channel_id = 0

@pytest.fixture(scope='session')
def setup1():
	data = getData()
	global channel_id
	channel_id = 0
	''' Registers user1 '''
	authRegDict1 = auth_register("sojin@gmail.com", "password123", "Sojin", "Nam")
	return authRegDict1

@pytest.fixture(scope='session')
def setup2():
	data = getData()
	''' Registers user2 '''
	authRegDict2 = auth_register("fairuz@gmail.com", "diffpass234", "Fairuz", "Alam")
	return authRegDict2
	
@pytest.fixture(scope='session')
def setup3():
	data = getData()
	''' Registers user3 '''
	authRegDict3 = auth_register("peter@gmail.com", "ilovepie22", "Peter", "Smith")
	return authRegDict3

def test_channel_invite_no_channel(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' Error when channel does not exist'''
	with pytest.raises(ValueError_http, match=r".*"):
		channel_invite(setup1['token'], -1, setup2['u_id'])

def test_channel_invite_no_user(setup1, setup2, setup3):
	data = getData()
	reset_channels()

	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' Error when user does not exist'''
	with pytest.raises(ValueError_http, match=r".*"):
		channel_invite(setup1['token'], channelId1, 'wrong')

def test_channel_invite_unauthorized(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' Error when authorized user is not a member of channel'''
	with pytest.raises(AccessError, match=r".*"):
		channel_invite(setup2['token'], channelId1, setup3['u_id'])

def test_channel_invite_already_member(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	channel_invite(setup1['token'], channelId1, setup2['u_id'])

	''' Error user trying to invite is already a member of channel'''
	with pytest.raises(ValueError_http, match=r".*"):
		channel_invite(setup1['token'], channelId1, setup2['u_id'])

def test_channel_invite_success(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	channel_invite(setup1['token'], channelId1, setup2['u_id'])

	assert channels_list(setup2['token']) == {'channels' : [{
		'channel_id' : channelId1,
		'name' : 'Public Channel',
	}]}

def test_channel_details_no_channel(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' Error when channel does not exist'''
	with pytest.raises(ValueError_http, match=r".*"):
		channel_details(setup1['token'], -1)

def test_channel_details_unauthorized(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' Error when authorized user is not a member of channel'''
	with pytest.raises(AccessError, match=r".*"):
		channel_details(setup2['token'], channelId1)

def test_channel_details_success(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	assert channel_details(setup1['token'], channelId1) == {
		'name' : "Public Channel",
		'all_members' : [{
			'u_id' : setup1['u_id'],
			'name_first' : 'Sojin',
			'name_last' : 'Nam',
			'profile_img_url' : "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg/440px-An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg"}],
			'owner_members' : [{
			'u_id' : setup1['u_id'],
			'name_first' : 'Sojin',
			'name_last' : 'Nam',
			'profile_img_url' : "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg/440px-An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg"
		}]
	}

def test_channel_messages_no_channel(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	# Creates public channel (Admin: user1)
	channelsCreateDict1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreateDict1['channel_id']

	# channel doesnt exist
	with pytest.raises(ValueError_http):
		channel_messages(setup1['token'], -1, 10)

def test_channel_messages_no_message(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	# Creates public channel (Admin: user1)
	channelsCreateDict1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreateDict1['channel_id']

	assert channel_messages(setup1['token'], channelId1, 0) == {
		'messages' : [],
		'start' : 0,
		'end' : 0
	}

def test_channel_messages_start_greater(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	# Creates public channel (Admin: user1)
	channelsCreateDict1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreateDict1['channel_id']

	message_send(setup1['token'], channelId1, 'sendmessage')

	# start is greater than total messages
	with pytest.raises(ValueError_http):
		channel_messages(setup1['token'], channelId1, 40)

def test_channel_messages_start_equal(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	# Creates public channel (Admin: user1)
	channelsCreateDict1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreateDict1['channel_id']

	message_send(setup1['token'], channelId1, 'sendmessage')

	# start is equal to total messages
	with pytest.raises(ValueError_http):
		channel_messages(setup1['token'], channelId1, 1)

def test_channel_messages_unauthorized(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	# Creates public channel (Admin: user1)
	channelsCreateDict1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreateDict1['channel_id']

	# not a member of channel
	with pytest.raises(AccessError):
		channel_messages(setup2['token'], channelId1, 1)

def test_channel_messages_success_exactly_fifty(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	# Creates public channel (Admin: user1)
	channelsCreateDict1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreateDict1['channel_id']

	i = 0
	message_send(setup1['token'], channelId1, 'oldest')
	while i < 48:
		message_send(setup1['token'], channelId1, 'hello')
		i += 1
	message_send(setup1['token'], channelId1, 'recent')

	assert len(channel_messages(setup1['token'], channelId1, 0)['messages']) == 50
	assert channel_messages(setup1['token'], channelId1, 0)['messages'][0]['message'] == 'recent'
	assert channel_messages(setup1['token'], channelId1, 0)['messages'][32]['message'] == 'hello'
	assert channel_messages(setup1['token'], channelId1, 0)['messages'][49]['message'] == 'oldest'

def test_channel_messages_success_more_than_fifty(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	# Creates public channel (Admin: user1)
	channelsCreateDict1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreateDict1['channel_id']

	i = 0
	message_send(setup1['token'], channelId1, 'oldest')
	while i < 55:
		message_send(setup1['token'], channelId1, 'hello')
		i += 1
	message_send(setup1['token'], channelId1, 'recent')

	assert len(channel_messages(setup1['token'], channelId1, 0)['messages']) == 50
	assert channel_messages(setup1['token'], channelId1, 0)['messages'][0]['message'] == 'recent'
	assert channel_messages(setup1['token'], channelId1, 0)['messages'][49]['message'] == 'hello'

def test_channel_messages_success_less_than_fifty(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	# Creates public channel (Admin: user1)
	channelsCreateDict1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreateDict1['channel_id']

	i = 0
	message_send(setup1['token'], channelId1, 'oldest')
	while i < 30:
		message_send(setup1['token'], channelId1, 'hello')
		i += 1
	message_send(setup1['token'], channelId1, 'recent')

	assert len(channel_messages(setup1['token'], channelId1, 1)['messages']) == 31
	assert channel_messages(setup1['token'], channelId1, 1)['messages'][0]['message'] == 'hello'
	assert channel_messages(setup1['token'], channelId1, 1)['messages'][30]['message'] == 'oldest'


def test_channel_leave_success_public(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	# Creates public channel (Admin: user1)
	channelsCreateDict1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreateDict1['channel_id']

	''' Leave public channel '''
	channel_leave(setup1['token'], channelId1)

	''' If above line was successful, channel_list should return an empty list '''
	assert channels_list(setup1['token']) == {'channels' : []}

def test_channel_leave_success_private(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a private channel (Admin: user1) '''
	channelsCreate2 = channels_create(setup1['token'], "Private Channel", False)
	channelId2 = channelsCreate2['channel_id']

	''' Leave private channel'''
	channel_leave(setup1['token'], channelId2)

	''' If above line was succesful, channel_list should return an empty list '''
	assert channels_list(setup1['token']) == {'channels' : []}

def test_channel_leave_no_channel(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' Error when channel does not exist'''
	with pytest.raises(ValueError_http, match=r".*"):
		channel_leave(setup1['token'], -1)

def test_channel_leave_not_member(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' Error when authorized user is not a member'''
	with pytest.raises(AccessError, match=r".*"):
		channel_leave(setup2['token'], channelId1)

def test_channel_join_no_channel(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' Error when Channel ID does not exist '''
	with pytest.raises(ValueError_http, match=r".*"):
		channel_join(setup1['token'], -1)

def test_channel_join_unauthorized(setup1, setup2, setup3):
	global data
	reset_channels()
	''' Creates a private channel (Admin: user1) '''
	channelsCreate2 = channels_create(setup1['token'], "Private Channel", False)
	channelId2 = channelsCreate2['channel_id']

	''' Error when unauthorized user joins private channel '''
	with pytest.raises(AccessError, match=r".*"):
		channel_join(setup2['token'], channelId2)

def test_channel_join_success(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']
	
	''' Join public channel '''
	channel_join(setup2['token'], channelId1)

	assert channels_list(setup1['token']) == {'channels' : [{
		'channel_id' : channelId1,
		'name' : "Public Channel",
	}]}

def test_channel_join_success_admin(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']
	
	''' Join public channel '''
	channel_join(tokenize('bob@gmail.com'), channelId1)

	assert channels_list(setup1['token']) == {'channels' : [{
		'channel_id' : channelId1,
		'name' : "Public Channel",
	}]}

def test_channel_addowner_no_channel(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' Error when channel does not exist '''
	with pytest.raises(ValueError_http, match=r".*"):
		channel_addowner(setup1['token'], -1, setup2['u_id'])

def test_channel_addowner_unauthorized_user(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' Error when not-an-owner tries to add another user as an owner'''
	with pytest.raises(AccessError, match=r".*"):
		channel_addowner(setup2['token'], channelId1, setup1['u_id'])

def test_channel_addowner_success(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' User2 joins the channel '''
	channel_join(setup2['token'], channelId1)

	''' Adds user2 as owner of "Public Channel" '''
	channel_addowner(setup1['token'], channelId1, setup2['u_id'])

	''' If above line was succesful, will display user2 as an owner when calling channel_details '''
	details = channel_details(setup1['token'], channelId1)
	assert details['owner_members'] == [{
		'u_id' : setup1['u_id'],
		'name_first' : "Sojin",
		'name_last' : "Nam",
		'profile_img_url' : "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg/440px-An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg"
		},
										{'u_id' : setup2['u_id'],
										 'name_first' : "Fairuz",
										 'name_last' : "Alam",
										 'profile_img_url' : "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg/440px-An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg"
										}]

def test_channel_addowner_already_owner(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' User2 joins the channel '''
	channel_join(setup2['token'], channelId1)

	''' Adds user2 as owner of "Public Channel" '''
	channel_addowner(setup1['token'], channelId1, setup2['u_id'])

	''' Error when trying to add owner that is already an owner '''
	with pytest.raises(ValueError_http, match=r".*"):
		channel_addowner(setup1['token'], channelId1, setup2['u_id'])

def test_channel_addowner_you_already_owner(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' Error when owner tries to make themselves an owner '''
	with pytest.raises(ValueError_http, match=r".*"):
		channel_addowner(setup1['token'], channelId1, setup1['u_id'])

def test_channel_addowner_not_a_member(setup1, setup2, setup3):
	data = getData()
	reset_channels()

	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' Error when owner tries to make a non-member an owner '''
	with pytest.raises(ValueError_http, match=r".*"):
		channel_addowner(setup1['token'], channelId1, setup2['u_id'])

def test_channel_removeowner_no_channel(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' User2 joins the channel '''
	channel_join(setup2['token'], channelId1)

	''' Adds user2 as owner of "Public Channel" '''
	channel_addowner(setup1['token'], channelId1, setup2['u_id'])

	''' Error when channel does not exist '''
	with pytest.raises(ValueError_http, match=r".*"):
		channel_removeowner(setup1['token'], -1, setup2['u_id'])

def test_channel_removeowner_not_owner(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' User2 joins the channel '''
	channel_join(setup2['token'], channelId1)

	''' User3 joins the channel '''
	channel_join(setup3['token'], channelId1)

	''' Adds user2 as owner of "Public Channel" '''
	channel_addowner(setup1['token'], channelId1, setup2['u_id'])

	''' Error when user is not an owner '''
	with pytest.raises(ValueError_http, match=r".*"):
		channel_removeowner(setup1['token'], channelId1, setup3['u_id'])

def test_channel_removeowner_unauthorized_user(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' Error when not-an-owner tries to remove another user as an owner'''
	with pytest.raises(AccessError, match=r".*"):
		channel_removeowner(setup2['token'], channelId1, setup1['u_id'])

def test_channel_removeowner_success(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' User 2 joins the channel '''
	channel_join(setup2['token'], channelId1)

	''' Adds user2 as an owner '''
	channel_addowner(setup1['token'], channelId1, setup2['u_id'])

	''' User2 removes user1 as owner '''
	channel_removeowner(setup2['token'], channelId1, setup1['u_id'])

	details = channel_details(setup2['token'], channelId1)
	assert details['owner_members'] == [{
		'u_id' : setup2['u_id'],
		'name_first' : "Fairuz",
		'name_last' : "Alam",
		'profile_img_url' : "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg/440px-An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg"
	}]

def test_channel_removeowner_yourself(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' User1 removes attempts to remove themself as an owner '''
	''' (Assumption) It is impossible to remove yourself as an owner (if you are the only owner) '''

	with pytest.raises(ValueError_http, match=r".*"):
		channel_removeowner(setup1['token'], channelId1, setup1['u_id'])

def test_channels_list_empty(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	assert channels_list(setup1['token']) == {'channels' : []}

def test_channels_list_one_channel(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (channel1) (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	assert channels_list(setup1['token']) == {'channels' : [{
		'channel_id' : channelId1,
		'name' : 'Public Channel',
	}]}

	# Passing in token 2 will return empty list
	assert channels_list(setup2['token']) == {'channels' : []}

def test_channels_list_user2_joins(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (channel1) (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	assert channels_list(setup1['token']) == {'channels' : [{
		'channel_id' : channelId1,
		'name' : 'Public Channel',
	}]}

	''' User2 joins channel1 '''
	channel_join(setup2['token'], channelId1)

	assert channels_list(setup2['token']) == {'channels' : [{
		'channel_id' : channelId1,
		'name' : 'Public Channel',
	}]}

def test_channels_list_two_channels(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (channel 1) (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' Creates a private channel (channel 2) (Admin: user1) '''
	channelsCreate2 = channels_create(setup2['token'], "Private Channel", False)
	channelId2 = channelsCreate2['channel_id']

	assert channels_list(setup1['token']) == {'channels' : [{
		'channel_id' : channelId1,
		'name' : 'Public Channel',
	}]}

	assert channels_list(setup2['token']) == {'channels' : [{
		'channel_id' : channelId2,
		'name' : 'Private Channel',
	}]}

def test_channels_listall_empty(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	assert channels_listall(setup1['token']) == {'channels' : []}

def test_channels_listall_1_channel(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (channel1) (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	assert channels_listall(setup1['token']) == {'channels' : [{
		'channel_id' : channelId1,
		'name' : 'Public Channel',
	}]}

	# Passing in token 2 will return same output

	assert channels_listall(setup2['token']) == {'channels' : [{
		'channel_id' : channelId1,
		'name' : 'Public Channel',
	}]}

def test_channels_listall_2_channels(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' Creates a public channel (channel1) (Admin: user1) '''
	channelsCreate1 = channels_create(setup1['token'], "Public Channel", True)
	channelId1 = channelsCreate1['channel_id']

	''' Creates a private channel (channel2) (Admin: user2) '''
	channelsCreate2 = channels_create(setup2['token'], "Private Channel", False)
	channelId2 = channelsCreate2['channel_id']

	assert channels_listall(setup1['token']) == {'channels' : [{
		'channel_id' : channelId1,
		'name' : 'Public Channel',
		},
								{'channel_id' : channelId2,
								'name' : 'Private Channel',
								}]}

	# Passing in token 2 will return same output

	assert channels_listall(setup2['token']) == {'channels' : [{
		'channel_id' : channelId1,
		'name' : 'Public Channel',
		},
								{'channel_id' : channelId2,
								'name' : 'Private Channel',
								}]}

def test_channels_create_success_public(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' valid name '''
	validName1 = "validname"

	''' Creating a public channel '''
	channelsCreate1 = channels_create(setup1['token'], validName1, True)
	channelId1 = channelsCreate1['channel_id']

	''' Confirm that created channel is public by attempting to add unauthorized user '''
	channel_join(setup2['token'], channelId1)

	''' If the above was successful, it will display the channel when calling channels_listall '''
	assert channels_listall(setup1['token']) == {'channels' : [{
		'channel_id' : channelId1,
		'name' : validName1,
	}]}


def test_channels_create_success_private(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' valid name '''
	validName2 = "anothername"

	''' Creating a private channel '''
	channelsCreate2 = channels_create(setup1['token'], validName2, False)
	channelId2 = channelsCreate2['channel_id']

	''' If the above was successful, it will display the channel when calling channels_listall'''
	assert channels_listall(setup1['token']) == {'channels' : [{
		'channel_id' : channelId2,
		'name' : validName2
	}]}

def test_channels_create_invalid_name_public(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' invalid name (> 20 characters) '''
	invalidName = "thisisaninvalidname!!!"

	''' Error when invalid name entered '''
	with pytest.raises(ValueError_http, match=r".*"):
		channels_create(setup1['token'], invalidName, True)

def test_channels_create_invalid_name_private(setup1, setup2, setup3):
	data = getData()
	reset_channels()
	''' invalid name (> 20 characters) '''
	invalidName = "thisisaninvalidname!!!"

	''' Error when invalid name entered '''
	with pytest.raises(ValueError_http, match=r".*"):
		channels_create(setup2['token'], invalidName, False)

