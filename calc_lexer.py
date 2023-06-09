from examples.calc.calc_parser_table import *
from examples.calc.calc_parser import *

class Calc:
    def __init__(self):
        self.list_symbol = []
    
    def compute(self, expr):
        self.lexer(expr)

        result = parse(self.list_symbol)
        return result

    def add_symbol(self, type=0, value=0):
        t = Symbol()
        t.type = type
        t.value = value
        self.list_symbol.append(t)
        
    def lexer(self, expr):
        idx_char = 0
        state = 0
        num = ''
        
        while idx_char < len(expr) + 1:
            if idx_char < len(expr):
                c = expr[idx_char]
            else:
                c = '$'

            idx_char += 1

            if state == 0:
                if '0' <= c <= '9':
                    num = c
                    state = 1
                elif c == '+':
                    self.add_symbol(type=PLUS, value=c)
                elif c == '-':
                    self.add_symbol(type=MINUS, value=c)
                elif c == '*':
                    self.add_symbol(type=TIMES, value=c)
                elif c == '/':
                    self.add_symbol(type=DIV, value=c)
            elif state == 1:
                if '0' <= c <= '9':
                    num += c
                else:
                    self.add_symbol(type=number, value=int(num))
                    idx_char -= 1
                    state = 0

if __name__ == '__main__':
    calc = Calc()
    result = calc.compute('10 + 20 * 2')
    y = 10 + 20 * 2
    print('{} = {}'.format(result.value, y))

    result = calc.compute('10 + 20 - 5 * 3 / 2')
    y = 10 + 20 - 5 * 3 / 2
    print('{} = {}'.format(result.value, y))

    print('done')
