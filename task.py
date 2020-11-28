import math

hour = 3600
day = 86400
week = 604800
month = 2629743
year = 31556926
epoc_year = 1970
epoc_month = 1
epoc_day = 1

valid_hex_num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                 'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f']


# Part 1
# Convert Hex to Decimal
def conv_num(num_str):
    hex_to_int = 0
    pwr = 0

    # Returns none if empty string or there is more than 1 period
    if count_period(num_str) > 1 or num_str == '':
        return None

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

    if pos_hex_num(num_str) is False and neg_hex_num(num_str) is False:
        return format_float(num_str)

    return None


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


def convert_lower(hex_num):
    hex_index = valid_hex_num.index(hex_num)
    if hex_index > 15:
        return hex_index - 6
    return hex_index


# ------------------------------------


def leap_yr(lp_year):
    """Helper func: Returns true if it's a leap year and False if it's not"""
    return lp_year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


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
