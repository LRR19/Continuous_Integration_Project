import math
from datetime import datetime

year = 31556926
month = year / 12
day = 86400
epoc_year = 1970
epoc_month = 1
epoc_day = 1
LEAP_MONTH_DAYS = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
REG_MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def leap_yr(lp_year):
    """Helper func: Returns true if it's a leap year and False if it's not"""
    return lp_year % 4 == 0 and (lp_year % 100 != 0 or lp_year % 400 == 0)


def calc_year(secs) -> int:
    """Converts seconds to a year"""
    current_year_in_sec = 0
    while True:
        if leap_yr(math.floor(current_year_in_sec / year) + epoc_year):
            if current_year_in_sec + year + day <= secs:
                current_year_in_sec += year + day
            else:
                break
        else:
            if current_year_in_sec + year <= secs:
                current_year_in_sec += year
            else:
                break

    # if leap_yr(math.floor(current_year_in_sec / year) + epoc_year):
    #     return math.floor(current_year_in_sec / (year + day))
    # else:
    return math.floor(current_year_in_sec / year)


def calc_month(secs) -> int:
    """Converts seconds to a month"""
    y = calc_year(secs)
    rem_secs = remain_secs_in_current_year(secs)
    m = 0
    if leap_yr(y + epoc_year):
        for v in LEAP_MONTH_DAYS:
            sec_in_month = v * day
            if rem_secs - sec_in_month < 0:
                if abs(rem_secs - sec_in_month) == day:  # midnight 12:00am
                    m += 1
                break
            else:
                rem_secs -= sec_in_month
                m += 1
    else:
        for v in REG_MONTH_DAYS:
            sec_in_month = v * day
            if rem_secs - sec_in_month < 0:
                if abs(rem_secs - sec_in_month) == day:  # midnight 12:00am
                    m += 1
                break
            else:
                rem_secs -= sec_in_month
                m += 1
    return m


def remain_secs_in_current_year(secs) -> int:
    i = calc_year(secs)
    leap_month_years = 0
    reg_month_years = 0
    while i > 0:
        if leap_yr(i + epoc_year):
            leap_month_years += 1
        else:
            reg_month_years += 1
        i -= 1

    rem = secs - (((reg_month_years * 365) + (leap_month_years * 366)) *
                  day)
    if rem < 0:
        rem = abs(rem)

    return rem


def calc_day(secs) -> int:
    """Converts seconds to a day"""
    m = calc_month(secs)
    rem_secs = remain_secs_in_current_year(secs)
    if leap_yr(calc_year(secs) + epoc_year):
        counter = 0
        while counter <= m:
            num_days = LEAP_MONTH_DAYS[counter]
            total_sec_in_month = num_days * day
            if rem_secs - total_sec_in_month < 0:
                if abs(rem_secs - total_sec_in_month) == day:  # midnight 12:00am
                    return 0
                elif abs(rem_secs - total_sec_in_month) == day + day:  # leap day @ midnight 12:00am
                    return math.floor(rem_secs / day) + 1
                return math.floor(rem_secs / day)
            else:
                rem_secs -= total_sec_in_month
                counter += 1
    else:
        counter = 0
        while counter <= m:
            num_days = REG_MONTH_DAYS[counter]
            total_sec_in_month = num_days * day
            if rem_secs - total_sec_in_month < 0:
                if abs(rem_secs - total_sec_in_month) == day:  # midnight 12:00am
                    return 0
                return math.floor(rem_secs / day)
            else:
                rem_secs -= total_sec_in_month
                counter += 1

    return math.floor(rem_secs / day)
    # rem_secs /= day
    # if 0 < rem_secs < 1:
    #     rem_secs = 1
    # else:
    #     rem_secs = math.floor(rem_secs)
    #
    # return rem_secs


def my_datetime(num_sec):
    get_calc_year = calc_year(num_sec)
    get_calc_month = calc_month(num_sec)
    get_calc_day = calc_day(num_sec)

    current_month = epoc_month + get_calc_month
    current_day = epoc_day + get_calc_day
    current_year = epoc_year + get_calc_year
    return str(current_month).zfill(2) + '-' + str(current_day).zfill(
        2) + '-' + str(current_year)


if __name__ == "__main__":
    # leap year 2188
    # print(f"My day: {my_datetime(6884312400)}")
    # print(datetime.utcfromtimestamp(6884312400).strftime('%m-%d-%Y'))

    # 03-01-2100
    print(f"My day: {my_datetime(4107567600)}")
    print(datetime.utcfromtimestamp(4107567600).strftime('%m-%d-%Y'))
    print(f"My day: {my_datetime(4107481200)}")
    print(datetime.utcfromtimestamp(4107481200).strftime('%m-%d-%Y'))
