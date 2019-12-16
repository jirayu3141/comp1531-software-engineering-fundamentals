import pytest
import re
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from Error import AccessError, ValueError_http
from functions_user import *
from functions_auth import auth_register
from functions_others import *
from data_structure import *
from functions_channel import channels_create, channel_invite
from functions_message import message_send


def setup_test_search():
    '''set up for test_search'''
    #SET UP START
    user1 = auth_register("bob@gmail.com", "GoodPassword1", "Builder", "Bob")
    user2 = auth_register("sally@gmail.com", "GoodPassword2", "Super", "Sally")
    user3 = auth_register("ethan@gmail.com", "GoodPassword3", "Ethan", "Earth")
    user_1 = getUserFromToken(user1['token'])
    user_2 = getUserById(user2['u_id'])
    user_3 = getUserById(user3['u_id'])
    # user 1 promote user 2 to be  an admin
    admin_userpermission_change(user_1['token'], user_2['u_id'], 2)
    # then user 1 create channel name drinkWater
    channels_create(user_1['token'], 'drinkWater', True)
    channel_1 = getChannelByChannelName('drinkWater') 
    # user 2 create channel name eatProtein
    channels_create(user_2['token'], 'eatProtein', False)
    channel_2 = getChannelByChannelName('eatProtein')
    # user 1 invite user 2 into drinkWater
    channel_invite(user_1['token'], channel_1['channel_id'], user2['u_id'])
    # user 2 invite user 1 into eatProtein
    channel_invite(user_2['token'], channel_2['channel_id'], user1['u_id'])
    # user 1 sends msg in drinkWate
    message_send(user_1['token'], channel_1['channel_id'], 'I\'m getting bored')
    message_send(user_1['token'], channel_1['channel_id'], 'ethan getting bored')
    # user 2 sends msg in eatProtein
    message_send(user_2['token'], channel_2['channel_id'], 'mer is boring')
    message_send(user_1['token'], channel_2['channel_id'], 'hollaaaaa')
    #SET UP END
    return data

 
# @pytest.fixture
# def setup():
#     # authRegisterDict = auth_register("sally@gmail.com", "GoodPassword1", "Super","Sally")
#     # sally_token = authRegisterDict['token']
#     # sally_uid = authRegisterDict['u_id']
#     # sally_name_first = authRegisterDict['name_first']
#     # sally_name_last = authRegisterDict['name_last']


#     # authRegisterDict2 = auth_register("bob@gmail.com", "GoodPassword2", "Super", "Bob")
#     # bob_token = authRegisterDict2['token'] 
#     # bob_uid = authRegisterDict2['u_id']
#     # bob_name_first = authRegisterDict['name_first']
#     # bob_name_last = authRegisterDict['name_last']

#     class Data:
#         def __init__(self):
#             self.sally_token = 'stoken'
#             self.sally_uid = 9998
#             self.bob_token = 'btoken'
#             self.bob_uid = 9999

#     return Data()


# def test_standup_start(setup):
#     #SET UP START
#     channel_id = channels_create(setup.sally_token, "test room", true)
#     #SET UP END
#     ''' funciton runs fine if the user has permission '''
#     time_finish = standup_start(setup.sally_token, channel_id)

#     ''' function fails if channel_id does not exist '''
#     with pytest.raises(ValueError_http):
#         standup_start(setup.sally_token, 12343454323)
    
#     ''' function fails if user is not in the channel '''
#     with pytest.raises(AccessError):
#         standup_start(setup.bob_token, channel_id)


#     ''' check that correct time returned '''
#     assert time_finish > 0



# def test_standup_send():
#     ''' function runs fine when all citerias are correct'''
#     #SET UP START
#     channel_id = channels_create(setup.sally_token, "test room", true)
#     end_time = standup_start(sally_token, channel_id)
#     #SET UP END
    
#     ''' function fails if channel_id does not exist '''
#     with pytest.raises(ValueError_http):
#         standup_send(setup.sally_token, 12343454323, "testmessage")
    
#     ''' value error if more than 1000 characters is sent '''
#     with pytest.raises(ValueError_http):
#         standup_send(setup.sally_token, channel_id, "a" * 1001)

#     ''' access error when authorised user is not a member of the channel '''
#     with pytest.raises(AccessError):
#         standup_send(setup.bob_token, channel_id, "test")

#     ''' access error if the standup time has been stopped '''
#     #will write test for this after fucntion has been implimented
    

def test_search_alright():
    data = reset_data()
    data = setup_test_search()
    # test if the function runs properly
    # { message_id, u_id, message, time_created, reacts, is_pinned,  }
    user_1 = getUserByHandle('Builder')
    search_return = search(user_1['token'], 'ethan')
    assert search_return[0]['message'] == 'ethan getting bored'

   
def test_search_invalidUser():
    data = reset_data()
    data = setup_test_search()
    # test invalid user
    with pytest.raises(ValueError_http):
        search('sfdgthfgcv', 'bor')


def test_search_emptyQueryString():
    data = reset_data()
    data = setup_test_search()
    # test query_str = '' (empty string)
    user_1 = getUserByHandle('Builder')
    assert search(user_1['token'], '') == []

   
def test_admin_userpermission_change_alright_01():
    # alright when admin change user to admin
    data = reset_data()
    data = setup_test_search()
    user_3 = getUserByHandle('Ethan')
    user_2 = getUserByHandle('Super')
    admin_userpermission_change(user_2['token'], user_3['u_id'], 2)
    assert user_3['permission_id'] == 2 


def test_admin_userpermission_change_alright_02():
    # alright when admin change admin to user
    data = reset_data()
    data = setup_test_search()
    user_2 = getUserByHandle('Super')
    admin_userpermission_change(user_2['token'], user_2['u_id'], 3)
    assert user_2['permission_id'] == 3 

def test_admin_userpermission_change_alright_03():
    # alright when owner change member to owner
    data = reset_data()
    data = setup_test_search()
    user_3 = getUserByHandle('Ethan')
    user_1 = getUserByHandle('Builder')
    admin_userpermission_change(user_1['token'], user_3['u_id'], 1)
    assert user_3['permission_id'] == 1

def test_admin_userpermission_change_alright_04():
    # alright when owner change admin to member
    data = reset_data()
    data = setup_test_search()
    user_2 = getUserByHandle('Super')
    user_1 = getUserByHandle('Builder')
    admin_userpermission_change(user_1['token'], user_2['u_id'], 3)
    assert user_2['permission_id'] == 3


def test_admin_userpermission_change_alright_05():
    # alright when owner change owner to member
    data = reset_data()
    data = setup_test_search()
    user_2 = getUserByHandle('Super')
    user_1 = getUserByHandle('Builder')
    admin_userpermission_change(user_1['token'], user_2['u_id'], 1)
    admin_userpermission_change(user_1['token'], user_2['u_id'], 3)
    assert user_2['permission_id'] == 3

def test_admin_userpermission_change_alright_06():
    # alright when owner change owner to admin
    data = reset_data()
    data = setup_test_search()
    user_2 = getUserByHandle('Super')
    user_1 = getUserByHandle('Builder')
    admin_userpermission_change(user_1['token'], user_2['u_id'], 1)
    admin_userpermission_change(user_1['token'], user_2['u_id'], 2)
    assert user_2['permission_id'] == 2

def test_admin_userpermission_change_VE_00():  
    # value error when owner change owner to owner   
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder')
    user_2 = getUserByHandle('Super')
    admin_userpermission_change(user_1['token'], user_2['u_id'], 1)
    with pytest.raises(ValueError_http, match = '.*'):
        admin_userpermission_change(user_1['token'], user_2['u_id'], 1)

    
def test_admin_userpermission_change_VE_01():  
    data = reset_data()
    data = setup_test_search()
    # value error when permission_id does not refer to a value permission
    user_1 = getUserByHandle('Builder')
    user_2 = getUserByHandle('Super')
    with pytest.raises(ValueError_http, match = '.*'):
        admin_userpermission_change(user_1['token'], user_2['u_id'], None)


def test_admin_userpermission_change_VE_02():
    data = reset_data()
    data = setup_test_search()
    # value error when token does not refer to a valid user
    user_1 = getUserByHandle('Builder')
    with pytest.raises(ValueError_http, match = '.*'):
        admin_userpermission_change('InvalidToken', user_1['u_id'], 1)
 

def test_admin_userpermission_change_VE_03():
    data = reset_data()
    data = setup_test_search()
    # value error when u_id does not refer to a valid user
    user_1 = getUserByHandle('Builder')
    with pytest.raises(ValueError_http, match = '.*'):
        admin_userpermission_change('InvalidUid', user_1['u_id'], 1)


def test_admin_userpermission_change_VE_04():
    data = reset_data()
    data = setup_test_search()   
    # value error when admin change member to member
    user_3 = getUserByHandle('Ethan')
    user_2 = getUserByHandle('Super')
    with pytest.raises(ValueError_http, match = '.*'):
        admin_userpermission_change(user_2['token'], user_3['u_id'], 3)


def test_admin_userpermission_change_VE_05():  
    data = reset_data()
    data = setup_test_search()  
    # value error when admin change member to owner
    user_3 = getUserByHandle('Ethan')
    user_2 = getUserByHandle('Super')
    with pytest.raises(ValueError_http):
        admin_userpermission_change(user_2['token'], user_3['u_id'], 1)

def test_admin_userpermission_change_VE_06():
    data = reset_data()
    data = setup_test_search()
    # value error when admin change admin to admin
    user_2 = getUserByHandle('Super')
    with pytest.raises(ValueError_http):
        admin_userpermission_change(user_2['token'], user_2['u_id'], 2)


def test_admin_userpermission_change_VE_07():
    data = reset_data()
    data = setup_test_search()
    # value error when admin change admin to owner
    user_2 = getUserByHandle('Super')
    with pytest.raises(ValueError_http):
        admin_userpermission_change(user_2['token'], user_2['u_id'], 1)


def test_admin_userpermission_change_VE_08():
    data = reset_data()
    data = setup_test_search()
    # value error when admin change owner to member
    user_1 = getUserByHandle('Builder')
    user_2 = getUserByHandle('Super')
    with pytest.raises(ValueError_http):
        admin_userpermission_change(user_2['token'], user_1['u_id'], 3) 

def test_admin_userpermission_change_VE_09():
    data = reset_data()
    data = setup_test_search()
    # value error when admin change owner to admin
    user_1 = getUserByHandle('Builder')
    user_2 = getUserByHandle('Super')
    with pytest.raises(ValueError_http):
        admin_userpermission_change(user_2['token'], user_1['u_id'], 2)

def test_admin_userpermission_change_VE_10():
    data = reset_data()
    data = setup_test_search()
    # value error when admin change owner to owner
    user_1 = getUserByHandle('Builder')
    user_2 = getUserByHandle('Super')
    with pytest.raises(ValueError_http):
        admin_userpermission_change(user_2['token'], user_1['u_id'], 1)


def test_admin_userpermission_change_VE_11():
    data = reset_data()
    data = setup_test_search()
    # value error when owner change member to member
    user_1 = getUserByHandle('Builder')
    user_3 = getUserByHandle('Ethan')
    with pytest.raises(ValueError_http):
        admin_userpermission_change(user_1['token'], user_3['u_id'], 3)


def test_admin_userpermission_change_VE_12():
    data = reset_data()
    data = setup_test_search()
    # value error when admin change admin to admin
    user_1 = getUserByHandle('Builder')
    user_2 = getUserByHandle('Super')
    with pytest.raises(ValueError_http):
        admin_userpermission_change(user_1['token'], user_2['u_id'], 2)



def test_admin_userpermission_change_VE_lastOwner():
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder')
    # value error when the last owner wants to demote him/herself
    with pytest.raises(ValueError_http):
        admin_userpermission_change(user_1['token'], user_1['u_id'], 2)

def test_admin_userpermission_change_notLastOwner():
    # alright when owner change admin to member
    data = reset_data()
    data = setup_test_search()
    user_2 = getUserByHandle('Super')
    user_1 = getUserByHandle('Builder')
    admin_userpermission_change(user_1['token'], user_2['u_id'], 1)
    admin_userpermission_change(user_1['token'], user_1['u_id'], 3)
    assert user_1['permission_id'] == 3


def test_admin_userpermission_change_AE():
    data = reset_data()
    data = setup_test_search()
    user_3 = getUserByHandle('Ethan')
    user_1 = getUserByHandle('Builder')
    ''' access error when the authorised user is not an admin or owner '''
    with pytest.raises(AccessError):
        admin_userpermission_change(user_3['token'], user_1['u_id'], 1)
