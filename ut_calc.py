import unittest
from examples.calc.calc import *

class TestCalc(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_calc1(self):
        calc = Calc()
        result = calc.compute('(10 + 20)')
        y = (10 + 20)

        print('{} = {}'.format(result.value, y))
        self.assertEqual(result.value, y)

    def test_calc2(self):
        calc = Calc()
        result = calc.compute('10 + 20 * 2')
        y = 10 + 20 * 2

        print('{} = {}'.format(result.value, y))
        self.assertEqual(result.value, y)

    def test_calc3(self):
        calc = Calc()
        result = calc.compute('10 + (20 - 5) * 3 / (2 + 4)')
        y = 10 + (20 - 5) * 3 / (2 + 4)

        print('{} = {}'.format(result.value, y))
        self.assertEqual(result.value, y)
    
    def test_calc4(self):
        calc = Calc()
        result = calc.compute('10 + (20 - +5) * 3 / (2 + -4)')
        y = 10 + (20 - +5) * 3 / (2 + -4)

        print('{} = {}'.format(result.value, y))
        self.assertEqual(result.value, y)

if __name__ == '__main__':
    unittest.main()
