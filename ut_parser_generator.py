import unittest
from src.parser_generator import *

class ParserGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.idx_token = 0

    def tearDown(self):
        pass
    
    def _compare_set(self, a, b):
        self.assertEqual(len(a), len(b))
        for i in range(len(a)):
            self.assertTrue(a[i] in b)

    def test_open(self):
        gen = ParserGenerator()
        gen.open('unittest/test1.gram')
        gen.print_nonterminals()
        gen.print_terminals()        

        symbols = ['S', 'C', 'D', 'a', 'b', 'c', 'd']
        
        self.assertEqual(len(gen.symbols), len(symbols))
        for i in range(len(symbols)):
            self.assertEqual(gen.symbols[i], symbols[i])

    def test_first(self):
        print('test_first')
        gen = ParserGenerator()
        gen.open('unittest/test_first_follow1.gram')
        gen.print_first_follow()

        t = ['(', 'id']
        self._compare_set(gen.rules['E'].first, t)
        
        t = ['+', 'ep']
        self._compare_set(gen.rules['Ep'].first, t)

        t = ['(', 'id']
        self._compare_set(gen.rules['T'].first, t)

        t = ['*', 'ep']
        self._compare_set(gen.rules['Tp'].first, t)

        t = ['(', 'id']
        self._compare_set(gen.rules['F'].first, t)

    def test_follow(self):
        print('test_follow')
        gen = ParserGenerator()
        gen.open('unittest/test_first_follow1.gram')
        gen.print_first_follow()

        t = ['$', ')']
        self._compare_set(gen.rules['E'].follow, t)
        
        t = ['$', ')']
        self._compare_set(gen.rules['Ep'].follow, t)

        t = ['$', ')', '+']
        self._compare_set(gen.rules['T'].follow, t)

        t = ['$', ')', '+']
        self._compare_set(gen.rules['Tp'].follow, t)

        t = ['$', ')', '+', '*']
        self._compare_set(gen.rules['F'].follow, t)

    def test_first_follow(self):
        print('test_first_follow')
        gen = ParserGenerator()
        gen.open('unittest/test_first_follow2.gram')
        gen.print_first_follow()

        # Check first set
        t = ['(', 'number']
        self._compare_set(gen.rules['exp'].first, t)
        
        t = ['+', '-']
        self._compare_set(gen.rules['addop'].first, t)

        t = ['(', 'number']
        self._compare_set(gen.rules['term'].first, t)

        t = ['*']
        self._compare_set(gen.rules['mulop'].first, t)

        t = ['(', 'number']
        self._compare_set(gen.rules['factor'].first, t)

        # Check follow set
        t = ['$', '+', '-', ')']
        self._compare_set(gen.rules['exp'].follow, t)
        
        t = ['(', 'number']
        self._compare_set(gen.rules['addop'].follow, t)

        t = ['$', '+', '-', '*', ')']
        self._compare_set(gen.rules['term'].follow, t)

        t = ['(', 'number']
        self._compare_set(gen.rules['mulop'].follow, t)

        t = ['$', '+', '-', '*', ')']
        self._compare_set(gen.rules['factor'].follow, t)
    
    def test_LR0_items(self):
        print('test LR(0) items')

        gen = ParserGenerator()
        gen.open('unittest/test_LR0_items.gram')
        gen.compute_LR0_items()
        
        self.assertEqual(len(gen.states), 12)

    def check_parsing_table(self, action, goto, state):
        for a in action:
            self.assertTrue(action[a] in str(state.action[a]))
        
        for g in goto:
            self.assertEqual(goto[g], state.goto[g])

    def test_clr_parsing_table(self):
        print('test CLR parsing table')

        gen = ParserGenerator()
        gen.open('unittest/test_LR1_items.gram')
        gen.compute_LR1_items()
        gen.construct_clr_parsing_table()

        action = {'c':'s3', 'd':'s4', '$':''}
        goto = {'S':1, 'C':2}
        self.check_parsing_table(action, goto, gen.states[0])

        action = {'c':'', 'd':'', '$':'a'}
        goto = {'S':-1, 'C':-1}
        self.check_parsing_table(action, goto, gen.states[1])

        action = {'c':'s6', 'd':'s7', '$':''}
        goto = {'S':-1, 'C':5}
        self.check_parsing_table(action, goto, gen.states[2])

        action = {'c':'s3', 'd':'s4', '$':''}
        goto = {'S':-1, 'C':8}
        self.check_parsing_table(action, goto, gen.states[3])

        action = {'c':'r3', 'd':'r3', '$':''}
        goto = {'S':-1, 'C':-1}
        self.check_parsing_table(action, goto, gen.states[4])

        action = {'c':'', 'd':'', '$':'r1'}
        goto = {'S':-1, 'C':-1}
        self.check_parsing_table(action, goto, gen.states[5])

        action = {'c':'s6', 'd':'s7', '$':''}
        goto = {'S':-1, 'C':9}
        self.check_parsing_table(action, goto, gen.states[6])

        action = {'c':'', 'd':'', '$':'r3'}
        goto = {'S':-1, 'C':-1}
        self.check_parsing_table(action, goto, gen.states[7])

        action = {'c':'r2', 'd':'r2', '$':''}
        goto = {'S':-1, 'C':-1}
        self.check_parsing_table(action, goto, gen.states[8])

        action = {'c':'', 'd':'', '$':'r2'}
        goto = {'S':-1, 'C':-1}
        self.check_parsing_table(action, goto, gen.states[9])

        gen.parse_string('c c d d')

if __name__ == '__main__':
    unittest.main()


