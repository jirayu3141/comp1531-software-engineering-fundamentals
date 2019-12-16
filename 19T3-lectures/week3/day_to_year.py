from is_leap_year import is_leap_year

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
