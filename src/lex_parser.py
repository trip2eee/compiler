"""
@fn lex_parser.py
@brief .lex file parser
@author Jongmin Park(trip2eee@gmail.com)
@date 2023-06-14
"""

import enum

C_LBRACE = '{'
C_RBRACE = '}'
C_NEW_LINE = '\n'
C_QUOT = '\''
C_CMT = '#'

class State(enum.IntEnum):
    IDLE = 0
    SYMBOL = 1
    STRING = 2
    ACTION = 3
    COMMENT = 4


class TokenType(enum.IntEnum):
    NDEF = 0
    SYMBOL = 1
    STRING = 2
    ACTION = 3
    COMMENT = 4
    NEW_LINE = 5

class Token:
    def __init__(self):
        self.type = TokenType.NDEF
        self.string = ''
        self.alias = ''
    def __str__(self):
        return self.string

class Rule:
    RULE_ID = 0
    def __init__(self):
        self.symbol = ''
        self.string = ''
        self.node = None        
        self.reduce_action = ''
        self.mark = 0

        self.id = Rule.RULE_ID
        Rule.RULE_ID += 1

    def mark_symbol(self):
        if self.mark < len(self.string):
            return self.string[self.mark]
        else:
            return None
    
    def __str__(self):
        s = self.symbol
        s += ' -> '
        for idx_ch in range(len(self.string)):
            if self.mark == idx_ch:
                s += '.'
            s += self.string[idx_ch]
        
        if self.mark == len(self.string):
            s += '.'

        return s

    def copy(self):
        new_rule = Rule()
        new_rule.symbol = self.symbol
        new_rule.string = self.string
        new_rule.node = self.node
        new_rule.id = self.id
        new_rule.reduce_action = self.reduce_action
        new_rule.mark = self.mark

        return new_rule

class LexParser:
    def __init__(self):
        self.rules = []
        self.terminals = []

        self.state = State.IDLE
        self.cur_token = None
        self.idx_line = 0
        self.idx_char = -1
        self.line = ''

        self.f = None
                
        self.definition = ''
        self.aux_routines = ''

        self.num_braces = 0
        
        self.idx_token = 0
        self.list_tokens = []
        
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
        self.parse()

        while True:
            line = self.f.readline()
            if line == '':
                break
            self.aux_routines += line
        
        self.f.close()

    def parse(self):
        self.tokenize()

        self.state = State.IDLE
        while True:
            token:Token
            token = self.get_token()
            if token is None:
                break

            if self.state == State.IDLE:
                if token.type == TokenType.SYMBOL:
                                        
                    rule = Rule()
                    rule.symbol = token.string
                    self.rules.append(rule)
                    self.cur_rule = rule

                    self.state = State.SYMBOL

            elif self.state == State.SYMBOL:
                if token.type == TokenType.STRING:
                    self.cur_rule.string = token.string

                    self.state = State.STRING
                else:
                    print('ERROR')
            
            elif self.state == State.STRING:
                if token.type == TokenType.NEW_LINE:
                    pass # No Action
                elif token.type == TokenType.ACTION:
                   self.cur_rule.reduce_action = token.string
                else:
                    print('ERROR')
                
                self.state = State.IDLE

    def get_token(self):
        if self.idx_token < len(self.list_tokens):
            token = self.list_tokens[self.idx_token]
            self.idx_token += 1
        else:
            token = None
        return token
    
    def tokenize(self):
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

                elif c == C_CMT:
                    self.cur_token = Token()
                    self.cur_token.type = TokenType.COMMENT
                    self.cur_token.string = c
                    # self.list_tokens.append(self.cur_token)
                    self.state = State.COMMENT
                                
                elif c == C_QUOT:
                    self.cur_token = Token()
                    self.state = State.STRING

                elif c == C_LBRACE:
                    self.cur_token = Token()
                    self.cur_token.type = TokenType.ACTION
                    self.list_tokens.append(self.cur_token)
                    self.num_braces += 1
                    self.state = State.ACTION
                
                elif c == C_NEW_LINE:
                    self.cur_token = Token()
                    self.cur_token.type = TokenType.NEW_LINE
                    self.list_tokens.append(self.cur_token)

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
            
            elif self.state == State.STRING:
                
                if c == "'":
                    self.cur_token.type = TokenType.STRING
                    self.list_tokens.append(self.cur_token)
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