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


        regex.set_pattern('[a-zA-Z-]ell[oO]')
        matched = regex.match('-ellO, world')
        self.assertEqual(len(matched), 1)
        self.assertEqual(matched[0], '-ellO')

    def test_regex_count(self):
        regex = RegEx()

        regex.set_pattern('[a-zA-Z][a-zA-Z0-9]+')

        self.assertEqual(regex.pattern.childs[0].type, PatternType.RANGE)
        self.assertEqual(regex.pattern.childs[0].next.type, PatternType.RANGE)

        matched = regex.match('    f32Value;    1234;    abcd')
        self.assertEqual(len(matched), 2)
        self.assertEqual(matched[0], 'f32Value')
        self.assertEqual(matched[1], 'abcd')

        regex.set_pattern('[0-9]+[.]?[0-9]*')
        matched = regex.match('3.141592, 12345')
        self.assertEqual(len(matched), 2)
        self.assertEqual(matched[0], '3.141592')
        self.assertEqual(matched[1], '12345')

        regex.set_pattern('ab?c+d*')
        matched = regex.match('acccd, abcddddd')
        self.assertEqual(len(matched), 2)
        self.assertEqual(matched[0], 'acccd')
        self.assertEqual(matched[1], 'abcddddd')    

    def test_regex_group(self):

        regex = RegEx()
        # + : >= 1
        # * : >= 0
        # ? : 0 or 1
        regex.set_pattern('\d+([.]\d*)?')
        matched = regex.match('-10. 10.321  -.123, +3.141592F')
        print(matched)
        self.assertEqual(len(matched), 4)
        self.assertEqual(matched[0], '10.')
        self.assertEqual(matched[1], '10.321')
        self.assertEqual(matched[2], '123')
        self.assertEqual(matched[3], '3.141592')

        regex.set_pattern('[+-]?((\d+([.]\d{0,10})?)|([.]\d{1,10}))[fF]{0,1}')
        matched = regex.match('-10. 10.321  -.123, +3.141592F')
        print(matched)

        self.assertEqual(len(matched), 4)
        self.assertEqual(matched[0], '-10.')
        self.assertEqual(matched[1], '10.321')
        self.assertEqual(matched[2], '-.123')
        self.assertEqual(matched[3], '+3.141592F')

    def test_regex_group2(self):
        regex = RegEx()
        regex.set_pattern('W{1}o(r|R|k)l*d')
        matched = regex.match('Hello, World, Hello WoRld, Hello Word, Wokd')

        self.assertEqual(len(matched), 4)
        self.assertEqual(matched[0], 'World')
        self.assertEqual(matched[1], 'WoRld')
        self.assertEqual(matched[2], 'Word')
        self.assertEqual(matched[3], 'Wokd')

    def test_cpp_comment(self):
        regex = RegEx()
        # regex.set_pattern('(\/\*(.|\n)*\*\/)|(\/\/(.)*\n)')
        regex.set_pattern('\/(\*(.|\n)*\*\/)|(\/.*\n)')

        code = ''
        code += "#include <stdio.h>\n   "
        code += "/* This is a C style Comment\n *with a line change. Currently searching this pattern is not efficient. **/\n"
        code += " // This is C++ style comment\n"
        code += " /* comment2 */\n"

        print(code)
        matched = regex.match(code)
        print(matched)

        self.assertEqual(len(matched), 3)
        self.assertEqual(matched[0], '/* This is a C style Comment\n *with a line change. Currently searching this pattern is not efficient. **/')
        self.assertEqual(matched[1], '// This is C++ style comment\n')
        self.assertEqual(matched[2], '/* comment2 */')
        
        # TODO: To optimize regex match()

if __name__ == '__main__':
    unittest.main()
