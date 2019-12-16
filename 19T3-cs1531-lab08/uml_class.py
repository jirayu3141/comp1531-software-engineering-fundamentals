
class order():
    def __init__(self, fruit, quantity, status):
        self.fruit = fruit()
        self.quantity = quantity
        self.whole_seller = []
        self.status = None

class whole_seller():
    def __init__(self, order):
        order = []

class fruit():
    def __init__(self, fruit_type, price, availability):
        self.fruit_type = fruit_type
        self.price = price
        self.availability = None

class delivery():
    def __init__(self, whole_seller):
        self.whole_seller = []
    
    def fulfuill_order(self, order):
        order.status = "Finished"
        pass
