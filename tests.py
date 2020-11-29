import unittest
from datetime import datetime
from task import leap_yr, my_datetime
from task import conv_endian
from task import count_period, valid_hex_digit, pos_hex_num
from task import neg_hex_num, conv_num, format_float, invalid_hex_string


class TestCase(unittest.TestCase):
    """Unit tests for function 2 - def my_datetime(num_sec)"""

    def test_leap_yr_func(self):
        self.assertTrue(leap_yr(2000))

    # year 11,969
    def test_secs(self):
        self.assertTrue(my_datetime(315537963048))

    def test_epoch0(self):
        self.assertEqual("01-01-1970", my_datetime(0))

    def test_epoch1(self):
        self.assertEqual("01-01-1970", my_datetime(86399))

    def test1(self):
        self.assertEqual("11-29-1973", my_datetime(123456789))

    def test2(self):
        self.assertEqual("12-22-2282", my_datetime(9876543210))

    # 09-26-1988 @ 12:00:00 am
    def test3(self):
        self.assertEqual(
            datetime.utcfromtimestamp(591235200).strftime('%m-%d-%Y'),
            my_datetime(591235200))

    # 07-01-2707. Beginning of the month
    def test4(self):
        self.assertEqual(
            datetime.utcfromtimestamp(23273096400).strftime('%m-%d-%Y'),
            my_datetime(23273096400))

    # 07-31-2185. End of the month
    def test5(self):
        self.assertEqual(
            datetime.utcfromtimestamp(6803096400).strftime('%m-%d-%Y'),
            my_datetime(6803096400))

    # 01-01-3131. Beginning of the year
    def test6(self):
        self.assertEqual(
            datetime.utcfromtimestamp(36637621200).strftime('%m-%d-%Y'),
            my_datetime(36637621200))

    # 12-31-9999. End of the year
    def test7(self):
        self.assertEqual(
            datetime.utcfromtimestamp(253402261200).strftime('%m-%d-%Y'),
            my_datetime(253402261200))

    # 01-01-2201. Beginning of a non-leap year
    def test8(self):
        self.assertEqual(
            datetime.utcfromtimestamp(7289738124).strftime('%m-%d-%Y'),
            my_datetime(7289738124))

    # 11-30-2007
    def test9(self):
        self.assertEqual(
            datetime.utcfromtimestamp(1196402400).strftime('%m-%d-%Y'),
            my_datetime(1196402400))

    # 12-22-6065 @ 11:59:59 pm
    def test10(self):
        self.assertEqual(
            datetime.utcfromtimestamp(129256559999).strftime('%m-%d-%Y'),
            my_datetime(129256559999))

    # 12-31-8573 @ 12:00:00 am
    def test11(self):
        self.assertEqual(
            datetime.utcfromtimestamp(208402070400).strftime('%m-%d-%Y'),
            my_datetime(208402070400))

    # LEAP: 02-29-1972
    def test12(self):
        self.assertEqual(
            datetime.utcfromtimestamp(68169600).strftime('%m-%d-%Y'),
            my_datetime(68169600))

    # LEAP: 02-29-1972 @ 11:59:59 pm
    def test13(self):
        self.assertEqual(datetime.utcfromtimestamp(68255999).strftime(
            '%m-%d-%Y'), my_datetime(68255999))

    # LEAP: 02-29-2024 @ 12:00:00 am
    def test14(self):
        self.assertEqual(datetime.utcfromtimestamp(1709164800).strftime(
            '%m-%d-%Y'), my_datetime(1709164800))

    # LEAP: 03-01-2020. Beginning of the month after Feb (leap)
    def test15(self):
        self.assertEqual(datetime.utcfromtimestamp(1583042400).strftime(
            '%m-%d-%Y'), my_datetime(1583042400))

    # Unit Tests for Function 3
    def test_big(self):
        self.assertEqual(conv_endian(954786), "0E 91 A2")

    def test_big_negative(self):
        self.assertEqual(conv_endian(-954786), "-0E 91 A2")

    def test_little(self):
        self.assertEqual(conv_endian(954786, 'little'), "A2 91 0E")

    def test_little_negative(self):
        self.assertEqual(conv_endian(-954786, 'little'), "-A2 91 0E")

    def test_bad_endian(self):
        self.assertEqual(conv_endian(-954786, 'bad'), None)

    # Unit tests for Function 1
    def test_count_period(self):
        self.assertEqual(count_period('abc....def'), 4)

    def test_valid_hex_digit(self):
        self.assertTrue(valid_hex_digit('a'))

    def test_pos_hex_num(self):
        self.assertTrue(pos_hex_num('0xA'))

    def test_neg_hex_num(self):
        self.assertTrue(neg_hex_num('-0xA'))

    def test_conv_num(self):
        self.assertEqual(conv_num('0x1a'), 26)

    def test_format_float(self):
        self.assertEqual(format_float('.123'), '0.123')

    def test_invalid_hex_string(self):
        self.assertEqual(invalid_hex_string('12345A'), True)


if __name__ == '__main__':
    unittest.main()
