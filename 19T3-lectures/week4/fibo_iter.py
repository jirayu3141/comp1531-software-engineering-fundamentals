class Fibonacci():
    def __init__(self):
        self.previous = 0
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > 1000:
            raise StopIteration()
        subsequent = self.current + self.previous
        self.previous = self.current
        self.current = subsequent
        return self.previous

for i in Fibonacci():
    print(i)
