from permutations import permutations
from hypothesis import given, strategies, assume
import inspect

def test_generator():
    '''
    Ensure it is generator function
    '''
    assert inspect.isgeneratorfunction(permutations), "permutations does not appear to be a generator"

def test_others():
    pass