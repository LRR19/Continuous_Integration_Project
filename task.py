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


def calc_year2(secs) -> int:
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


def calc_year(secs) -> int:
    """Converts seconds to a year"""
    current_year_in_sec = 0
    while True:
        if current_year_in_sec + year <= secs:
            current_year_in_sec += year
        else:
            break

    return math.floor(current_year_in_sec / year)


def calc_month(secs) -> int:
    """Converts seconds to a month"""
    y = calc_year2(secs)
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
    i = calc_year2(secs)
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
    if leap_yr(calc_year2(secs) + epoc_year):
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
    else:
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

    return math.floor(rem_secs / day)


def my_datetime(num_sec):
    get_calc_year = calc_year2(num_sec)
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


if __name__ == "__main__":
    # print(f"My day: {my_datetime(131634486250)}")
    # print(datetime.utcfromtimestamp(131634486250).strftime('%m-%d-%Y'))
    #
    #
    # print(f"My day: {my_datetime(54351580109)}")
    # print(datetime.utcfromtimestamp(54351580109).strftime('%m-%d-%Y'))
    # print(f"My day: {my_datetime(109904972918)}")
    # print(datetime.utcfromtimestamp(109904972918).strftime('%m-%d-%Y'))
    #
    # print(f"My day: {my_datetime(14642439067)}")
    # print(datetime.utcfromtimestamp(14642439067).strftime('%m-%d-%Y'))
    # print(f"My day: {my_datetime(15557568132)}")
    # print(datetime.utcfromtimestamp(15557568132).strftime('%m-%d-%Y'))
    # print(f"My day: {my_datetime(136925670091)}")
    # print(datetime.utcfromtimestamp(136925670091).strftime('%m-%d-%Y'))
    #
    #
    # print(f"My day: {my_datetime(21521869118)}")
    # print(datetime.utcfromtimestamp(21521869118).strftime('%m-%d-%Y'))
    # print(f"My day: {my_datetime(138884725212)}")
    # print(datetime.utcfromtimestamp(138884725212).strftime('%m-%d-%Y'))
    # print(f"My day: {my_datetime(171519770657)}")
    # print(datetime.utcfromtimestamp(171519770657).strftime('%m-%d-%Y'))
    # print(f"My day: {my_datetime(114817389093)}")
    # print(datetime.utcfromtimestamp(114817389093).strftime('%m-%d-%Y'))
    # print(f"My day: {my_datetime(163943502679)}")
    # print(datetime.utcfromtimestamp(163943502679).strftime('%m-%d-%Y'))
    # print(f"My day: {my_datetime(148287045670)}")
    # print(datetime.utcfromtimestamp(148287045670).strftime('%m-%d-%Y'))
    print(f"My day: {my_datetime(233716089025)}")
    print(datetime.utcfromtimestamp(233716089025).strftime('%m-%d-%Y'))
    # print(f"My: {my_datetime(234951368048)}")
    # print(datetime.utcfromtimestamp(234951368048).strftime('%m-%d-%Y'))
    # print(f"My: {my_datetime(123176718521)}")
    # print(datetime.utcfromtimestamp(123176718521).strftime('%m-%d-%Y'))
    #
    #
    # # leap year 2188
    # print(f"My day: {my_datetime(6884312400)}")
    # print(datetime.utcfromtimestamp(6884312400).strftime('%m-%d-%Y'))
    #
    # # 03-01-2100
    # print(f"My day: {my_datetime(4107567600)}")
    # print(datetime.utcfromtimestamp(4107567600).strftime('%m-%d-%Y'))
    # print(f"My day: {my_datetime(4107481200)}")
    # print(datetime.utcfromtimestamp(4107481200).strftime('%m-%d-%Y'))
