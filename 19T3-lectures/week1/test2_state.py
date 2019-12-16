import pytest

a = 5
def increment():
	a += 1
def getA():
	return a

def sum(x, y):
    return x * y

def test_sum1():
	increment()
	print(getA())

def test_sum1():
	increment()
	print(getA())