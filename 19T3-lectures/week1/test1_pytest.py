import pytest

def sum(x, y):
    return x + y

def multiply(x, y):
    return x * y

def test_sum1():
    assert sum(1, 2) == 3, "1 + 2 == 3"
def test_sum2():
    assert sum(1, 4) == 5, "1 + 4 == 5"
def test_sum3():
    assert sum(1, 7) == 8, "1 + 7 == 8"
