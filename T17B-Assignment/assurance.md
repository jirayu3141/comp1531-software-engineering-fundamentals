Verification and Validation are two of the most important aspects of software management. In essence, verification denotes whether a system is being developed in a correct way, while validation refers to the quality management process: determining whether a correct software has been produced. To make sure that our system is both verified, and validated, we employed several techniques and tools. 

Using the Acceptance Testing method, we created a specific acceptance criteria for each user story to test that our system satisfies all the user requirements. We created the following list of acceptance criteria:

As a user, I want to have my own account so that other people can identify me and I can have personalized content.

    -	There is a register button placed at the top of the slackr home page. After clicking on that, the user will be redirected to a page which asks for the user’s personal information (like email, first and last name, and display/username i.e. handle_str);
    -	It will tell them to set a password for the account;
    -	Then by clicking on the sign up button on the bottom, (assuming the entered email is valid and exists), will be directed to the login page.
    
As a user, I want to reset my password when I forget it or want to have a stronger password to secure my account.

    -	After clicking on the ‘forgot password’ button on the slackr home page, user will be asked to fill in the email field with their email
    -	Then, if the email is valid and registered, the user will be sent an email with a reset code
    -	Entering that code back in the slackr page will enable user to set a new password, then confirm the password and login.
    
As a user, I want to have different sub-topics (channel) so I can categorize the content.

    -	Once logged in, the user can create a channel, by clicking on the plus button displayed to the left task board of slackr.
    -	Then a popup box will allow the user to name the channel, and add other members to it, and set privacy status.
    -	Doing this will add the channel on the left sidebar  
    -	By creating the channel, the user automatically becomes the owner of that channel, and can make other members admin of owner.
    
As a user, I want to manage privacy of the channel so I can prevent unauthorized access.

    -	The user can access the is_public criteria of a channel
    -	By changing it to private, user can control who can access the channel
    
As a user, I want to see who are in the channel and their status so I know who can see my messages.

    - The user can go to settings in a channel.
    - There, the user can view all the members of that channel.
    
As a user, I want to invite other users to the channel so I can work in a team.

    - On the display side board of slackr, there will be a 'invite people' button. 
    - Clicking on that will bring up a popup box, in which the user has to fillin details of members that he wants to add to the channel
    - Then clicking on the invite button on the bottom will enable user to add those members
    
As a user, I want to join/leave a channel so I can part of the conversion if I choose to.

    - Going to the settings on a particular channel will enable user to leave, by clicking on leave channel
    - User can join a channel only after getting an invitation and clicking on it.
    
As a channel owner, I want to make other people an owner so they can help me manage the channel.

    - If the user is the owner or admin of a particular channel, then he can make others admin or owner by changing their permission_id.


To demonstrate assurance, our team has utilized several tools such as 'coverage' and 'pylint'. Using coverage.py (specifically branch coverage), we could detect areas of the code that were not being executed by the tests, and used this information to add to the tests to ensure maximum code coverage. Also, using pylint, we could analyze our code and detect any errors, and potential errors, and make adjustments accordingly, to ensure that our system is behaving correctly.
