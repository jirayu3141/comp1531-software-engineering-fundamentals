import pytest
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
from test_others import setup_test_search
from data_structure import getUidFromToken, getData, reset_data, getUserByHandle
from unittest.mock import patch
#from functions_channel import channels_create
#import http.client  


def test_user_profile_alright():
    data = reset_data()
    #create some users
    email1 = "sally@gmail.com"
    name_first1 = "Super"
    name_last1 = "Sally"
    authRegisterDict = auth_register(email1, "GoodPassword1", name_first1, name_last1)
    token1 = authRegisterDict['token']
    uid1 = getUidFromToken(token1)
    
    #do some tests
    profile = user_profile(token1, uid1)
    ''' test that the returned values are correct '''
    assert(profile['email']) == email1
    assert(profile['name_first']) == name_first1
    assert(profile['name_last']) == name_last1
    assert(profile['handle_str']) == name_first1
    
def test_user_profile_invalidToken():
    data = reset_data()
    #create some users
    email1 = "sally@gmail.com"
    name_first1 = "Super"
    name_last1 = "Sally"
    authRegisterDict = auth_register(email1, "GoodPassword1", name_first1, name_last1)
    token1 = authRegisterDict['token']
    uid1 = getUidFromToken(token1)

    #do some tests
    ''' test that function rasies error if token doesn't belong to the correct user '''
    with pytest.raises(ValueError_http):
        profile = user_profile('wrong', uid1)

def test_user_profile_invalidId():
    data = reset_data()
    #create some users
    email1 = "sally@gmail.com"
    name_first1 = "Super"
    name_last1 = "Sally"
    authRegisterDict = auth_register(email1, "GoodPassword1", name_first1, name_last1)
    token1 = authRegisterDict['token']
    uid1 = getUidFromToken(token1)

    #do some tests
    ''' test that error is raised if u_id is not a valid user '''
    with pytest.raises(ValueError_http):
        profile = user_profile(token1, 6508)


def test_user_profile_setname_alright():
    data = reset_data()
    #create some users
    email1 = "sally@gmail.com"
    name_first1 = "Super"
    name_last1 = "Sally"
    authRegisterDict = auth_register(email1, "GoodPassword1", name_first1, name_last1)
    token1 = authRegisterDict['token']
    uid1 = getUidFromToken(token1)

    #do some tests
    ''' function runs fine if everything is valid '''
    #initially the user's name is sally, and is changed to NewSally
    user_profile_setname(token1, 'NewSuper', 'NewSally')
    profile2 = user_profile(token1, uid1)
    #print(userProfileDict2)
    assert(profile2['name_first']) == "NewSuper"
    assert(profile2['name_last']) == "NewSally"
    

def test_user_profile_setname_tooLong():
    data = reset_data()
    #create some users
    email1 = "sally@gmail.com"
    name_first1 = "Super"
    name_last1 = "Sally"
    authRegisterDict = auth_register(email1, "GoodPassword1", name_first1, name_last1)
    token1 = authRegisterDict['token']
    uid1 = getUidFromToken(token1)

    #do some tests
    ''' error is raised when name_first is more than 50 characters '''
    with pytest.raises(ValueError_http):
        user_profile_setname(token1, "a"*51, "evans")

    ''' error is raised when name_last is more than 50 characters '''
    with pytest.raises(ValueError_http):
        user_profile_setname(token1, "james", "a"*51)


def test_user_profile_setemail_alright():
    data = reset_data()
    #create some users
    email1 = "sally@gmail.com"
    name_first1 = "Super"
    name_last1 = "Sally"
    authRegisterDict = auth_register(email1, "GoodPassword1", name_first1, name_last1)
    token1 = authRegisterDict['token']
    uid1 = getUidFromToken(token1)

    #do some tests
    ''' function runs fine under normal condition '''
    ''' check that email is changed to desired email input '''
    user_profile_setemail(token1, "new_email@gmail.com")
    profile = user_profile(token1, uid1)
    newEmail = profile['email']
    assert newEmail == "new_email@gmail.com"

def test_user_profile_setemail_invalidEmail():
    data = reset_data()
    #create some users
    email1 = "sally@gmail.com"
    name_first1 = "Super"
    name_last1 = "Sally"
    authRegisterDict = auth_register(email1, "GoodPassword1", name_first1, name_last1)
    token1 = authRegisterDict['token']
    uid1 = getUidFromToken(token1)

    #do some tests
    ''' fucntion fails if email entered is invalid '''
    # No prefix
    with pytest.raises(ValueError_http):
        user_profile_setemail(token1, "@gmail.com")
    # No suffix
    with pytest.raises(ValueError_http):
        user_profile_setemail(token1, "sally@.com")
    # No .com
    with pytest.raises(ValueError_http):
        user_profile_setemail(token1, "sally@gmail.")
    # no @
    with pytest.raises(ValueError_http):
        user_profile_setemail(token1, "sallygmail.com")

def test_user_profile_setemail_usedEmail():
    data = reset_data()
    #create some users
    email1 = "sally@gmail.com"
    name_first1 = "Super"
    name_last1 = "Sally"
    authRegisterDict = auth_register(email1, "GoodPassword1", name_first1, name_last1)
    token1 = authRegisterDict['token']
    uid1 = getUidFromToken(token1)

    email2 = "bob@gmail.com"
    name_first2 = "Builder"
    name_last2 = "Bob"
    authRegisterDict2 = auth_register(email2, "GoodPassword2", name_first2, name_last2)
    token2 = authRegisterDict2['token']
    uid2 = getUidFromToken(token2)

    #do some tests
    ''' function fails if email has been used by another user '''
    with pytest.raises(ValueError_http):
        user_profile_setemail(token1, email2)
    
def test_user_profile_setemail_invalidToken():
    data = reset_data()
    #do some tests
    # user with token not registered/invalid
    with pytest.raises(ValueError_http):
        user_profile_setemail('token_invalid', 'hp@gmail.com')
    

def test_user_profile_sethandle_alright():
    data = reset_data()
    #create some users
    email1 = "sally@gmail.com"
    name_first1 = "Super"
    name_last1 = "Sally"
    authRegisterDict = auth_register(email1, "GoodPassword1", name_first1, name_last1)
    token1 = authRegisterDict['token']
    uid1 = getUidFromToken(token1)

    #do some tests
    ''' function runs fine under normal condition '''
    user_profile_sethandle(token1, 'new_handle')
    profile = user_profile(token1, uid1)
    newHandle = profile['handle_str']
    assert newHandle == 'new_handle'
    
def test_user_profile_sethandle_usedHandle():
    data = reset_data()
    #create some users
    email1 = "sally@gmail.com"
    name_first1 = "Super"
    name_last1 = "Sally"
    authRegisterDict = auth_register(email1, "GoodPassword1", name_first1, name_last1)
    token1 = authRegisterDict['token']
    uid1 = getUidFromToken(token1)

    email2 = "bob@gmail.com"
    name_first2 = "Builder"
    name_last2 = "Bob"
    authRegisterDict2 = auth_register(email2, "GoodPassword2", name_first2, name_last2)
    token2 = authRegisterDict2['token']
    uid2 = getUidFromToken(token2)

    #do some tests
    # function fails if handle used by other
    with pytest.raises(ValueError_http):
        user_profile_sethandle(token1, name_first2)
    
def test_user_profile_sethandle_invalidToken():
    data = reset_data()
    #do some tests
    # function fails if token not valid
    with pytest.raises(ValueError_http):
        user_profile_sethandle('tscevr', 'new_handle')
    
def test_user_profile_sethandle_tooLong():
    data = reset_data()
    #create some users
    email1 = "sally@gmail.com"
    name_first1 = "Super"
    name_last1 = "Sally"
    authRegisterDict = auth_register(email1, "GoodPassword1", name_first1, name_last1)
    token1 = authRegisterDict['token']
    uid1 = getUidFromToken(token1)

    #do some tests
    ''' error raised when handle_str is more than 20 characters '''
    with pytest.raises(ValueError_http):
        user_profile_sethandle(token1, "a"*21)
    
def test_user_profile_sethandle_tooShort():
    data = reset_data()
    #create some users
    email1 = "sally@gmail.com"
    name_first1 = "Super"
    name_last1 = "Sally"
    authRegisterDict = auth_register(email1, "GoodPassword1", name_first1, name_last1)
    token1 = authRegisterDict['token']
    uid1 = getUidFromToken(token1)

    #do some tests
    # error raised when handle lower than 3 characters
    with pytest.raises(ValueError_http):
        user_profile_sethandle(token1, "a"*2)

def test_users_all_alright():
    data = reset_data()
    #create some users
    email1 = "sally@gmail.com"
    name_first1 = "Super"
    name_last1 = "Sally"
    authRegisterDict = auth_register(email1, "GoodPassword1", name_first1, name_last1)
    token1 = authRegisterDict['token']
    uid1 = getUidFromToken(token1)
    profile1 = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg/440px-An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg"

    email2 = "bob@gmail.com"
    name_first2 = "Builder"
    name_last2 = "Bob"
    authRegisterDict2 = auth_register(email2, "GoodPassword2", name_first2, name_last2)
    token2 = authRegisterDict2['token']
    uid2 = getUidFromToken(token2)
    profile2 = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg/440px-An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg"

    
    #do some tests
    # test if the function works properly
    profile = users_all(token1)
    # List of dictionaries, where each dictionary contains types 
    # u_id, email, name_first, name_last, handle_str, profile_img_url
    print(profile)
    assert profile == {'users': [{
        'u_id': uid1,
        'email': email1,  
        'name_first': name_first1, 
        'name_last': name_last1, 
        'handle_str': name_first1,
        'profile_img_url': profile1
        },{ 
        'u_id': uid2,
        'email': email2, 
        'name_first': name_first2, 
        'name_last': name_last2, 
        'handle_str': name_first2,
        'profile_img_url': profile2
        }]
    }

def test_users_all_invalidToken():
    data = reset_data()
    # test if user is a valid user
    with pytest.raises(ValueError_http):
        users_all('whatever')

# def test_upload_photo_valid():
#     reset_data()
#     #create user
#     token = auth_register('user_test@gmail.com', 'password', 'name', 'name')["token"]
#     #upload some photo
#     user_profiles_uploadphoto(token, 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQSnAObADKlIZbzf5L-FP55P7wlU2wBPtlC8fsifHXWoKwCD31e', 0,0, 100,100)
    
    
def test_upload_photo_invalid_dim():
    reset_data()
    #create user
    token = auth_register('user_test@gmail.com', 'password', 'name', 'name')["token"]
    #upload some photo
    with pytest.raises(ValueError_http):
        user_profiles_uploadphoto(token, 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQSnAObADKlIZbzf5L-FP55P7wlU2wBPtlC8fsifHXWoKwCD31e', 0,100, 10,10)


def test_upload_photo_invalid_url0():
    reset_data()
    #create user
    token = auth_register('user_test@gmail.com', 'password', 'name', 'name')["token"]
    #upload some photo
    with pytest.raises(AccessError):
        user_profiles_uploadphoto(token, 'https://stackoverflow.com/quest', None, None, None, None)


# def test_upload_photo_default():
#     reset_data()
#     #create user
#     token = auth_register('user_test@gmail.com', 'password', 'name', 'name')["token"]
#     #upload some photo
#     user_profiles_uploadphoto(token, 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQSnAObADKlIZbzf5L-FP55P7wlU2wBPtlC8fsifHXWoKwCD31e', x_start=None, y_start=None, x_end=None, y_end=None)

def test_upload_photo_invalid_url1():
    reset_data()
    #create user
    token = auth_register('user_test@gmail.com', 'password', 'name', 'name')["token"]
    #upload some photo
    with pytest.raises(AccessError):
        user_profiles_uploadphoto(token, 'www.google.com', x_start=None, y_start=None, x_end=None, y_end=None)

def test_upload_photo_invalid_url2():
    reset_data()
    #create user
    token = auth_register('user_test@gmail.com', 'password', 'name', 'name')["token"]
    #upload some photo
    with pytest.raises(AccessError):
        user_profiles_uploadphoto(token, 'asdf', x_start=None, y_start=None, x_end=None, y_end=None)
