import unittest
from task import leap_yr, my_datetime
from task import conv_endian
from task import count_period, valid_hex_digit, pos_hex_num, neg_hex_num


class TestCase(unittest.TestCase):

    """Unit tests for function 2 - def my_datetime(num_sec)"""
    def test_leap_yr_func(self):
        self.assertTrue(leap_yr(2000))

    def test_yr_zero(self):
        self.assertEqual(my_datetime(0), "01-01-1970")

    # Testing 9999 years: 11,969
    def test_secs1(self):
        self.assertTrue(my_datetime(315537963048))

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
        self.assertTrue(valid_hex_digit(1))

    def test_pos_hex_num(self):
        self.assertTrue(pos_hex_num('0xA'))

    def test_neg_hex_num(self):
        self.assertTrue(neg_hex_num('-0xA'))

if __name__ == '__main__':
    unittest.main()
