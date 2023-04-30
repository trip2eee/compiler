"""
C-- Lexical Scanner
@author Jongmin Park (trip2eee@gmail.com)
@date 2023-04-29   
"""
import enum

class State(enum.IntEnum):
    START = 0
    ID = 1
    NUM_INT = 2
    NUM_FRAC = 3
    OP1 = 4
    S1 = 5
    
    CMNT1   = 90
    CMNT2   = 91
    CMNT2_1 = 92

    DONE    = 100

class TokenType(enum.IntEnum):
    UNDEF = -1
    NUM = 0
    NUM_FRAC = 1
    STRING = 2

    IF    = 10
    ELSE  = 11
    FOR   = 12
    WHILE = 13

    PLUS   = 100          # +
    MINUS  = 101          # -
    MUL    = 102          # *
    DIV    = 103          # /
    ASSIGN = 104          # =
    EQ     = 105          # ==
    LT     = 106          # <
    GT     = 107          # >
    LTE    = 108          # <=
    GTE    = 109          # >=
    NEQ    = 110          # !=
    
    LPAREN   = 200        # (
    RPAREN   = 201        # )
    LBRACKET = 202        # [
    RBRACKET = 203        # ]
    LBRACE   = 204        # {
    RBRACE   = 205        # }


class Token:
    def __init__(self):
        self.type = TokenType.UNDEF
        self.string_val = ''
        self.int_val = 0
        self.frac_val = 0.0
        self.line_number = 0
        self.column_number = 0

class Scanner:
    def __init__(self):
        self.line_number = 0
        self.idx_char = 0
        self.line = ''
        self.state = State.START
        self.f = None
        self.list_tokens = []

    def scan(self, file_path):
        self.f = open(file_path, 'r')




    def get_token(self):
        pass
    
    def get_next_char(self):
        if self.idx_char < len(self.line) - 1:
            self.idx_char += 1

            

    def unget_next_char(self):
        if self.idx_char > 0:
            self.idx_char -= 1


