import pytest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from functions_auth import *
from data_structure import data, tokenize, reset_data, getUserByHandle, getDictFromResetCode
from Error import AccessError, ValueError_http
from test_others import setup_test_search
import smtplib


@pytest.fixture(scope='session')
def setup1(request):
    data = getData()
    ''' Registers user1 '''
    authRegDict1 = auth_register("earth@gmail.com", "GoodPassword1", "Builder", "Bob")
    return authRegDict1

@pytest.fixture(scope='session')
def reg1(request):
    data = getData()
    authRegDict = auth_register("user_1@gmail.com", "password", "user1", "user1_last")
    # def fin():
    #     #print("teardown smtp_connection")
    #     data = {
    #         'users' : [],
    #         'channels' : [],
    #         'resetCode' : []
    #     }
    return authRegDict

@pytest.fixture(scope='session')
def reg2(request):
    data = getData()
    authRegDict = auth_register("user_2@gmail.com", "password", "user2", "user2_last")
    # def fin():
    #     #print("teardown smtp_connection")
    #     data = {
    #         'users' : [],
    #         'channels' : [],
    #         'resetCode' : []
    #     }
    return authRegDict

@pytest.fixture(scope='session')
def reg3(request):
    data = getData()
    authRegDict = auth_register("user_3@gmail.com", "password", "user3", "user3_last")
    # def fin():
    #     #print("teardown smtp_connection")
    #     data = {
    #         'users' : [],
    #         'channels' : [],
    #         'resetCode' : []
    #     }
    return authRegDict


def test_login_valid(reg1, reg2, reg3):
    #valid logins
    assert auth_login("user_1@gmail.com", "password") == {'u_id' : reg1['u_id'], 'token' : reg1['token']}
    assert auth_login("user_2@gmail.com", "password") == {'u_id' : reg2['u_id'], 'token' : reg2['token']}
    assert auth_login("user_3@gmail.com", "password") == {'u_id' : reg3['u_id'], 'token' : reg3['token']}

def test_login_not_registered(reg1, reg2, reg3):
    #email does not belong to a user
    with pytest.raises(ValueError_http, match=r".*"):
        auth_login('bnm@gmail.com', 'password')
    
def test_login_invalid_email(reg1, reg2, reg3):
    #testing invalid email
    with pytest.raises(ValueError_http, match='Invalid email'):
        auth_login('invalid_email', 'password')
    with pytest.raises(ValueError_http, match='Invalid email'):
        auth_login('invalid_email@gmail', 'password')
    with pytest.raises(ValueError_http, match='Invalid email'):
        auth_login('invalid_email@.com', 'password')
    with pytest.raises(ValueError_http, match='Invalid email'):
        auth_login('@gmail.com', 'password')
    with pytest.raises(ValueError_http, match='Invalid email'):
        auth_login('invalid.com', 'password')
    with pytest.raises(ValueError_http, match='Invalid email'):
        auth_login('invalid @gmail.com', 'password')


def test_login_invalid_password(reg1, reg2, reg3):
    #testing invalid password
    with pytest.raises(ValueError_http, match='Incorrect password'):
        auth_login('user_1@gmail.com', 'wrong_password')


def test_register_invalid_email():
    # invaid email
    with pytest.raises(ValueError_http):
        auth_register("sadf", "abc12345", "Bob", "Lastbob")
    # email with space
    with pytest.raises(ValueError_http):
        auth_register("bab @gmail.com", "ThisIsAvalidpass40", "Bob", "Cool")

def test_register_already_user():
    data = reset_data()
    data = setup_test_search()
    # already a user
    print(data)
    with pytest.raises(ValueError_http):
        auth_register("bob@gmail.com", "password", "user1", "user1_last")

def test_register_invalid_password():
    # invalid password
    with pytest.raises(ValueError_http):
        auth_register("sojin@gmail.com", "abc", "dtghdf", "dfghgf")

def test_register_tooLong_nameFirst():
    with pytest.raises(ValueError_http):
        auth_register("sojin@gmail.com", "abcdefghijk", "a"*51, 'name_last')

def test_register_tooLong_nameLast():
    with pytest.raises(ValueError_http):
        auth_register("sojin@gmail.com", "abcdefghijk", 'name_first', "a"*51)

def test_logout():
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder')
    logoutUser = auth_logout(user_1['token'])
    assert logoutUser == True


def test_auth_passwordreset_request_alright():
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder')
    resetCode_forTest = auth_passwordreset_request(user_1['email'])
    resetCode_dict = getDictFromResetCode(resetCode_forTest)
    assert resetCode_dict['email'] == user_1['email']
    
def test_auth_passwordreset_request_invalidEmail(setup1):
    # check the validity of email
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder')
    with pytest.raises(ValueError_http, match='Invalid email'):
        auth_passwordreset_request('invalid_email')
    with pytest.raises(ValueError_http, match='Invalid email'):
        auth_passwordreset_request('invalid_email@gmail')
    with pytest.raises(ValueError_http, match='Invalid email'):
        auth_passwordreset_request('invalid_email@.com')
    with pytest.raises(ValueError_http, match='Invalid email'):
        auth_passwordreset_request('@gmail.com')
    with pytest.raises(ValueError_http, match='Invalid email'):
        auth_passwordreset_request('invalid.com')
    with pytest.raises(ValueError_http, match='Invalid email'):
        auth_passwordreset_request('invalid @gmail.com')

def test_auth_passwordreset_reset_alright():
    # test if the function works properly
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder')
    resetCode_forTest = auth_passwordreset_request(user_1['email'])
    auth_passwordreset_reset(resetCode_forTest, 'new_password')

def test_auth_passwordreset_reset_VE_01():
    # invalid reset code
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder')
    resetCode_forTest = auth_passwordreset_request(user_1['email'])
    with pytest.raises(ValueError_http):
        auth_passwordreset_reset("Invalid reset_code", "12345678")

def test_auth_passwordreset_reset_VE_02():
    # valid reset code but invalid password
    data = reset_data()
    data = setup_test_search()
    user_1 = getUserByHandle('Builder')
    resetCode_forTest = auth_passwordreset_request(user_1['email'])
    with pytest.raises(ValueError_http):
        auth_passwordreset_reset(resetCode_forTest, "1234")

