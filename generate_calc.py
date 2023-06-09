import os
import sys
      
from src.parser_generator import ParserGenerator


if __name__ == '__main__':
    print('calc parser generator')

    stack = [0, 1, 2, 3]

    gen = ParserGenerator()
    gen.generate_parser('unittest/test_calc.gram')
    gen.export('examples/calc/calc_parser_table.py')



