import re
import jwt
from data_structure import *
from myemail import *
from random import randint
from Error import ValueError_http, AccessError

# Settings
SECRET = 'secret'
# Global variables
#token = 0

def check_valid_password(password):
    # check password validity
    if len(password) < 6:
        raise ValueError_http(
            "Invalid password; Password should contain at least 6 characters!")

# check email validity


def check_valid_email(email):
    data = getData()
    # need to include check for space
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email) or " " in email:
        raise ValueError_http("Invalid email")


def check_registered_email(email):
    data = getData()
    if userExists(email) is True:
        raise ValueError_http(description="Email already exists")


def check_valid_name(firstName, lastName):
    # check validity of first name and last name
    if len(firstName) > 50:
        raise ValueError_http("First name is too long!")
    if len(lastName) > 50:
        raise ValueError_http("Last name is too long!")


def auth_login(email, password):
    # check for valid email
    check_valid_email(email)
    # check if user exists
    if userExists(email) == False:
        raise ValueError_http("User does not exist")
    login_user = getUserByEmail(email)
    # check if password entered is corrects
    if password != login_user['password']:
        raise ValueError_http("Incorrect password")

    # generate token for logged in users
    login_user['token'] = str(jwt.encode(
        {'email': email}, SECRET, algorithm='HS256'))

    return {'u_id': login_user['u_id'], 'token': login_user['token']}


def auth_logout(token):
    # check for valid token
    logout_user = getUserFromToken(token)
    logout_user['token'] = None
    return True


def auth_register(email, password, name_first, name_last):
    data = getData()
    check_valid_email(email)
    check_registered_email(email)
    check_valid_password(password)
    check_valid_name(name_first, name_last)
    u_id = generateUid()
    token = str(jwt.encode({'email': email}, SECRET, algorithm='HS256'))
    data['users'].append({
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
        'token': str(token),
        'u_id': u_id,
        'handle_str' : name_first,
        'permission_id' : checkFirstUserPermission(),
        'joined_channels' : [],
        'profile_img_url' : "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg/440px-An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg"
    })
    return{'u_id': u_id, 'token': str(token)}

def auth_passwordreset_request(email):  
    data = getData()
    check_valid_email(email)
    #given an email, check that user is registered
    found_user = getUserByEmail(email)
    reset_resetCode(email)
    reset_code = str(randint(100000, 999999))
    data['resetCode'].append({
        'email' : email,
        'reset_code' : reset_code
    })
    return reset_code

def auth_passwordreset_reset(reset_code, new_password):
    data = getData()
    # check invalid password
    if len(new_password) < 6:
        raise ValueError_http("Invalid password")
    # check for valid reset code
    find_email = findResetcodeMatch(reset_code)
    user = getUserByEmail(find_email)
    user['password'] = new_password
    reset_resetCode(find_email)
    return()

if __name__ == '__main__':
    # data = getData()
    # token = auth_register("user1@gmail.com", "password", "name1", "name2")['token']
    # auth_register("user2@gmail.com", "password", "name1", "name2")
    # uid = auth_register("user3@gmail.com", "password", "name1", "name2")['u_id']

    # auth_login("user1@gmail.com", "password")
    # auth_login("user2@gmail.com", "password")
    # login_dict = auth_login("user3@gmail.com", "password")

    # resetCode = auth_passwordreset_request('user1@gmail.com')
    # resetCode2 = auth_passwordreset_request('user2@gmail.com')
    # print(data['resetCode'])
    # auth_passwordreset_reset(resetCode2, '222222')
    
    # admin_userpermission_change(tokenize('user1@gmail.com'), uid, 2)

    pass
