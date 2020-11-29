import math

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
            # if adding another year with leap day doesn't overflow our
            # given seconds then we can add a new year and day
            if current_year_in_sec + year + day <= secs:
                current_year_in_sec += year + day
            else:
                break
        else:
            # if adding another year doesn't overflow our given seconds
            # then we can add a new year
            if current_year_in_sec + year <= secs:
                current_year_in_sec += year
            else:
                break

    return math.floor(current_year_in_sec / year)


def calc_month(secs) -> int:
    """Converts seconds to a month"""
    y = calc_year(secs)
    rem_secs = remain_secs_in_current_year(secs)
    calculated_month = 0
    if leap_yr(y + epoc_year):
        month_itr = 0
        while True:
            if month_itr > 11:
                month_itr = 0
            sec_in_month = LEAP_MONTH_DAYS[month_itr] * day
            if rem_secs - sec_in_month < 0:
                if abs(rem_secs - sec_in_month) <= day:  # midnight 12:00am
                    calculated_month += 1
                break
            else:
                rem_secs -= sec_in_month
                calculated_month += 1
                month_itr += 1
    else:
        month_itr = 0
        while True:
            if month_itr > 11:
                month_itr = 0
            sec_in_month = REG_MONTH_DAYS[month_itr] * day
            if rem_secs - sec_in_month < 0:
                break
            else:
                rem_secs -= sec_in_month
                calculated_month += 1
                month_itr += 1
    return calculated_month


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
        return calc_day_leap(m, rem_secs)
    else:
        return calc_day_comm(m, rem_secs)


def calc_day_leap(m, rem_secs) -> int:
    """Converts seconds to a day for a leap year"""
    counter = 0
    internal_counter = 0
    while counter <= m:
        if counter > 11 and internal_counter > 11:
            internal_counter = 0
        num_days = LEAP_MONTH_DAYS[internal_counter]
        total_sec_in_month = num_days * day
        if math.ceil((total_sec_in_month - rem_secs) / day) == \
                LEAP_MONTH_DAYS[internal_counter] - 1:
            return 0
        elif math.ceil((total_sec_in_month - rem_secs) / day) >= \
                LEAP_MONTH_DAYS[internal_counter]:
            return 0
        elif math.ceil((total_sec_in_month - rem_secs) / day) == 1:
            return 0
        elif rem_secs - total_sec_in_month < 0:
            if counter > 11:
                return math.ceil(rem_secs / day) + 1
            else:
                return math.floor(rem_secs / day) + 1
        else:
            rem_secs -= total_sec_in_month
            counter += 1
            internal_counter += 1


def calc_day_comm(m, rem_secs) -> int:
    """Converts seconds to a day for a regular year"""
    counter = 0
    internal_counter = 0
    while counter <= m:
        if counter > 11 and internal_counter > 11:
            internal_counter = 0
        num_days = REG_MONTH_DAYS[internal_counter]
        total_sec_in_month = num_days * day
        if rem_secs - total_sec_in_month < 0:
            return REG_MONTH_DAYS[internal_counter] - \
                   math.ceil((total_sec_in_month - rem_secs) / day)
        else:
            rem_secs -= total_sec_in_month
            counter += 1
            internal_counter += 1

def my_datetime(num_sec):
    get_calc_year = calc_year(num_sec)
    get_calc_month = calc_month(num_sec)
    get_calc_day = calc_day(num_sec)
    # Handles case when 12/32/2000 to be 01/nn/2001
    if get_calc_month + epoc_month == 12:
        if get_calc_day + epoc_day > REG_MONTH_DAYS[11]:
            get_calc_month = 0
            get_calc_day = get_calc_day - REG_MONTH_DAYS[11]
            get_calc_year += 1
    elif get_calc_month + epoc_month > 12:
        get_calc_year += 1
        get_calc_month = get_calc_month - 12

    current_month = epoc_month + get_calc_month
    current_day = epoc_day + get_calc_day
    current_year = epoc_year + get_calc_year
    return str(current_month).zfill(2) + '-' + str(current_day).zfill(
        2) + '-' + str(current_year)
