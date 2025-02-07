from list_exercises import *
import pytest
def test_reverse():
    l = [0]
    reverse_list(l)
    assert l == [0]

    l = [-3, -2, -1, 0, 1, 2, 3]
    reverse_list(l)
    assert l == [3, 2, 1, 0, -1, -2, -3]

    # TODO Write more tests for reverse
    l = []
    reverse_list(l)
    assert l == []

    l = [1, 1, 1, 1]
    reverse_list(l)
    assert l == [1, 1, 1, 1]



def test_min():
    assert minimum([0]) == 0
    assert minimum([-3, -2, -1, 0, 1, 2, 3]) == -3
    # TODO Write more tests for minimum
    with pytest.raises(Exception):
        min([])
    



def test_sum():
    assert sum_list([0]) == 0
    assert sum_list([-3, -2, -1, 0, 1, 2, 3]) == 0
    # TODO Write more tests for sum
    #assert
