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
    NUM_FLOAT = 3
    S1 = 4              # Slash(/) 1
    
    OP1 = 5
    OP2 = 6
    OP2_1 = 7
    OP3 = 8
    OP3_1 = 9
    
    STR = 10
    CHR = 11

    CMNT1   = 90
    CMNT2   = 91
    CMNT2_1 = 92

    DONE    = 100

class TokenType(enum.IntEnum):
    UNDEF = -1
    COMMENT = 0
    NUM = 1
    NUM_FLOAT = 2
    ID = 3
    STRING = 4
    CHAR = 5
    TYPE = 6

    SEMI = 10             # ;
    DOT  = 11             # .

    IF    = 100
    ELSE  = 101
    FOR   = 102
    WHILE = 103
    
    OP_PLUS      = 201         # +
    OP_MINUS     = 202         # -
    OP_TIMES     = 203         # *
    OP_DIV       = 204         # /
    OP_BIT_NOT   = 205         # ~
    OP_BIT_OR    = 206         # |
    OP_BIT_AND   = 207         # &
    OP_BIT_XOR   = 208         # ^
    OP_INC       = 209         # ++
    OP_DEC       = 210         # --
    OP_SHL       = 211         # Shift Left <<
    OP_SHR       = 212         # Shift Right >>
    OP_LOGIC_OR  = 213         # ||
    OP_LOGIC_AND = 214         # &&
    OP_LOGIC_NOT = 215         # !

    OP_ASSIGN          = 300   # =
    OP_ADD_ASSIGN      = 301   # +=
    OP_SUB_ASSIGN      = 302   # -=
    OP_MUL_ASSIGN      = 303   # *=
    OP_DIV_ASSIGN      = 304   # /=
    OP_SHL_ASSIGN      = 305   # <<=
    OP_SHR_ASSIGN      = 306   # >>=
    OP_BIT_OR_ASSIGN   = 307   # |=
    OP_BIT_AND_ASSIGN  = 308   # &=
    OP_BIT_NOT_ASSIGN  = 309   # ~=
    OP_BIT_XOR_ASSIGN  = 300   # ^=


    EQ      = 401          # ==
    LT      = 402          # <
    GT      = 403          # >
    LTE     = 404          # <=
    GTE     = 405          # >=
    NEQ     = 406          # !=
    
    LPAREN   = 500        # (
    RPAREN   = 501        # )
    LBRACKET = 502        # [
    RBRACKET = 503        # ]
    LBRACE   = 504        # {
    RBRACE   = 505        # }


class Token:
    def __init__(self, type, line_no, col_no):
        self.type = type
        self.string_val = ''
        self.int_val = 0
        self.float_val = 0.0
        self.line_number = line_no   # line number
        self.col_number = col_no     # column number

class Scanner:
    def __init__(self):
        self.idx_line = -1
        self.idx_char = -1
        self.line = ''
        self.f = None           # file handle
        self.list_tokens = []
    
    def __del__(self):
        if self.f is not None:
            self.f.close()

    def scan(self, file_path):
        self.f = open(file_path, 'r')
        self.list_tokens = []

        if self.f is not None:
            
            while True:
                token = self.get_token()
                if token is not None:
                    self.list_tokens.append(token)
                else:
                    break

        return self.list_tokens

    def get_token_other(self, c):
        token = None
        state = State.DONE

        if c == ';':
            token = self.make_token(TokenType.SEMI, c)            
        elif c == '(':
            token = self.make_token(TokenType.LPAREN, c)
        elif c == ')':
            token = self.make_token(TokenType.RPAREN, c)
        elif c == '[':
            token = self.make_token(TokenType.LBRACKET, c)
        elif c == ']':
            token = self.make_token(TokenType.RBRACKET, c)
        elif c == '{':
            token = self.make_token(TokenType.LBRACE, c)
        elif c == '}':
            token = self.make_token(TokenType.RBRACE, c)
        elif c == '.':
            token = self.make_token(TokenType.DOT, c)
        
        return token, state
    
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
    
    def determine_id_type(self, token: Token):
        val = token.string_val
        if val == 'int':
            token.type = TokenType.TYPE
        elif val == 'if':
            token.type = TokenType.IF
        elif val == 'else':
            token.type = TokenType.ELSE
        elif val == 'for':
            token.type = TokenType.FOR
        elif val == 'while':
            token.type = TokenType.WHILE

    def make_token(self, type: TokenType, c=None):
        token = Token(type, self.idx_line, self.idx_char)

        if c is not None:
            token.string_val = c
        else:
            token.string_val = ''

        return token

    def get_token(self):

        state = State.START
        token = None

        while state != State.DONE:
            c = self.get_next_char()
            
            # end of file
            if c == -1:
                break

            # Start State
            if state == State.START:
                # if white space
                if c == ' ' or c == '\t' or c == '\n':
                    pass

                # if digits
                elif self.is_digits(c):
                    token = self.make_token(TokenType.NUM, c)
                    state = State.NUM_INT
                
                # if letters
                elif self.is_letter(c):
                    token = self.make_token(TokenType.ID, c)
                    state = State.ID

                elif c == '/':
                    token = self.make_token(TokenType.OP_DIV, c)
                    state = State.S1

                elif c in '+-*!=~^':
                    if c == '=':
                        token = self.make_token(TokenType.OP_ASSIGN, c)
                    elif c == '+':
                        token = self.make_token(TokenType.OP_PLUS, c)
                    elif c == '-':
                        token = self.make_token(TokenType.OP_MINUS, c)
                    elif c == '*':
                        token = self.make_token(TokenType.OP_TIMES, c)
                    elif c == '/':
                        token = self.make_token(TokenType.OP_DIV, c)
                    elif c == '!':
                        token = self.make_token(TokenType.OP_LOGIC_NOT, c)
                    elif c == '~':
                        token = self.make_token(TokenType.OP_BIT_NOT, c)
                    elif c == '^':
                        token = self.make_token(TokenType.OP_BIT_XOR, c)

                    state = State.OP1

                elif c == '<' or c == '>':
                    if c == '<':
                        token = self.make_token(TokenType.LT, c)
                    elif c == '>':
                        token = self.make_token(TokenType.GT, c)
                    state = State.OP2

                elif c == '|' or c == '&':
                    if c == '|':
                        token = self.make_token(TokenType.OP_BIT_OR, c)
                    elif c == '&':
                        token = self.make_token(TokenType.OP_BIT_AND, c)
                    state = State.OP3
                
                # if double quotation mark
                elif c == '"':
                    token = self.make_token(TokenType.STRING)
                    state = State.STR
                
                # if single quotation mark
                elif c == "'":
                    token = self.make_token(TokenType.CHAR)
                    state = State.CHR
                    
                # other
                else:
                    token, state = self.get_token_other(c)
            # integer
            elif state == State.NUM_INT:
                if self.is_digits(c):
                    token.string_val += c
                elif c == 'u' or c == 'U':
                    token.int_val = int(token.string_val)
                    state = State.DONE
                elif c == '.':
                    token.string_val += c
                    token.type = TokenType.NUM_FLOAT
                    state = State.NUM_FLOAT
                else:
                    self.unget_next_char()
                    token.int_val = int(token.string_val)
                    state = State.DONE
            # floating point number
            elif state == State.NUM_FLOAT:
                if '0' <= c <= '9':
                    token.string_val += c
                elif c == 'f' or c == 'F':
                    token.float_val = float(token.string_val)
                    state = State.DONE
                else:
                    self.unget_next_char()
                    token.float_val = float(token.string_val)
                    state = State.DONE
            # identifier
            elif state == State.ID:
                if self.is_letter(c) or self.is_digits(c):
                    token.string_val += c
                else:
                    self.determine_id_type(token)

                    self.unget_next_char()
                    state = State.DONE
            
            elif state == State.S1:
                if c == '/':
                    token.string_val += c
                    state = State.CMNT1
                    token.type = TokenType.COMMENT
                elif c == '*':
                    token.string_val += c
                    state = State.CMNT2
                    token.type = TokenType.COMMENT
                elif c == '=':
                    token.string_val += c
                    token.type = TokenType.OP_DIV_ASSIGN
                    state = State.DONE
                else:
                    self.unget_next_char()
                    state = State.DONE
            
            # Comment type 1
            elif state == State.CMNT1:
                if c == '\n':
                    state = State.DONE
                else:
                    token.string_val += c
            
            # Comment type 2
            elif state == State.CMNT2:
                token.string_val += c
                if c == '*':
                    state = State.CMNT2_1
            elif state == State.CMNT2_1:
                token.string_val += c
                if c == '/':
                    state = State.DONE
                else:                    
                    state = State.CMNT2

            elif state == State.OP1:
                if c == '=' or c == '+' or c == '-':
                    token.string_val += c
                    if token.string_val == '++':
                        token.type = TokenType.OP_INC
                    elif token.string_val == '--':
                        token.type = TokenType.OP_DEC
                    elif token.string_val == '+=':
                        token.type = TokenType.OP_ADD_ASSIGN
                    elif token.string_val == '-=':
                        token.type = TokenType.OP_SUB_ASSIGN
                    elif token.string_val == '==':
                        token.type = TokenType.EQ
                    elif token.string_val == '!=':
                        token.type = TokenType.NEQ
                    elif token.string_val == '~=':
                        token.type = TokenType.OP_BIT_NOT_ASSIGN
                    elif token.string_val == '^=':
                        token.type = TokenType.OP_BIT_XOR_ASSIGN
                    else:
                        token.type == TokenType.UNDEF

                state = State.DONE
            
            elif state == State.OP2:                
                if c == '=':
                    token.string_val += c
                    if token.string_val == '<=':
                        token.type = TokenType.LTE
                    elif token.string_val == '>=':
                        token.type = TokenType.GTE
                    state = State.DONE
                elif c in '<>':
                    token.string_val += c
                    state = State.OP2_1
                else:
                    self.unget_next_char()
                    state = State.DONE
            
            elif state == State.OP2_1:
                if c == '=':
                    token.string_val += c
                    if token.string_val == '<<=':
                        token.type = TokenType.OP_SHL_ASSIGN
                    elif token.string_val == '>>=':
                        token.type = TokenType.OP_SHR_ASSIGN
                else:
                    self.unget_next_char()
                state = State.DONE

            elif state == State.OP3:
                if c == '=':
                    token.string_val += c
                    if token.string_val == '|=':
                        token.type = TokenType.OP_BIT_OR_ASSIGN
                    elif token.string_val == '&=':
                        token.type = TokenType.OP_BIT_AND_ASSIGN
                    else:
                        token.type = TokenType.UNDEF
                elif c in '|&':
                    token.string_val += c
                    if token.string_val == '||':
                        token.type = TokenType.OP_LOGIC_OR
                    elif token.string_val == '&&':
                        token.type = TokenType.OP_LOGIC_AND
                    else:
                        token.type = TokenType.UNDEF
                else:
                    self.unget_next_char()
                
                state = State.DONE

            # if string between " and "
            elif state == State.STR:
                if c == '"':
                    state = State.DONE
                else:
                    token.string_val += c

            # if a character between ' and '
            elif state == State.CHR:
                if c == "'":
                    state = State.DONE
                else:
                    token.string_val += c

        return token
        
    
    def get_next_char(self):
        # if no line data or the column number exceeds the length of the line.
        if self.line == '' or ((self.idx_char+1) >= len(self.line)):
            line = self.f.readline()
            self.idx_char = -1
            self.line = line
            self.idx_line += 1

        if self.line != '':
            self.idx_char += 1
            c = self.line[self.idx_char]
            return c
        else:
            return -1

    def unget_next_char(self):
        if self.idx_char > 0:
            self.idx_char -= 1


