class Squares:
    def __init__(self):
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.i += 1
        return self.i*self.i

def squares():
    i = 0
    while True:
        i += 1
        yield i*i
