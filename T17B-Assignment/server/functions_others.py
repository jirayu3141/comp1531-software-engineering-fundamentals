import re
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from Error import AccessError, ValueError_http
from data_structure import getData, getUserById, user_is_in_channel, getUserFromToken, getUidFromToken
from datetime import datetime
from json import dumps
from werkzeug.exceptions import HTTPException

def check_last_owner(u_id):
    data = getData()
    foundOwner = 0
    foundUser = getUserById(u_id)
    for user in data['users']:
        if user['permission_id'] == 1:
            foundOwner += 1
    return foundOwner

def search(token, query_str):
    data = getData()
    returnMessage = []
    u_id = getUidFromToken(token)
    # condition for query_str is an empty string
    if query_str == '':
        return []
    # search for messages with query_str and add to returnMessage 
    for channels in data['channel']:
        if u_id in channels['all_members']:
            for msg in channels['messages']:
                    if re.search(query_str.lower(), msg['message'].lower()):
                        returnMessage.append(msg)
    # print(returnMessage)
    return returnMessage

def admin_userpermission_change(token, u_id, permission_id):
    # check if permission_id is a valid value for permission_id
    if permission_id != 1 and permission_id != 2 and permission_id != 3:
        raise ValueError_http("Permission_id doesn't refer to a value permission.")

    foundUser1 = getUserFromToken(token)
    # check if token is valid
    foundUser2 = getUserById(u_id)
    # check if u_id is valid

    # check if token refer to a member, not an admin or owner 
    if foundUser1['permission_id'] == 3:
        raise AccessError("Authorised user is not an admin or owner")
    # check if token refers to admin  
    elif foundUser1['permission_id'] == 2:
        # u_id refers to member
        if foundUser2['permission_id'] == 3:
            # permission_id is 3 (member)    
            if permission_id == 3:
                raise ValueError_http("User is already a member.")
            # permission_id is 2 (admin)    
            elif permission_id == 2:
                foundUser2['permission_id'] = 2
            # permission_id is 2 (owner)
            elif permission_id == 1:
                raise ValueError_http("Authorised user is not an owner.")
        # u_id refers to an admin
        elif foundUser2['permission_id'] == 2:
            # permission_id is 3 (member)    
            if permission_id == 3:
                foundUser2['permission_id'] = 3
            # permission_id is 2 (admin)    
            elif permission_id == 2:
                raise ValueError_http("User is already an admin.")
            elif permission_id == 1:
                raise ValueError_http("Authorised user is not an owner.")
        # u_id refers to an owner
        elif foundUser2['permission_id'] == 1:
            # permission_id is 3 (member)    
            if permission_id == 3:
                raise ValueError_http("Authorised user is not an owner.")
            # permission_id is 2 (admin)    
            elif permission_id == 2:
                raise ValueError_http("Authorised user is not an owner.")
            elif permission_id == 1:
                raise ValueError_http("Authorised user is not an owner.")
    # check if token refers to an owner
    elif foundUser1['permission_id'] == 1:
        # u_id refers to a member
        if foundUser2['permission_id'] == 3:
            # permission_id is 3 (member)    
            if permission_id == 3:
                raise ValueError_http("User is already a member.")
            # permission_id is 2 (admin)    
            elif permission_id == 2:
                foundUser2['permission_id'] = 2                
            # permission_id is 2 (owner)
            elif permission_id == 1:
                foundUser2['permission_id'] = 1
        # u_id refers to an admin        
        elif foundUser2['permission_id'] == 2:
            # permission_id is 3 (member)    
            if permission_id == 3:
                foundUser2['permission_id'] = 3
            # permission_id is 2 (admin)    
            elif permission_id == 2:
                raise ValueError_http("User is already an admin.")
            elif permission_id == 1:        
                foundUser2['permission_id'] = 1
        # u_id refers to an owner        
        elif foundUser2['permission_id'] == 1:
            if foundUser1 == foundUser2:
                foundOwner = check_last_owner(u_id)
                if foundOwner == 1:
                    raise ValueError_http("You're the last owner!")
                elif foundOwner > 1:
                    foundUser2['permission_id'] = 1
            # permission_id is 3 (member)    
            if permission_id == 3:
                foundUser2['permission_id'] = 3
            # permission_id is 2 (admin)    
            elif permission_id == 2:
                foundUser2['permission_id'] = 2
            elif permission_id == 1:
                raise ValueError_http("User is already an owner.")
    return ({})