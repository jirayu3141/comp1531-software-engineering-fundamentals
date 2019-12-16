from is_leap_year import is_leap_year

def day_to_year(days):
    year = 1970

    while days > 0:
        if is_leap_year(year):
            days -= 366
        else:
            days -= 365
        year += 1

    return year - 1
