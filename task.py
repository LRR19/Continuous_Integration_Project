import math

year = 31556926
month = year / 12
day = 86400
epoc_year = 1970
epoc_month = 1
epoc_day = 1
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
