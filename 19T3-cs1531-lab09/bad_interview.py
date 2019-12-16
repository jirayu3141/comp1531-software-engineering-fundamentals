def bad_interview():
    '''
    A generator that yields all numbers from 1 onward, but with some exceptions:
    * For numbers divisible by 3 it instead yields "Fizz"
    * For numbers divisible by 5 it instead yields "Buzz"
    * For numbers divisible by both 3 and 5 it instead yields "FizzBuzz"
    '''
    
    i = 1
    while i < 30:
        if i % 3 == 0 and i % 5 == 0:
            yield "FizzBuzz"
        elif i % 5 == 0:
            yield "Buzz"
        elif i % 3 == 0:
            yield "Fizz"
        else:
            yield i
        i += 1      
