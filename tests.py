import unittest
import random
from _datetime import datetime
from task import leap_yr, my_datetime


class TestCase(unittest.TestCase):

    """Unit tests for function 2 - def my_datetime(num_sec)"""
    def test_leap_yr_func(self):
        self.assertTrue(leap_yr(2000))

    def test_yr_zero(self):
        self.assertEqual(my_datetime(0), "01-01-1970")

    def test_secs1(self):
        self.assertTrue(my_datetime(1606186302))

    def test_random(self):
        for i in range(0, 1000):
            num_secs = random.randint(0, 315537963048)
            self.assertEqual(my_datetime(num_secs),
                             datetime.utcfromtimestamp(num_secs).
                             strftime('%m-%d-%Y'))


if __name__ == '__main__':
    unittest.main()
