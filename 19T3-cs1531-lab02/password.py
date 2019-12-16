import string
import pytest
import re

def check_password(password):
    '''
    Takes in a password, and returns a string based on the strength of that password.

    The returned value should be:
    * "Strong password", if at least 12 characters, contains at least one number, at least one uppercase letter, at least one lowercase letter.
    * "Moderate password", if at least 8 characters, contains at least one number.
    * "Poor password", for anything else
    * "Horrible password", if the user enters "password", "iloveyou", or "123456"
    '''

    
    '''
    flag = 0 poor 1 = moderate 2 = strong
    '''
    flag = 0
    
    if len(password) >= 8:
        for x in password:
            if x in string.digits:
                flag = 1
        
            
    if len(password) >= 12:
        if re.search("[0-9]", password):
            if re.search("[A-Z]", password):
                if re.search("[a-z]", password):
                    flag = 2

    if password == "iloveyou" :
        flag = -1
    elif password == "password":
        flag = -1
    elif password == "123456":
        flag = -1


    if flag == -1:
        return "Horrible password"
    elif flag == 0:
        return "Poor password"
    elif flag == 1:
        return "Moderate password"
    elif flag == 2:
        return "Strong password" 





def test_horrible():
    assert check_password("123456") == "Horrible password"
    assert check_password("iloveyou") == "Horrible password"
    assert check_password("password") == "Horrible password"

def test_poor():
    assert check_password("123") == "Poor password"
    assert check_password("hi") == "Poor password"
    assert check_password("this is really long") == "Poor password"
    assert check_password("") == "Poor password"
    
def test_moderate():
    assert check_password("12341934871893479") == "Moderate password"
    assert check_password("1234567a") == "Moderate password"
    assert check_password("1234567891a") == "Moderate password"
    assert check_password("thisis123!!!!@#$%^&*") == "Moderate password"
    assert check_password("thisadfadfadfadfs123") == "Moderate password"
    assert check_password("Thisis123") == "Moderate password"
    assert check_password("THIS12345") == "Moderate password"
    assert check_password("12345673134234ABC") == "Moderate password"

def test_strong():
    assert check_password("1234567899aBc") == "Strong password"
    assert check_password("12345678900000000!Cc") == "Strong password"
    



            


#     pass

# if __name__ == '__main__':
#       return(check_password("ihearttrimesters"))