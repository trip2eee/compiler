import sys
sys.path += '../../'
from src.yacc.parser_generator import ParserGenerator
from src.lex.lexer_generator import LexerGenerator

if __name__ == '__main__':
    gen = ParserGenerator()
    gen.generate_parser('examples/c_minus/c_minus.gram')
    gen.export('examples/c_minus/cmm_parser.py')

    gen = LexerGenerator()
    gen.open('examples/c_minus/c_minus.lex')
    gen.generate_code('examples/c_minus/cmm_lexer.py')

