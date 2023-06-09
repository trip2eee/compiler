import sys

sys.path += '../../'
from src.parser_generator import ParserGenerator

if __name__ == '__main__':
    print('calc parser generator')

    gen = ParserGenerator()
    gen.generate_parser('examples/calc/calc.gram')
    gen.export('examples/calc/calc_parser.py')



