from src.parser_generator import ParserGenerator

if __name__ == '__main__':
    gen = ParserGenerator()
    gen.generate_parser('./src/regex.gram')
    gen.export('./src/regex_parser_table.py')

    # rule = "LBR CHAR MINUS CHAR RBR PLUS LBR CHAR RBR QUES LBR CHAR MINUS CHAR RBR TIMES LBR CHAR CHAR RBR QUES"
    # gen.parse_string(rule)