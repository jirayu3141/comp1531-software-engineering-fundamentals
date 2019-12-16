"""
This is a simple flask app where you can send an email from a
gmail account. To do this:

1) Setup a team gmail account with a username/password
2) Follow these instructions to allow gmail to be OK with these emails
   https://www.dev2qa.com/how-do-i-enable-less-secure-apps-on-gmail/
3) Fill in the username and password in this script
4) Run the flask app, and access /send-mail

"""

from flask import Flask
from flask_mail import Mail, Message

APP = Flask(__name__)
APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'my.gmail@gmail.com',
    MAIL_PASSWORD = ""
)

@APP.route('/send-mail/')
def send_mail():
    mail = Mail(APP)
    try:
        msg = Message("Send Mail Test!",
            sender="my.gmail@gmail.com",
            recipients=["person.sending.to@gmail.com"])
        msg.body = "Hello! This is a test body"
        mail.send(msg)
        return 'Mail sent!'
    except Exception as e:
        return (str(e))

if __name__ == '__main__':
    APP.run()

# 