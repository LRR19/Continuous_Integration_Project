import unittest
from task import leap_yr, my_datetime
from task import conv_endian


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


if __name__ == '__main__':
    unittest.main()
