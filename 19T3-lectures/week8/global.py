message = ["Hello", "I'm", "stored", "in", "a", "global", "variable"]

def example1():
    # Only reading from the variable; don't need global
    print(message)

def example2():
    # Modifying the list stored in the variable; don't need global.
    message[0] = "G'day"

def example3():
    # Calling a method on the object stored in the variable; don't need global
    message.append("mate")

def example4():
    # Assigning a new value to a variable; need global
    global message
    message = ["Good", "day", "sir", "I", "am", "a", "variable", "most", "global"]