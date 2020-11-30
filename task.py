import math

YEAR = 31556926
MONTH = YEAR / 12
DAY = 86400
EPOCH_YEAR = 1970
EPOCH_MONTH = 1
EPOCH_DAY = 1
LEAP_MONTH_DAYS = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
REG_MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

valid_hex_num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                 'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f']


# PART 1: Convert Hex to Decimal
def conv_num(num_str):
    hex_to_int = 0
    pwr = 0
    if invalid_hex_string(num_str):
        return None
    if num_str.startswith('.') or num_str.endswith('.'):
        return format_float(num_str)
    if pos_hex_num(num_str) is False and neg_hex_num(num_str) is False:
        return num_str
    # For loop to determine value of hex
    for digit in reversed(num_str):
        if valid_hex_digit(digit):
            hex_to_int += convert_lower(digit) * 16 ** pwr
            pwr += 1
        if digit == 'x' or digit == '-':
            continue
        if not valid_hex_digit(digit):
            return None
    if neg_hex_num(num_str):
        return hex_to_int * -1
    return hex_to_int


# Helper function to validate hex string
def invalid_hex_string(hex_str):
    if count_period(hex_str) > 1 or hex_str == '':
        return True
    if pos_hex_num(hex_str) is False and neg_hex_num(hex_str) is False:
        for hex_digit in hex_str:
            if valid_hex_digit(hex_digit):
                if valid_hex_num.index(hex_digit) > 9:
                    return True
    count_x = 0
    count_neg = 0
    for digit in hex_str:
        if digit == 'x':
            count_x += 1
        if digit == '-':
            count_neg += 1
    if count_x > 1 or count_neg > 1:
        return True
    return False


# Helper function that returns the number of periods in given string
def count_period(hex_str):
    count = 0
    for char in hex_str:
        if char == '.':
            count += 1
    return count


# Helper function that checks for valid hex number
def valid_hex_digit(hex_digit):
    if hex_digit in valid_hex_num:
        return True
    return False


# Helper function that returns true if hex value is positive
def pos_hex_num(hex_str):
    if hex_str.startswith('0x'):
        return True
    return False


# Helper function returns true if negative hex value
def neg_hex_num(hex_str):
    if hex_str.startswith('-0x'):
        return True
    return False


# Helper function that inserts missing 0 next to period
def format_float(hex_str):
    if hex_str.startswith('.'):
        return '0' + hex_str
    elif hex_str.endswith('.'):
        return hex_str + '0'
    return hex_str


# Helper function that converts lowercase hex digit to correct value
def convert_lower(hex_num):
    hex_index = valid_hex_num.index(hex_num)
    if hex_index > 15:
        return hex_index - 6
    return hex_index


# PART 2: Datetime
def leap_yr(lp_year):
    """Helper func: Returns true if it's a leap YEAR and False if it's not"""
    return lp_year % 4 == 0 and (lp_year % 100 != 0 or lp_year % 400 == 0)


def calc_year(secs) -> int:
    """Helper func: Calculates the YEAR given the seconds"""
    current_year_in_sec = 0
    while True:
        if leap_yr(math.floor(current_year_in_sec / YEAR) + EPOCH_YEAR):
            # if adding another YEAR with leap DAY doesn't overflow our
            # given seconds then we can add a new YEAR and DAY
            if current_year_in_sec + YEAR + DAY <= secs:
                current_year_in_sec += YEAR + DAY
            else:
                break
        else:
            # if adding another YEAR doesn't overflow our given seconds
            # then we can add a new YEAR
            if current_year_in_sec + YEAR <= secs:
                current_year_in_sec += YEAR
            else:
                break

    return math.floor(current_year_in_sec / YEAR)


def calc_month(secs) -> int:
    """Helper func: Calculates MONTH of the year given the remaining seconds"""
    y = calc_year(secs)
    rem_secs = remain_secs_in_current_year(secs)
    calculated_month = 0
    # if a leap year, iterate through the list of LEAP_MONTHS_DAYS to
    # calculate the days in a month. If there is an overflow of days
    # within a month, it means you go to the next month. If it's not a leap
    # year then repeat same process using REG_MONTHS_DAYS.
    if leap_yr(y + EPOCH_YEAR):
        month_itr = 0
        while True:
            if month_itr > 11:
                month_itr = 0
            sec_in_month = LEAP_MONTH_DAYS[month_itr] * DAY
            if rem_secs - sec_in_month < 0:
                if abs(rem_secs - sec_in_month) <= DAY:  # midnight 12:00am
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
            sec_in_month = REG_MONTH_DAYS[month_itr] * DAY
            if rem_secs - sec_in_month < 0:
                break
            else:
                rem_secs -= sec_in_month
                calculated_month += 1
                month_itr += 1
    return calculated_month


def remain_secs_in_current_year(secs) -> int:
    """Helper func: Calculates the remaining seconds from given year"""
    i = calc_year(secs)
    leap_month_years = 0
    reg_month_years = 0
    # Calculates the remaining seconds(seconds that are left over after the
    # year has been calculated) for a leap and regular year.
    while i > 0:
        if leap_yr(i + EPOCH_YEAR):
            leap_month_years += 1
        else:
            reg_month_years += 1
        i -= 1

    rem = secs - (((reg_month_years * 365) + (leap_month_years * 366)) *
                  DAY)
    if rem < 0:
        rem = abs(rem)

    return rem


def calc_day(secs) -> int:
    """Helper func: Calculates the day given the MONTH for a leap and
       regular year"""
    m = calc_month(secs)
    rem_secs = remain_secs_in_current_year(secs)
    if leap_yr(calc_year(secs) + EPOCH_YEAR):
        return calc_day_leap(m, rem_secs)
    else:
        return calc_day_comm(m, rem_secs)


def calc_day_leap(m, rem_secs) -> int:
    """Helper func: Determines the DAY of the MONTH in a leap year"""
    counter = 0
    internal_counter = 0
    while counter <= m:
        if counter > 11 and internal_counter > 11:
            internal_counter = 0
        num_days = LEAP_MONTH_DAYS[internal_counter]
        total_sec_in_month = num_days * DAY
        if math.ceil((total_sec_in_month - rem_secs) / DAY) == \
                LEAP_MONTH_DAYS[internal_counter] - 1:
            return 0
        elif math.ceil((total_sec_in_month - rem_secs) / DAY) >= \
                LEAP_MONTH_DAYS[internal_counter]:
            return 0
        elif math.ceil((total_sec_in_month - rem_secs) / DAY) == 1:
            return 0
        elif rem_secs - total_sec_in_month < 0:
            if counter > 11:
                return math.ceil(rem_secs / DAY) + 1
            else:
                return math.floor(rem_secs / DAY) + 1
        else:
            rem_secs -= total_sec_in_month
            counter += 1
            internal_counter += 1


def calc_day_comm(m, rem_secs) -> int:
    """Helper func: Determines the DAY of the MONTH in a regular year"""
    counter = 0
    internal_counter = 0
    while counter <= m:
        if counter > 11 and internal_counter > 11:
            internal_counter = 0
        num_days = REG_MONTH_DAYS[internal_counter]
        total_sec_in_month = num_days * DAY
        if rem_secs - total_sec_in_month < 0:
            return REG_MONTH_DAYS[internal_counter] - \
                   math.ceil((total_sec_in_month - rem_secs) / DAY)
        else:
            rem_secs -= total_sec_in_month
            counter += 1
            internal_counter += 1


def my_datetime(num_sec):
    """ Main function that utilizes above helpers to convert seconds in
    MM-DD-YYYY"""
    get_calc_year = calc_year(num_sec)
    get_calc_month = calc_month(num_sec)
    get_calc_day = calc_day(num_sec)

    # Handles case when 12/32/2000 to be 01/nn/2001
    if get_calc_month + EPOCH_MONTH == 12:
        if get_calc_day + EPOCH_DAY > REG_MONTH_DAYS[11]:
            get_calc_month = 0
            get_calc_day = get_calc_day - REG_MONTH_DAYS[11]
            get_calc_year += 1
    elif get_calc_month + EPOCH_MONTH > 12:
        get_calc_year += 1
        get_calc_month = get_calc_month - 12

    current_month = EPOCH_MONTH + get_calc_month
    current_day = EPOCH_DAY + get_calc_day
    current_year = EPOCH_YEAR + get_calc_year

    return str(current_month).zfill(2) + '-' + str(current_day).zfill(
        2) + '-' + str(current_year)


# PART 3: This part of task.py converts int to hex string
# Core helper function that converts int to big endian hex
def int_to_hex(num):
    hex_string = '0123456789ABCDEF'
    converted = ''
    number = num
    remainder = -1
    count = 0

    while number >= 0:
        remainder = number % 16
        number = number // 16
        count += 1

        if number == 0:
            if count % 2 == 1:
                return '0' + hex_string[remainder] + converted
            return hex_string[remainder] + converted
        else:
            converted = hex_string[remainder] + converted


# Helper function that converts big endian to little endian
def little_endian(hex_string):
    length = len(hex_string)
    converted = [''] * length
    half = len(hex_string) // 2
    if half % 2 == 1:
        half -= 1
        converted[half] = hex_string[half]
        converted[half + 1] = hex_string[half + 1]

    for i in range(0, half, 2):
        converted[i] = hex_string[length - i - 2]
        converted[i + 1] = hex_string[length - i - 1]
        converted[length - i - 2] = hex_string[i]
        converted[length - i - 1] = hex_string[i + 1]

    return "".join(converted)


# Helper function that formats the hex to be separated by space per byte
def format_hex(hex_string):
    formatted = hex_string
    j = iter(formatted)
    return ' '.join(i + k for i, k in zip(j, j))


# Main function that utilizes above helpers, adds negative if num is negative
def conv_endian(num, endian='big'):
    abs_num = abs(num)
    to_hex = int_to_hex(abs_num)
    if endian == 'little':
        to_hex = little_endian(to_hex)
    elif endian != 'big' and endian != 'little':
        return None

    to_hex = format_hex(to_hex)

    if num < 0:
        return "-" + to_hex
    else:
        return to_hex
