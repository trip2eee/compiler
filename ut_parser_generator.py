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
        gen.print_result()

        symbols = ['S', 'C', 'D', 'a', 'b', 'c', 'd']
        
        self.assertEqual(len(gen.symbols), len(symbols))
        for i in range(len(symbols)):
            self.assertEqual(gen.symbols[i], symbols[i])

    def test_first(self):
        gen = ParserGenerator()
        gen.open('unittest/test2.gram')
        gen.print_result()

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
        gen = ParserGenerator()
        gen.open('unittest/test2.gram')
        gen.print_result()

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
        gen = ParserGenerator()
        gen.open('unittest/test3.gram')
        gen.print_result()

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
        
if __name__ == '__main__':
    unittest.main()