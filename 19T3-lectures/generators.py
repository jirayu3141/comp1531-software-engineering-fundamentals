def encode(string):
    num = 0
    curr = string[0]
    for c in string:
        if c != curr:
            yield(curr, num)
            num = 1
            curr = c
        else:
            num += 1
    yield(curr, num)


def decode(encoded):
    s = ""
    for a, b in encoded:
        s += a * b
    return s




def simpleGenerator():
    yield 1
    yield 2
    yield 3


def main1():
    print(decode(encode("hheeyyya")))
    for x, y in encode("hheeyaa"):
        print(f"{x} was seen {y} times")

def main2():
    for value in simpleGenerator():
        print(value)
    
#generator object
def main3():
if __name__ == "__main__":
    main2()