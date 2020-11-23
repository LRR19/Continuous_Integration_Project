import unittest
from task import leap_yr


class TestCase(unittest.TestCase):

    """Unit tests for function 2 - def my_datetime(num_sec)"""
    def test_leap_yr_func(self):
        self.assertTrue(leap_yr(2000))


if __name__ == '__main__':
    unittest.main()
