from is_leap_year import is_leap_year

def test_is_leap_year():
    assert is_leap_year(2004)
    assert not is_leap_year(2019)
    assert not is_leap_year(2100)
    assert is_leap_year(4000)