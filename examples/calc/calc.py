from examples.calc.calc_parser_table import *
from examples.calc.calc_parser import parse
from examples.calc.calc_lexer import CalcLexer

class Calc:
    def __init__(self):
        self.list_symbol = []
        self.lexer = CalcLexer()
    
    def compute(self, expr):
        list_symbol = self.lexer.lexer(expr)
        result = parse(list_symbol)
        
        return result

