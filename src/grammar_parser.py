"""
@fn grammar_file_parser.py
@brief .gram file parser
@author Jongmin Park(trip2eee@gmail.com)
@date 2023-06-08
"""

import enum

C_OR = '|'
C_COLON = ':'
C_SEMI = ';'
C_CMT = '#'
C_LBRACE = '{'
C_RBRACE = '}'
C_NEW_LINE = '\n'

EPSILON = 'ep'  # empty string epsilon

class State(enum.IntEnum):
    IDLE = 0
    SYMBOL = 1
    ACTION = 2
    COMMENT = 3
    SYMBOL2 = 4

    LEFT = 10
    RIGHT = 11

class TokenType(enum.IntEnum):
    NDEF = 0
    SYMBOL = 1
    OR = 2
    COLON = 3
    SEMI = 4
    ACTION = 5
    COMMENT = 6

class Token:
    def __init__(self):
        self.type = TokenType.NDEF
        self.string = ''
        self.alias = ''
    def __str__(self):
        return self.string


class Rule:
    def __init__(self, non_terminal):
        self.left_symbol = non_terminal
        self.strings = []   # two dimensional array of strings
        self.rule_ids = []  # IDs of rules
        self.first = []     # First set
        self.follow = []    # Follow set
        self.reduce_actions = []

    def __str__(self):
        str = self.left_symbol
        str += ' -> '
        
        for idx_str in range(len(self.strings)):
            for s in self.strings[idx_str]:
                str += s + ' '
            
            if idx_str < len(self.reduce_actions) and self.reduce_actions[idx_str] != '':
                str += '  : { ' + self.reduce_actions[idx_str] + ' }'

            if idx_str < len(self.strings)-1:
                str += '\n'
                for i in range(len(self.left_symbol)+2):
                    str += ' '
                str += '| '

        return str
    
    def add_first(self, f):
        if f not in self.first:
            self.first.append(f)
            return 1
        else:
            return 0
        
    def add_follow(self, f):
        if f not in self.follow and f != EPSILON:
            self.follow.append(f)
            return 1
        else:
            return 0

    def print_first(self):
        print('First({}) = '.format(self.left_symbol), end='')
        print('{', end='')
        for f in self.first:
            print('{}, '.format(f), end='')
        print('}')
    
    def print_follow(self):
        print('Follow({}) = '.format(self.left_symbol), end='')
        print('{', end='')
        for f in self.follow:
            print('{}, '.format(f), end='')
        print('}')

class GarmmarParser:
    def __init__(self):
        self.rules = {}
        
        self.symbols = []
        self.non_terminals = []
        self.terminals = []

        self.cur_non_terminal = ''
        self.cur_rule = None

        self.start_symbol = None    # the start symbol of program (the first non-terminal of grammar file)

        self.state = State.IDLE
        self.cur_token = None
        self.idx_line = 0
        self.idx_char = -1
        self.line = ''
        self.f = None           # file handle        

        self.definition = ''
        self.aux_routines = ''

        self.num_braces = 0
        
        self.idx_token = 0
        self.list_tokens = []

        self.cur_string = []
        self.cur_reduce_action = ''
        self.embedded_action = {}        
        
    def __del__(self):
        if self.f is not None:
            self.f.close()

    def open(self, file_path):
        
        self.f = open(file_path, 'r')
        # find definitions
        while True:
            line = self.f.readline()

            if line == '':
                break
            
            self.idx_line += 1
            if line.strip() == '%%':
                break
            else:
                self.definition += line

        # find rules
        self.parse(file_path)

        while True:
            line = self.f.readline()
            if line == '':
                break
            self.aux_routines += line
        
        self.f.close()

    def parse(self, file_path):
        self.tokenize(file_path)

        self.state = State.IDLE
        while True:
            token:Token
            token = self.get_token()
            if token is None:
                break

            if self.state == State.IDLE:
                if token.type == TokenType.SYMBOL:
                    
                    non_terminal = token.string
                    self.cur_non_terminal = non_terminal

                    if self.start_symbol is None:
                        self.start_symbol = non_terminal

                    if non_terminal not in self.symbols:
                        self.symbols.append(non_terminal)

                    if non_terminal not in self.non_terminals:
                        self.non_terminals.append(non_terminal)

                    rule = Rule(self.cur_non_terminal)
                    self.rules[self.cur_non_terminal] = rule
                    self.cur_rule = rule

                    self.state = State.LEFT
                else:
                    print('ERROR: The definition of a rule shall start with a symbol')

            elif self.state == State.LEFT:
                if token.type == TokenType.COLON:
                    self.cur_string = []
                    self.cur_reduce_action = ''
                    self.cur_rule.strings.append(self.cur_string)
                    self.cur_rule.reduce_actions.append(self.cur_reduce_action)

                    self.state = State.RIGHT
                else:
                    print('ERROR')
            
            elif self.state == State.RIGHT:
                if token.type == TokenType.SYMBOL:
                    symbol = token.string
                    self.cur_string.append(symbol)

                    if symbol not in self.symbols:
                        self.symbols.append(symbol)

                elif token.type == TokenType.ACTION:
                    # check the next token
                    if self.idx_token < len(self.list_tokens) and self.idx_token >= 2:
                        prev_token:Token
                        next_token:Token                        
                        prev_token = self.list_tokens[self.idx_token-2]
                        next_token = self.list_tokens[self.idx_token]
                        if prev_token.type == TokenType.SYMBOL:
                            if next_token.type == TokenType.SYMBOL:
                                # add embedded action for the previous string
                                self.embedded_action[prev_token.string] = token.string
                            elif next_token.type == TokenType.OR or next_token.type == TokenType.SEMI:
                                # update reduce action
                                self.cur_rule.reduce_actions[-1] = token.string
                    else:
                        print('ERROR')

                elif token.type == TokenType.OR:
                    self.cur_string = []
                    self.cur_reduce_action = ''
                    self.cur_rule.strings.append(self.cur_string)
                    self.cur_rule.reduce_actions.append(self.cur_reduce_action)

                elif token.type == TokenType.SEMI:
                    self.state = State.IDLE

        
        for s in self.symbols:
            if s not in self.non_terminals:
                self.terminals.append(s)

    def get_token(self):
        if self.idx_token < len(self.list_tokens):
            token = self.list_tokens[self.idx_token]
            self.idx_token += 1
        else:
            token = None
        return token

    def set_token_alias(self):
        if self.cur_token.string == '=':
            self.cur_token.alias = 'EQUAL'
        elif self.cur_token.string == '+':
            self.cur_token.alias = 'PLUS'
        elif self.cur_token.string == '-':
            self.cur_token.alias = 'MINUS'
        elif self.cur_token.string == '*':
            self.cur_token.alias = 'TIMES'
        elif self.cur_token.string == '/':
            self.cur_token.alias = 'DIV'
        elif self.cur_token.string == '(':
            self.cur_token.alias = 'LPAREN'
        elif self.cur_token.string == ')':
            self.cur_token.alias = 'RPAREN'
        elif self.cur_token.string == '[':
            self.cur_token.alias = 'LBRACKET'
        elif self.cur_token.string == ']':
            self.cur_token.alias = 'RBRACET'
        elif self.cur_token.string == '.':
            self.cur_token.alias = 'DOT'
        elif self.cur_token.string == ',':
            self.cur_token.alias = 'COMMA'
        elif self.cur_token.string == '$':
            self.cur_token.alias = 'END'

    def tokenize(self, file_path):
        self.state = State.IDLE

        while True:
            c = self.get_next_char()
            if c is None:
                break

            if self.state == State.IDLE:
                if self.is_letter(c):
                    self.cur_token = Token()
                    self.cur_token.type = TokenType.SYMBOL
                    self.cur_token.string = c
                    self.list_tokens.append(self.cur_token)
                    self.state = State.SYMBOL

                
                elif c in '=_+-*/()$[].,':
                    self.cur_token = Token()
                    self.cur_token.type = TokenType.SYMBOL
                    self.cur_token.string = c
                    self.list_tokens.append(self.cur_token)
                    self.set_token_alias()

                elif c == C_CMT:
                    self.cur_token = Token()
                    self.cur_token.type = TokenType.COMMENT
                    self.cur_token.string = c
                    # self.list_tokens.append(self.cur_token)
                    self.state = State.COMMENT
                    
                elif c == C_COLON:
                    token = Token()
                    token.type = TokenType.COLON
                    token.string = c
                    self.list_tokens.append(token)

                elif c == C_OR:
                    token = Token()
                    token.type = TokenType.OR
                    token.string = c
                    self.list_tokens.append(token)
                
                elif c == C_SEMI:
                    token = Token()
                    token.type = TokenType.SEMI
                    token.string = c
                    self.list_tokens.append(token)

                elif c == C_LBRACE:
                    self.cur_token = Token()
                    self.cur_token.type = TokenType.ACTION
                    self.list_tokens.append(self.cur_token)
                    self.num_braces += 1
                    self.state = State.ACTION                


            elif self.state == State.SYMBOL:
                if self.is_letter(c) or self.is_digits(c):
                    self.cur_token.string += c
                else:
                    self.unget_next_char()
                    self.state = State.IDLE

            elif self.state == State.ACTION:
                if c == C_RBRACE:
                    self.num_braces -= 1
                    if self.num_braces == 0:
                        self.state = State.IDLE
                    else:
                        self.cur_token.string += c
                else:
                    self.cur_token.string += c
            
            elif self.state == State.COMMENT:
                if c == C_NEW_LINE:
                    self.state = State.IDLE
                else:
                    self.cur_token.string += c

    def is_digits(self, c):
        if '0' <= c <= '9':
            return True
        else:
            return False
    
    def is_letter(self, c):
        if 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_':
            return True
        else:
            return False
        
    def get_next_char(self):
        # if no line data or the column number exceeds the length of the line.
        if self.line == '' or ((self.idx_char+1) >= len(self.line)):
            line = self.f.readline()
            self.idx_char = -1
            self.line = line
            self.idx_line += 1

        if self.line != '' and self.line[0:2] != '%%':
            self.idx_char += 1
            c = self.line[self.idx_char]
            return c
        else:
            return None

    def unget_next_char(self):
        if self.idx_char > 0:
            self.idx_char -= 1
