class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y

def get_data():
    global data
    return data

def reset_data():
    global data
    data = {
        'point': None,
    }

data = None
reset_data()

def fn_get():
    data = get_data()
    x = 0
    y = 0
    if data['point'] is not None:
        x = data['point'].getX()
        y = data['point'].getY()
    return (x, y)

def fn_create(x, y):
    data = get_data()
    data['point'] = Point(x, y)

def fn_update(x, y):
    data = get_data()
    data['point'].setX(x)
    data['point'].setY(y)

def fn_delete():
    data = get_data()
    data['point'] = None