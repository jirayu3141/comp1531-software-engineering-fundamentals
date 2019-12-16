from data_structure import *
from Error import AccessError, ValueError_http

channel_id = 0

def channel_invite(token, channel_id, u_id):
    data = getData()
    inviter_id = getUidFromToken(token)
    # check if u_id refers to a valid user
    isUidValid(u_id)
    # check if channel exists
    channel = getChannelFromChannelId(channel_id)
    # check if u_id is already in the channel
    if u_id in channel['all_members']:
        raise ValueError_http("User is already part of the channel")
    # # check if user is attempting to invite themself
    # if inviter_id == u_id:
    #     raise ValueError_http("You are not allowed to invite yourself")
    # check if authorized user is part of channel
    if inviter_id not in channel['all_members']:
        raise AccessError("Authorised user not a member of channel")
    # check permission of invited user
    invitee_permission = checkUserPermission(u_id)
    if invitee_permission == 1 or invitee_permission == 2:
        channel['owner_members'].append(u_id)
    
    channel['all_members'].append(u_id)
    details_channel = getChannelDetailsSimple(channel_id)
    getUserFromUid(u_id)['joined_channels'].append(details_channel)

    return()      
    
def channel_details(token, channel_id):
    data = getData()
    u_id = getUidFromToken(token)
    owner_members = []
    all_members = []
    # check if channel exists
    channel = getChannelFromChannelId(channel_id)
    # check if authorized user is a member of channel
    if u_id in channel['all_members']:
        name = channel['name']
        for owners in channel['owner_members']:
            owner_members_dic = getDetailsFromUid(owners)
            owner_members.append(owner_members_dic)
        for members in channel['all_members']:
            all_members_dic = getDetailsFromUid(members)
            all_members.append(all_members_dic)
        return {
            'name': name,
            'owner_members': owner_members,
            'all_members': all_members
        }
    else:
        raise AccessError("Authorized user not a member of channel")

def channel_messages(token, channel_id, start):
    data = getData()
    u_id = getUidFromToken(token)
    # check if channel exists
    channel = getChannelFromChannelId(channel_id)
    # check if authorized user is a member of channel
    if u_id not in channel['all_members']:
        raise AccessError("Authorised User not a member of channel")
    # check if there are no messages
    if len(channel['messages']) == 0:
        return {
            'messages' : [],
            'start' : start,
            'end' : start
        }
    # check if start < total number of messages
    if start < len(channel['messages']):
        if len(channel['messages'][start:]) > 50:
            end = start + 50
            mes = getMessages(u_id, channel['messages'], start, end)
        else:
            end = -1
            mes = getMessages(u_id, channel['messages'], start, end)
        return {
            'messages' : mes,
            'start' : start,
            'end' : -1
        }
    else:
        raise ValueError_http("Start is greater")            

def channel_leave(token, channel_id):
    data = getData()
    u_id = getUidFromToken(token)
    # check if channel exists
    channel = getChannelFromChannelId(channel_id)
    # check that u are a member of channel
    if u_id not in channel['all_members']:
        raise AccessError("You are not a member of this channel")
    channel['all_members'].remove(u_id)
    details_channel = getChannelDetailsSimple(channel_id)
    getUserFromToken(token)['joined_channels'].remove(details_channel)
    # check if empty channel
    if len(channel['all_members']) == 0:
        # delete channel
        data['channel'].remove(channel)

    return ()

def channel_join(token, channel_id):
    data = getData()
    u_id = getUidFromToken(token)
    # check if channel exists
    channel = getChannelFromChannelId(channel_id)
    # check if channel_id is private
    if channel['is_public'] == False:
        raise AccessError("You cannot join a private channel")
    # check permission of invited user
    permission = checkUserPermission(u_id)
    if permission == 1 or permission == 2:
        channel['owner_members'].append(u_id)
    channel['all_members'].append(u_id)
    details_channel = getChannelDetailsSimple(channel_id)
    getUserFromToken(token)['joined_channels'].append(details_channel)
    return ()          

def channel_addowner(token, channel_id, u_id):
    data = getData()
    adder_id = getUidFromToken(token)
    # check if channel exists
    channel = getChannelFromChannelId(channel_id)
    # check if authorized user is an owner of slackr / owner of channel
    if adder_id not in channel['owner_members']:
        raise AccessError("You are not authorized to add an owner")
    # check if user is already an owner of channel / member of channel
    if u_id in channel['owner_members']:
        raise ValueError_http("User is already an owner of the channel")
    # check if user is a member of the channel
    if u_id not in channel['all_members']:
        raise ValueError_http("User is not a member of the channel")
    channel['owner_members'].append(u_id)
    return ()

def channel_removeowner(token, channel_id, u_id):
    data = getData()
    remover_id = getUidFromToken(token)
    # check if channel exists
    channel = getChannelFromChannelId(channel_id)
    # check if authorized user is an owner of slackr / owner of channel
    if remover_id not in channel['owner_members']:
        raise AccessError("You are not authorized to remove an owner")
    # check if authorized user is the only owner and they are attempting to remove themself
    if len(channel['owner_members']) == 1 and remover_id in channel['owner_members']:
        raise ValueError_http("You cannot remove yourself as an owner because you are the only owner")
    # check if user is not an owner of channel
    if u_id in channel['owner_members']:
        channel['owner_members'].remove(u_id)
        return()
    else:
        raise ValueError_http("User is not an owner of the channel")

def channels_list(token):
    data = getData()
    user = getUserFromToken(token)
    channel_list = []
    for channel in user['joined_channels']:
        channel_dic = {
            'channel_id' : channel['channel_id'],
            'name' : channel['name']
        }
        channel_list.append(channel_dic)
    return {
        'channels': channel_list
    }

def channels_listall(token):
    data = getData()
    channel_list = []
    for channel in data['channel']:
        channel_dic = {
            'channel_id' : channel['channel_id'],
            'name' : channel['name']
        }
        channel_list.append(channel_dic)
    return {
        'channels': channel_list
    }

def channels_create(token, name, is_public):
    global channel_id
    data = getData()
    u_id = getUidFromToken(token)

    # check if length of name <= 20
    if len(name) <= 20:
        # CREATE CHANNEL ID
        channel_id += 1
        channel_dic = {
            'channel_id' : channel_id,
            'name' : name,
            'is_public' : is_public,
            'all_members' : [u_id],
            'owner_members' : [u_id],
            'messages' : [],
            'standup_msg' : "",
            'standup_active': False,
            'standup_finish': 0,
            'standup_started_by' : None
        }
        channel_dic2 = {
            'channel_id' : channel_id,
            'name' : name
        }
        data['channel'].append(channel_dic)
        getUserFromToken(token)['joined_channels'].append(channel_dic2)

        return {
            'channel_id': channel_id
        }
    else:
        raise ValueError_http(
            "The name of the channel cannot be longer than 20 characters")