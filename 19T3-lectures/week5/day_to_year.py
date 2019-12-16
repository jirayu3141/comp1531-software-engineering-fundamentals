from is_leap_year import is_leap_year

def day_to_year(days):
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
