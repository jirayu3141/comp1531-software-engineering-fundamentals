animals = ["dog", "cat", "chicken", "sheep"]

animal_iterator = iter(animals)

class Squares:
    def __init__(self):
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.i += 1
        if (self.i > 200):
            raise StopIteration
        return self.i*self.i

squares = Squares()

for s in squares:
    print(s)