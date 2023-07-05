import sys
sys.path += '../../'

from examples.calc.calc_parser_table import *
from examples.calc.calc_parser import Parser
from examples.calc.calc_lexer import CalcLexer

class Calc:
    def __init__(self):
        self.list_symbol = []
        self.lexer = CalcLexer()
    
    def compute(self, expr):
        list_symbol = self.lexer.lexer(expr)
        parser = Parser()
        result = parser.parse(list_symbol)
        
        return result

