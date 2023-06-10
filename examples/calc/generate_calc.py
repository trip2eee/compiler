import sys
sys.path += '../../'
from src.parser_generator import ParserGenerator

if __name__ == '__main__':
    print('calc parser generator')

    gen = ParserGenerator()
    # generate a parser from a grammar file.
    gen.generate_parser('examples/calc/calc.gram')
    # export the parser in python code.
    gen.export('examples/calc/calc_parser.py')



