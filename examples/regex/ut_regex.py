import unittest
import sys

sys.path += '../../'
from examples.regex.regex import *

class TestRegEx(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_regex_char(self):
        regex = RegEx()
        regex.set_pattern('hello')

        matched, matched_string = regex.match('    hello, world')
        self.assertEqual(matched, True)
        self.assertEqual(matched_string, 'hello')

        matched, matched_string = regex.match('hi  yello, world')
        self.assertEqual(matched, False)


    def test_regex_class(self):
        regex = RegEx()
        regex.set_pattern('[a-zA-Z]ell[oO]')

        matched, matched_string = regex.match('hello, world')
        self.assertEqual(matched, True)
        self.assertEqual(matched_string, 'hello')

        matched, matched_string = regex.match('World, HellO')
        self.assertEqual(matched, True)
        self.assertEqual(matched_string, 'HellO')

        matched, matched_string = regex.match('yello, world')
        self.assertEqual(matched, True)
        self.assertEqual(matched_string, 'yello')


if __name__ == '__main__':
    unittest.main()
