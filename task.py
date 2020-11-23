def leap_yr(year):
    """Helper func: Returns true if it's a leap year and False if it's not"""

    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

