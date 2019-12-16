# Function Specific Assumptions (Channel functions)

- `channel_leave(token, channel_id)` : Assume that the function is only called if the user is part of the channel they wish to leave. 
  - if the last person leave the channel, the channel gets deleted 

- `channel_addowner(token, channel_id, u_id)` : Assume that user needs to be a member of the channel to be able to become an owner. Currently there is no way to check whether a user is an owner of the slackr.

- `channel_removeowner(token, channel_id, u_id)` : Assume that if you are the only owner, you cannot remove yourself as an owner.

# Function Specific Assumptions (Message functions)
- `message_remove(token, message_id)` : Unable to test for the last 2 AccessErrors as the specifications are unclear; we will assume that the first error took care of all cases.

- `message_edit(token, message_id, message)`: Assume user cannot edit any messages in channels they are not part of.

- `message_react(token, message_id, react_id)` : Assume user cannot react to any messages in the channels they aren't part of.

- `message_unreact(token, message_id, react_id)` : Assume user cannot unreact to any messages in channels they are not part of.

- `message_pin(token, message_id, react_id)` : Assume user cannot pin any messages in channels they are not part of.

- `message_unpin(token, message_id, react_id)` : Assume user cannot unpin any messages in channels they are not part of.

# Function Specific Assumptions (User functions)

- `user_profile(token, u_id)`: return handle_str in the format of "name_first name_last" if it is not modified. "name_first name_last" format is used for testing that default return value is correct. 

- `admin_permission_change()`: Last owner cannot lower his status

- `user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end)` : if dimensions are not given, make it the size of the input image