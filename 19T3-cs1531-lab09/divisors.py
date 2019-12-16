import inspect

def divisors(n):
    '''
    Given some number n, this generator yields all positive integer divisors of n in ascending order. For example:
    >>> list(divisors(12))
    [1, 2, 3, 4, 6, 12]
    '''
    #list = (i for i in range(1,n+1) if n % i == 0)

    for i in range(1,n+1):
        if n % i == 0:
            yield i


