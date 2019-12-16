from balanced import balanced
from hypothesis import given, strategies
import inspect

def test_generator():
    '''
    Ensure it is generator function
    '''
    assert inspect.isgeneratorfunction(balanced), "balanced does not appear to be a generator"
