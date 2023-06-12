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

        matched = regex.match('    hello, world')
        self.assertEqual(len(matched), 1)
        self.assertEqual(matched[0], 'hello')

        matched = regex.match('hi  yello, world')
        self.assertEqual(len(matched), 0)


    def test_regex_class(self):
        regex = RegEx()
        regex.set_pattern('[a-zA-Z]ell[oO]')

        matched = regex.match('hello, world')
        self.assertEqual(len(matched), 1)
        self.assertEqual(matched[0], 'hello')

        matched = regex.match('World, HellO')
        self.assertEqual(len(matched), 1)
        self.assertEqual(matched[0], 'HellO')

        matched = regex.match('yello, world')
        self.assertEqual(len(matched), 1)
        self.assertEqual(matched[0], 'yello')

    def test_regex_count(self):
        regex = RegEx()
        regex.set_pattern('[a-zA-Z][a-zA-Z0-9]+')

        self.assertEqual(regex.pattern.child.type, Pattern.RANGE)
        self.assertEqual(regex.pattern.child.next.type, Pattern.RANGE)

        matched = regex.match('    f32Value;    1234;    abcd')
        self.assertEqual(len(matched), 2)
        self.assertEqual(matched[0], 'f32Value')
        self.assertEqual(matched[1], 'abcd')

        regex.set_pattern('[0-9]*[.]?[0-9]+')
        matched = regex.match('3.141592, 12345')
        self.assertEqual(len(matched), 2)
        self.assertEqual(matched[0], '3.141592')
        self.assertEqual(matched[1], '12345')

        regex.set_pattern('ab?c+d*')
        matched = regex.match('acccd, abcddddd')
        self.assertEqual(len(matched), 2)
        self.assertEqual(matched[0], 'acccd')
        self.assertEqual(matched[1], 'abcddddd')


        # TODO: To handle [+-]
        # TODO: To implement group and OR operator.
        # TODO: To optimize

if __name__ == '__main__':
    unittest.main()
