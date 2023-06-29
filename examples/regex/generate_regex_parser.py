import sys
sys.path += '../../'
from src.yacc.parser_generator import ParserGenerator

if __name__ == '__main__':
    gen = ParserGenerator()
    gen.generate_parser('examples/regex/regex.gram')
    gen.export('examples/regex/regex_parser.py')
