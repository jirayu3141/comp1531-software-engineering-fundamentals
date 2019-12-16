def simple_generator():
    print("Hello")
    yield 1
    print("Nice to meet you")
    yield 2
    print("I am a generator")

for i in simple_generator():
    print(i)
