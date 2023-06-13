from examples.regex.regex_parser_table import *

class RegExLexer:
    def __init__(self):
        self.list_symbol = []
    
    def add_symbol(self, type=0, value=0):
        t = Symbol()
        t.type = type
        t.value = value
        t.idx_col = self.idx_char
        self.list_symbol.append(t)
    
    def lexer(self, expr):
        self.idx_char = 0
        state = 0
        self.list_symbol = []
        
        while self.idx_char < len(expr):
            c = expr[self.idx_char]
            self.idx_char += 1

            if state == 0:                
                if c == '\\':
                    # if escape character
                    state = 1
                elif c == '+':
                    self.add_symbol(type=PLUS, value=c)
                elif c == '-':
                    self.add_symbol(type=MINUS, value=c)
                elif c == '*':
                    self.add_symbol(type=TIMES, value=c)
                elif c == '?':
                    self.add_symbol(type=QUES, value=c)
                elif c == '(':
                    self.add_symbol(type=LPAREN, value=c)
                elif c == ')':
                    self.add_symbol(type=RPAREN, value=c)
                elif c == '[':
                    self.add_symbol(type=LBRACKET, value=c)
                elif c == ']':
                    self.add_symbol(type=RBRACKET, value=c)
                elif c == '{':
                    self.add_symbol(type=LBRACE, value=c)
                elif c == '}':
                    self.add_symbol(type=RBRACE, value=c)
                elif c == '|':
                    self.add_symbol(type=OR, value=c)
                elif c == ',':
                    self.add_symbol(type=COMMA, value=c)
                else:
                    if '0' <= c <= '9':
                        self.add_symbol(type=DIGIT, value=c)
                    else:
                        self.add_symbol(type=CHAR, value=c)
                
            elif state == 1:
                if c == 'd':
                    self.add_symbol(type=ESC, value=c)
                else:
                    self.add_symbol(type=CHAR, value=c)
                state = 0

        return self.list_symbol