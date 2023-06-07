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

    def test_lalr_parsing_table(self):
        print('test LALR parsing table')

        gen = ParserGenerator()
        gen.open('unittest/test_LALR_parsing_table.gram')
        gen.compute_LR0_items()
        gen.print_first_follow()
        gen.construct_lalr_parsing_table()

        self.assertEqual(len(gen.states[0].closure.items[0].lookahead), 0)

        self.assertEqual(len(gen.states[1].closure.items[0].lookahead), 0)

        self.assertEqual(len(gen.states[2].closure.items[0].lookahead), 0)
        self.assertEqual(len(gen.states[2].closure.items[1].lookahead), 0)

        self.assertEqual(len(gen.states[3].closure.items[0].lookahead), 0)

        self.assertEqual(len(gen.states[5].closure.items[0].lookahead), 1)
        self.assertEqual(gen.states[5].closure.items[0].lookahead[0], '=')

        self.assertEqual(len(gen.states[7].closure.items[0].lookahead), 1)
        self.assertEqual(gen.states[7].closure.items[0].lookahead[0], '=')

        self.assertEqual(len(gen.states[8].closure.items[0].lookahead), 1)
        self.assertEqual(gen.states[8].closure.items[0].lookahead[0], '=')

        self.assertEqual(len(gen.states[9].closure.items[0].lookahead), 0)

        action = {'=':'', '*':'s4', 'id':'s5', '$':''}
        goto = {'S':1, 'R':3, 'L':2}
        self.check_parsing_table(action, goto, gen.states[0])

        action = {'=':'', '*':'', 'id':'', '$':'a'}
        goto = {'S':-1, 'R':-1, 'L':-1}
        self.check_parsing_table(action, goto, gen.states[1])

        action = {'=':'s6', '*':'', 'id':'', '$':'r5'}
        goto = {'S':-1, 'R':-1, 'L':-1}
        self.check_parsing_table(action, goto, gen.states[2])

        action = {'=':'', '*':'', 'id':'', '$':'r2'}
        goto = {'S':-1, 'R':-1, 'L':-1}
        self.check_parsing_table(action, goto, gen.states[3])

        action = {'=':'', '*':'s4', 'id':'s5', '$':''}
        goto = {'S':-1, 'R':7, 'L':8}
        self.check_parsing_table(action, goto, gen.states[4])

        action = {'=':'r4', '*':'', 'id':'', '$':'r4'}
        goto = {'S':-1, 'R':-1, 'L':-1}
        self.check_parsing_table(action, goto, gen.states[5])

        action = {'=':'', '*':'s4', 'id':'s5', '$':''}
        goto = {'S':-1, 'R':9, 'L':8}
        self.check_parsing_table(action, goto, gen.states[6])

        action = {'=':'r3', '*':'', 'id':'', '$':'r3'}
        goto = {'S':-1, 'R':-1, 'L':-1}
        self.check_parsing_table(action, goto, gen.states[7])

        action = {'=':'r5', '*':'', 'id':'', '$':'r5'}
        goto = {'S':-1, 'R':-1, 'L':-1}
        self.check_parsing_table(action, goto, gen.states[8])

        action = {'=':'', '*':'', 'id':'', '$':'r1'}
        goto = {'S':-1, 'R':-1, 'L':-1}
        self.check_parsing_table(action, goto, gen.states[9])

        gen.parse_string('* id = id')


    def test_lalr_parsing_table2(self):
        print('test LALR parsing table 2')

        gen = ParserGenerator()
        gen.open('unittest/test_LALR_parsing_table2.gram')
        gen.compute_LR0_items()
        gen.construct_lalr_parsing_table()

        action = {'+':'', '-':'', '*':'', 'NUMBER':'s5', '(':'s6', ')':'', '$':''}
        goto = {'CMD':1, 'EXP':2, 'TERM':3, 'FACTOR':4}
        self.check_parsing_table(action, goto, gen.states[0])
        
        action = {'+':'', '-':'', '*':'', 'NUMBER':'', '(':'', ')':'', '$':'a'}
        goto = {'CMD':-1, 'EXP':-1, 'TERM':-1, 'FACTOR':-1}
        self.check_parsing_table(action, goto, gen.states[1])

        action = {'+':'s7', '-':'s8', '*':'', 'NUMBER':'', '(':'', ')':'', '$':'r1'}
        goto = {'CMD':-1, 'EXP':-1, 'TERM':-1, 'FACTOR':-1}
        self.check_parsing_table(action, goto, gen.states[2])

        action = {'+':'r4', '-':'r4', '*':'s9', 'NUMBER':'', '(':'', ')':'r4', '$':'r4'}
        goto = {'CMD':-1, 'EXP':-1, 'TERM':-1, 'FACTOR':-1}
        self.check_parsing_table(action, goto, gen.states[3])

        action = {'+':'r6', '-':'r6', '*':'r6', 'NUMBER':'', '(':'', ')':'r6', '$':'r6'}
        goto = {'CMD':-1, 'EXP':-1, 'TERM':-1, 'FACTOR':-1}
        self.check_parsing_table(action, goto, gen.states[4])

        action = {'+':'r7', '-':'r7', '*':'r7', 'NUMBER':'', '(':'', ')':'r7', '$':'r7'}
        goto = {'CMD':-1, 'EXP':-1, 'TERM':-1, 'FACTOR':-1}
        self.check_parsing_table(action, goto, gen.states[5])

        action = {'+':'', '-':'', '*':'', 'NUMBER':'s5', '(':'s6', ')':'', '$':''}
        goto = {'CMD':-1, 'EXP':10, 'TERM':3, 'FACTOR':4}
        self.check_parsing_table(action, goto, gen.states[6])

        action = {'+':'', '-':'', '*':'', 'NUMBER':'s5', '(':'s6', ')':'', '$':''}
        goto = {'CMD':-1, 'EXP':-1, 'TERM':11, 'FACTOR':4}
        self.check_parsing_table(action, goto, gen.states[7])

        action = {'+':'', '-':'', '*':'', 'NUMBER':'s5', '(':'s6', ')':'', '$':''}
        goto = {'CMD':-1, 'EXP':-1, 'TERM':12, 'FACTOR':4}
        self.check_parsing_table(action, goto, gen.states[8])

        action = {'+':'', '-':'', '*':'', 'NUMBER':'s5', '(':'s6', ')':'', '$':''}
        goto = {'CMD':-1, 'EXP':-1, 'TERM':-1, 'FACTOR':13}
        self.check_parsing_table(action, goto, gen.states[9])

        action = {'+':'s7', '-':'s8', '*':'', 'NUMBER':'', '(':'', ')':'s14', '$':''}
        goto = {'CMD':-1, 'EXP':-1, 'TERM':-1, 'FACTOR':-1}
        self.check_parsing_table(action, goto, gen.states[10])

        action = {'+':'r2', '-':'r2', '*':'s9', 'NUMBER':'', '(':'', ')':'r2', '$':'r2'}
        goto = {'CMD':-1, 'EXP':-1, 'TERM':-1, 'FACTOR':-1}
        self.check_parsing_table(action, goto, gen.states[11])

        action = {'+':'r3', '-':'r3', '*':'s9', 'NUMBER':'', '(':'', ')':'r3', '$':'r3'}
        goto = {'CMD':-1, 'EXP':-1, 'TERM':-1, 'FACTOR':-1}
        self.check_parsing_table(action, goto, gen.states[12])

        action = {'+':'r5', '-':'r5', '*':'r5', 'NUMBER':'', '(':'', ')':'r5', '$':'r5'}
        goto = {'CMD':-1, 'EXP':-1, 'TERM':-1, 'FACTOR':-1}
        self.check_parsing_table(action, goto, gen.states[13])

        action = {'+':'r8', '-':'r8', '*':'r8', 'NUMBER':'', '(':'', ')':'r8', '$':'r8'}
        goto = {'CMD':-1, 'EXP':-1, 'TERM':-1, 'FACTOR':-1}
        self.check_parsing_table(action, goto, gen.states[14])

        gen.parse_string('NUMBER * ( NUMBER + NUMBER )')

        print('done')

if __name__ == '__main__':
    unittest.main()


