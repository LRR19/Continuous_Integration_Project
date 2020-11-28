import math

hour = 3600
day = 86400
week = 604800
month = 2629743
year = 31556926
epoc_year = 1970
epoc_month = 1
epoc_day = 1


def leap_yr(lp_year):
    """Helper func: Returns true if it's a leap year and False if it's not"""
    return lp_year % 4 == 0 and (lp_year % 100 != 0 or lp_year % 400 == 0)


def calc_year(secs) -> (int, float):
    """Converts seconds to a year"""
    some_year = secs / year
    # take the number before the decimal
    a_year = some_year // 1
    a_year_remainder = some_year % 1
    return math.trunc(a_year), a_year_remainder


def calc_month(secs) -> (int, float):
    """Converts seconds to a month"""
    y, y_remainder = calc_year(secs)
    remaining_sec_in_year = y_remainder * year
    month_from_remainder = remaining_sec_in_year / month
    a_month = month_from_remainder // 1
    a_month_remainder = month_from_remainder % 1
    return math.trunc(a_month), a_month_remainder


def calc_day(secs) -> (int, float):
    """Converts seconds to a day"""
    m, m_remainder = calc_month(secs)
    remaining_sec_in_month = m_remainder * month
    day_from_remainder = remaining_sec_in_month / day
    a_day = round(day_from_remainder, 4)
    a_day_remainder = day_from_remainder % 1
    return math.trunc(a_day), a_day_remainder


def my_datetime(num_sec):
    get_calc_year, _ = calc_year(num_sec)
    get_calc_month, _ = calc_month(num_sec)
    get_calc_day, _ = calc_day(num_sec)

    current_month = epoc_month + get_calc_month
    current_day = epoc_day + get_calc_day
    current_year = epoc_year + get_calc_year
    return str(current_month).zfill(2) + '-' + str(current_day).zfill(
        2) + '-' + str(current_year)
