import unittest
import sys

sys.path += '../../'
from examples.regex.regex import *

class TestRegExDFA(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_id(self):
        
        regex = RegEx()
        
        regex.compile('[_a-zA-Z][_a-zA-Z0-9]*')
        code = '    f32Value;    1234;    abcd'

        list_matched = regex.match_dfa(code)

        for s in list_matched:
            print(s)

        self.assertEqual(list_matched[0], 'f32Value')
        self.assertEqual(list_matched[1], 'abcd')

    def test_number(self):
        
        regex = RegEx()
        
        regex.compile('[+-]?((\d+([.]\d{0,10})?)|([.]\d{1,10}))[fF]{0,1}')
        code = '-10. 10.321  -.123, +3.141592F, +1.234f -.321F'

        list_matched = regex.match_dfa(code)

        for s in list_matched:
            print(s)

        self.assertEqual(list_matched[0], '-10.')
        self.assertEqual(list_matched[1], '10.321')
        self.assertEqual(list_matched[2], '-.123')
        self.assertEqual(list_matched[3], '+3.141592F')
        self.assertEqual(list_matched[4], '+1.234f')
        self.assertEqual(list_matched[5], '-.321F')

    def test_number2(self):
        
        regex = RegEx()
        
        regex.compile('((\d+([.]\d{0,10})?)|([.]\d{1,10}))[fF]{0,1}')
        code = '-10. 10.321  -.123, +3.141592F, +1.234f -.321F'

        list_matched = regex.match_dfa(code)

        for s in list_matched:
            print(s)

        self.assertEqual(list_matched[0], '10.')
        self.assertEqual(list_matched[1], '10.321')
        self.assertEqual(list_matched[2], '.123')
        self.assertEqual(list_matched[3], '3.141592F')
        self.assertEqual(list_matched[4], '1.234f')
        self.assertEqual(list_matched[5], '.321F')

    def test_or(self):

        regex = RegEx()

        regex.compile('W{1}o(r|R|k)l*d')
        code = 'Hello, World, Hello WoRld, Hello Word, Wokd'

        list_matched = regex.match_dfa(code)

        for s in list_matched:
            print(s)

        self.assertEqual(list_matched[0], 'World')
        self.assertEqual(list_matched[1], 'WoRld')
        self.assertEqual(list_matched[2], 'Word')
        self.assertEqual(list_matched[3], 'Wokd')

    def test_cpp_comment(self):
        
        regex = RegEx()
        
        regex.compile('\/(\*(.|\n)*\*\/)|(\/.*\n)')
        code = ''
        code += "#include <stdio.h>\n   "
        code += "/* This is a C style Comment\n *with a line change. Currently searching this pattern is not efficient. **/\n"
        code += " // This is C++ style comment\n"
        code += " /* comment2 */\n"
        code += " /***/\n"

        list_matched = regex.match_dfa(code)

        for s in list_matched:
            print(s)

        self.assertEqual(list_matched[0], '/* This is a C style Comment\n *with a line change. Currently searching this pattern is not efficient. **/')
        self.assertEqual(list_matched[1], '// This is C++ style comment\n')
        self.assertEqual(list_matched[2], '/* comment2 */')
        self.assertEqual(list_matched[3], '/***/')


if __name__ == '__main__':
    unittest.main()
