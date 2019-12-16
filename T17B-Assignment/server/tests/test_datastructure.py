import os
import pytest
import sys
import inspect
from json import dumps
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from data_structure import *
from test_others import setup_test_search
from Error import AccessError, ValueError_http
from functions_auth import auth_passwordreset_request

def test_generateUid_alright():
    # test if the function works properly so it generate 5 digit 
    # integer range between 10000 and 99999
    randomNum = generateUid()
    assert randomNum >= 10000
    assert randomNum <= 99999

def test_getUserByEmail_alright():
    # test if the function works properly so
    # it successfully get a user
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder')
    foundUser = getUserByEmail(user_1['email'])
    assert foundUser == user_1

def test_getUserByEmail_VE():
    # test for ValueError in case unregistered email is input
    data = reset_data()
    data = setup_test_search()
    with pytest.raises(ValueError_http):
        getUserByEmail("someemail@gmail.com")

def test_userExists_true():
    # test if the function works properly
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder')
    boolean = userExists(user_1['email'])
    assert boolean == True


def test_userExists_false():
    # test if the function works properly
    data = reset_data()
    data = setup_test_search()
    boolean = userExists("someemail@gmail.com")
    assert boolean == False


def test_getUidFromToken_alright():
    # test if the function take in a valid token and return a valid u_id 
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder')
    u_id = getUidFromToken(user_1['token'])
    assert u_id == user_1['u_id']

def test_sendSuccess():
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder')
    test = sendSuccess(user_1)
    assert test == dumps(user_1)

def test_sendError():
    data = reset_data()
    data = setup_test_search()
    test = sendError("hollaaaaa")
    assert test == dumps({
        "_error" : "hollaaaaa",
    })

def test_getUidFromToken_VE():
    # test if it raises valueError when function takes in invalid token
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder')
    with pytest.raises(ValueError_http):
        getUidFromToken("someToken")

def test_stringToBoolean_true():
    # test if the function returna boolean value True
    boolean = stringToBoolean("true")
    assert boolean == True
    
def test_stringToBoolean_TRUE():
    # test if the function returna boolean value True
    # test if the function is non case sensitive
    boolean = stringToBoolean("TRUE")
    assert boolean == True

def test_stringToBoolean_false():
    # test if the function returna boolean value True
    boolean = stringToBoolean("false")
    assert boolean == False
    
def test_stringToBoolean_FALSE():
    # test if the function returna boolean value True
    # test if the function is non case sensitive
    boolean = stringToBoolean("FALSE")
    assert boolean == False

def test_getDetailsFromUid():
    # test if the function takes in a valid u_id
    # and returns valid information 
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder')
    info = getDetailsFromUid(user_1['u_id'])
    assert info == {
        'u_id' : user_1['u_id'],
        'name_first' : user_1['name_first'],
        'name_last' : user_1['name_last'],
        'profile_img_url' : user_1['profile_img_url']
    }
 
def test_userIsInChannel_true():
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder') 
    channel_1 = getChannelByChannelName('drinkWater')
    boolean = user_is_in_channel(user_1['u_id'], channel_1['channel_id'])
    assert boolean == True

def test_userIsInChannel_false():
    data = reset_data()
    data = setup_test_search()
    user_3 = getUserByHandle('Ethan') 
    channel_1 = getChannelByChannelName('drinkWater')
    boolean = user_is_in_channel(user_3['u_id'], channel_1['channel_id'])
    assert boolean == False

def test_messageExists_true():
    data = reset_data()
    data = setup_test_search()
    channel_1 = getChannelByChannelName('drinkWater')
    boolean = messageExists(channel_1['messages'][0]['message_id'])
    assert boolean == True


def test_messageExists_false():
    data = reset_data()
    data = setup_test_search()
    boolean = messageExists(10)
    assert boolean == False
    
def test_MessageInfo_alright():
    data = reset_data()
    data = setup_test_search()
    channel_1 = getChannelByChannelName('drinkWater')
    test = getMessageInfo(channel_1['messages'][0]['message_id'])
    assert test == channel_1['messages'][0]


def test_MessageInfo_VE():
    data = reset_data()
    data = setup_test_search()
    channel_1 = getChannelByChannelName('drinkWater')
    with pytest.raises(ValueError_http):
        test = getMessageInfo(1234556)

def test_getUserFromUid_alright():
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder')
    test = getUserFromUid(user_1['u_id'])
    assert test == user_1

def test_getChannelDetails_alright():
    data = reset_data()
    data = setup_test_search()
    channel_1 = getChannelByChannelName('drinkWater')
    test = getChannelDetails(channel_1['channel_id'])
    assert test == channel_1

def test_getChannelDetails_VE():
    data = reset_data()
    data = setup_test_search()
    with pytest.raises(ValueError_http):
        test = getChannelDetails(123365496)


def test_getChannelDetailsSimple_alright():
    data = reset_data()
    data = setup_test_search()
    channel_1 = getChannelByChannelName('drinkWater')
    test = getChannelDetailsSimple(channel_1['channel_id'])
    assert test == {
                'channel_id' : channel_1['channel_id'],
                'name' : channel_1['name']
            }

def test_getChannelDetailsSimple_none():
    data = reset_data()
    data = setup_test_search()
    channel_1 = getChannelByChannelName('drinkWater')
    test = getChannelDetailsSimple(1234556)
    assert test == None


def test_getChnnaelFromMsgId_alright():
    data = reset_data()
    data = setup_test_search()
    channel_1 = getChannelByChannelName('drinkWater')
    test = getChannelFromMsgId(channel_1['messages'][0]['message_id'])
    assert test == channel_1


def test_getChnnaelFromMsgId_VE():
    data = reset_data()
    data = setup_test_search()
    with pytest.raises(ValueError_http):
        getChannelFromMsgId(123456)


def test_getChannelDetails():
    data = reset_data()
    data = setup_test_search()
    channel_1 = getChannelByChannelName('drinkWater')
    test = getChannelDetails(channel_1['channel_id'])
    assert test == channel_1


def test_findMessage_alright():
    data = reset_data()
    data = setup_test_search()
    channel_1 = getChannelByChannelName('drinkWater')
    test = findMessage(channel_1['messages'][0]['message_id'])
    assert test == channel_1

def test_findMessage_none():
    data = reset_data()
    data = setup_test_search()
    channel_1 = getChannelByChannelName('drinkWater')
    test = findMessage(123456)
    assert test == None


def test_getUserFromUid_none():
    data = reset_data()
    data = setup_test_search()
    test = getUserFromUid('someUid')
    assert test == None


def test_checkUserPermission_alright():
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder') 
    test = checkUserPermission(user_1['u_id'])
    assert test == 1


def test_checkUserPermission_VE():
    data = reset_data()
    data = setup_test_search()
    with pytest.raises(ValueError_http):
        test = checkUserPermission(12345)
    

def test_getChannelByChannelName_VE():
    data = reset_data()
    data = setup_test_search()
    with pytest.raises(ValueError_http):
        test = getChannelByChannelName('someChannel')



def test_getDictFromResetCode_VE():
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder') 
    reset_code = auth_passwordreset_request(user_1['email'])
    with pytest.raises(ValueError_http):
        getDictFromResetCode("someResetCode")






    

    




