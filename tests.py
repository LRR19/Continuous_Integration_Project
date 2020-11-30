import unittest
import random
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

    def test_random_big(self):
        for x in range(0, 1000):
            random_int = random.randint(0, 999999)
            formatted = hex(random_int)[2:]
            if len(formatted)%2 == 1:
                formatted = "0" + formatted
            j = iter(formatted)
            formatted = ' '.join(i + k for i, k in zip(j, j)).upper()
            self.assertEqual(conv_endian(random_int, 'big'), formatted)

    def test_random_little(self):
        for x in range(0, 1000):
            random_int = random.randint(0, 999999)
            formatted = hex(random_int)[2:]
            if len(formatted)%2 == 1:
                formatted = "0" + formatted
            j = iter(formatted)
            formatted = ' '.join(i + k for i, k in zip(j, j))

            # little endian source https://www.xspdf.com/resolution/52873369.html
            t = bytearray.fromhex(formatted)
            t.reverse()
            little_formatted = ' '.join(format(x, '02x') for x in t).upper()
            self.assertEqual(conv_endian(random_int, 'little'), little_formatted)


if __name__ == '__main__':
    unittest.main()
