from hypothesis import given, strategies, settings, Verbosity

def bubblesort(numbers):
    numbers = numbers.copy()
    for _ in range(0, len(numbers) - 1):
        for i in range(0, len(numbers) - 1):
            if numbers[i] > numbers[i+1]:
                numbers[i], numbers[i+1] = numbers[i+1], numbers[i]
    return numbers

def is_sorted(numbers):
    for i in range(0, len(numbers) - 1):
        if numbers[i] > numbers[i+1]:
            return False
    return True

@given(strategies.lists(strategies.integers()))
def test_sort_permutation(numbers):
    result = bubblesort(numbers)
    for n in numbers:
        assert n in result
    for r in result:
        assert r in numbers

@given(strategies.lists(strategies.integers()))
def test_length_sorted(numbers):
    assert len(numbers) == len(bubblesort(numbers))

@given(strategies.lists(strategies.integers()))
def test_sort_is_sorted(numbers):
    assert is_sorted(bubblesort(numbers))

@given(strategies.lists(strategies.integers()))
# @settings(verbosity=Verbosity.verbose)
def test_bubblesort_idempotent(numbers):
    assert bubblesort(bubblesort(numbers)) == bubblesort(numbers)


@given(strategies.lists(strategies.integers()))
def test_bubblesort_sort(numbers):
    assert bubblesort(numbers) == sorted(numbers)