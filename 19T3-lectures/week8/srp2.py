class Channel:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.messages = []

    def addMessage(self, id, text):
        self.messages.append({
            'id': id,
            'text': text,
            'reacts' : []
        })

    def editMessage(self, message_id, new_text):
        for message in self.messages:
            if message['id'] == message_id:
                message['text'] = new_text

    def reactToMessage(self, message_id, react_id):
        for message in self.messages:
            if message['id'] == message_id:
                message['reacts'].append(react_id)

    def getMessages(self):
        return self.messages

if __name__ == '__main__':
    c = Channel(1, 'General')
    c.addMessage(1200, 'Hello')
    c.addMessage(1201, 'How are you')
    c.editMessage(1201, 'How are you?')
    c.reactToMessage(1201, 1)
    for m in c.getMessages():
        print(m['text'])
