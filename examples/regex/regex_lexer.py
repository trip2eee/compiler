from examples.regex.regex_parser_table import *

class RegExLexer:
    def __init__(self):
        self.list_symbol = []
    
    def add_symbol(self, type=0, value=0):
        t = Symbol()
        t.type = type
        t.value = value
        self.list_symbol.append(t)
    
    def lexer(self, expr):
        idx_char = 0
        state = 0
        self.list_symbol = []
        
        while idx_char < len(expr):
            c = expr[idx_char]
            idx_char += 1

            if state == 0:
                # if escape character
                if c == '\\':
                    state = 1
                elif c == '+':
                    self.add_symbol(type=PLUS, value=c)
                elif c == '-':
                    self.add_symbol(type=MINUS, value=c)
                elif c == '*':
                    self.add_symbol(type=TIMES, value=c)
                elif c == '(':
                    self.add_symbol(type=LPAREN, value=c)
                elif c == ')':
                    self.add_symbol(type=RPAREN, value=c)
                elif c == '[':
                    self.add_symbol(type=LBRACKET, value=c)
                elif c == ']':
                    self.add_symbol(type=RBRACET, value=c)
                elif c == '|':
                    self.add_symbol(type=OR, value=c)
                else:
                    self.add_symbol(type=CHAR, value=c)
                
            elif state == 1:
                self.add_symbol(type=ESC, value=c)
                state = 0

        return self.list_symbol