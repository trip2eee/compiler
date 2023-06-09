import unittest
from src.grammar_parser import *

class GarmmarFileParserTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _test_rule(self, parser:GarmmarParser, left, strings, actions):
        rule: Rule
        rule = parser.rules[left]

        self.assertEqual(rule.left_symbol, left)
        
        self.assertEqual(len(rule.strings), len(rule.reduce_actions))

        for idx_string in range(len(strings)):
            for idx_token in range(len(strings[idx_string])):
                self.assertEqual(rule.strings[idx_string][idx_token], strings[idx_string][idx_token])
            self.assertEqual(rule.reduce_actions[idx_string], actions[idx_string])

    def _test_embedded_action(self, parser:GarmmarParser, symbol, action):
        self.assertEqual(parser.embedded_action[symbol], action)

    def test_grammar_file(self):
        parser = GarmmarParser()
        parser.open('unittest/test_grammar_parser.gram')
        
        print('Rules')
        for key in parser.rules:
            rule = parser.rules[key]
            print(str(rule))
        
        print('Embedded actions')
        for key in parser.embedded_action:
            print('{} -> {}\n'.format(key, parser.embedded_action[key]))

        symbols = ['decl','type', 'var_list', 'int', 'float', ',', 'id']
        self.assertEqual(len(parser.symbols), len(symbols))
        for i in range(len(symbols)):
            self.assertEqual(symbols[i], parser.symbols[i])

        self.assertEqual(len(parser.rules), 3)
        
        self._test_rule(parser, 'decl', [['type', 'var_list']], [''])
        self._test_rule(parser, 'type', [['int'], ['float']], ['', ''])
        self._test_rule(parser, 'var_list', [['var_list', ',', 'id'], ['id']], [' print("1") ', ' print("2") '])

        self._test_embedded_action(parser, 'type', ' cur_type = $1 ')

        print('done')

if __name__ == '__main__':
    unittest.main()

