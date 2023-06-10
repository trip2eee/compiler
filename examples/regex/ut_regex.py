import unittest
import sys

sys.path += '../../'
from examples.regex.regex import *

class TestRegEx(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_regex1(self):
        regex = RegEx()
        regex.set_pattern('hello')

        matched, matched_string = regex.match('    hello, world')
        self.assertEqual(matched, True)
        self.assertEqual(matched_string, 'hello')

        matched, matched_string = regex.match('hi  yello, world')
        self.assertEqual(matched, False)


    def test_regex2(self):
        regex = RegEx()
        regex.set_pattern('[a-z]orld')

        matched, matched_string = regex.match('hello, world')
        self.assertEqual(matched, True)
        self.assertEqual(matched_string, 'world')

        matched, matched_string = regex.match('hello, corld')
        self.assertEqual(matched, True)
        self.assertEqual(matched_string, 'corld')


if __name__ == '__main__':
    unittest.main()
