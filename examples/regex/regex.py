from examples.regex.regex_parser_table import *
from examples.regex.regex_parser import parse
from examples.regex.regex_lexer import RegExLexer

class RegEx:
    def __init__(self):
        self.list_symbol = []
        self.lexer = RegExLexer()
    
    def set_pattern(self, expr):
        list_symbol = self.lexer.lexer(expr)
        self.result = parse(list_symbol)
        
        return self.result

    def match(self, str):
        matched = False
        matched_string = ''

        for idx_begin in range(len(str)):

            # match
            substr_matched, matched_string = self.__match_substring(str[idx_begin:])
            if substr_matched:
                matched = substr_matched
                break

        return matched, matched_string
    
    def __match_substring(self, substr):
        symbol: Symbol
        symbol = self.result

        matched_str = ''

        idx_char = 0
        while symbol is not None and idx_char < len(substr):
            matched = False
            c = substr[idx_char]

            pattern : Pattern
            pattern = symbol.pattern

            if pattern.type == Pattern.VALUE:
                if pattern.value == c:
                    matched = True
                    matched_str += c

            if matched == False:
                break
            else:
                symbol = symbol.next
                idx_char += 1
        
        return matched, matched_str
                


