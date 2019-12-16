from is_leap_year import is_leap_year

from hypothesis import given, strategies, Verbosity, settings

def day_to_year(days):
    '''
    Given a number of days from January 1st 1970, return the year.
    '''
    year = 1970

    while days > 365:
        if is_leap_year(year):
            if days > 366:
                days -= 366
                year += 1
        else:
            days -= 365
            year += 1

    return year

@given(strategies.integers(min_value=0))
def test_non_leap(days):
    day_to_year(days) <= days // 365 + 1970