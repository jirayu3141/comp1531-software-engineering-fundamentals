from prefix import prefix_search
import pytest

def test_documentation():
    assert prefix_search({"ac": 1, "ba": 2, "ab": 3}, "a") == { "ac": 1, "ab": 3}

def test_exact_match():
    assert prefix_search({"category": "math", "cat": "animal"}, "cat") == {"category": "math", "cat": "animal"}

def test_same():
    assert prefix_search({"cat": "cat", "cat": "cat"}, "ca") == {"cat": "cat", "cat": "cat"}

def test_oneelement():
    assert prefix_search({"cat": "dog"}, "c") == {"cat": "dog"}

def test_degits():
    assert prefix_search({"5": 1, "6": 2, "56": 3}, "5") == { "5": 1, "56": 3}

    