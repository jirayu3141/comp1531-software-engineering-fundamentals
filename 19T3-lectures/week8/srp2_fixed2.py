class Message:
    def __init__(self, id, text):
        self.id = id
        self.text = text
        self.reacts = []

    def getId(self):
        return self.id

    def edit(self, new_text):
        self.text = new_text

    def react(self, react_id):
        self.reacts.append(react_id)

class Channel:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.messages = []

    def addMessage(self, message):
        self.messages.append(message)

    def getMessage(self, message_id):
        for message in self.messages:
            if message.getId() == message_id:
                return message

    def getMessages(self):
        return self.messages

if __name__ == '__main__':
    c = Channel(1, 'General')
    c.addMessage(Message(1200, 'Hello'))
    c.addMessage(Message(1201, 'How are you'))
    c.getMessage(1201).edit('How are you?')
    c.getMessage(1201).react(1)
    for m in c.getMessages():
        print(m.getText())
