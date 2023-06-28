import sys
sys.path += '../../'
from src.yacc.parser_generator import ParserGenerator

if __name__ == '__main__':
    gen = ParserGenerator()
    gen.generate_parser('src/lex/regex.gram')
    gen.export('src/lex/regex_parser.py')
