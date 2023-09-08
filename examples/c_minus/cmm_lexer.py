"""
@fn examples/c_minus/cmm_lexer.py
@brief Lexer table generated by lexer_generator.py
@date 2023-09-09 16:19:12
"""


# Definitions


from cmm_parser_table import *




class Lexer:
    def __init__(self):        
        self.idx_char = 0
        self.idx_line = 0
        self.idx_col = -1
        self.idx_col_prev = -1
        self.idx_line_prev = -1

        self.idx_start = 0
        self.idx_start_col = 0
        self.idx_start_line = 0

        self.code = ''
        self.list_tokens = []
    
    def get_char(self):
        if self.idx_char < len(self.code):
            c = self.code[self.idx_char]

            self.idx_line_prev = self.idx_line
            self.idx_col_prev = self.idx_col

            self.idx_char += 1
            self.idx_col += 1

            # handle new line.
            if c == '\n':
                self.idx_line += 1
                self.idx_col = -1

            return c
        else:
            self.idx_char += 1
            return '\n'

    def unget_char(self):
        if self.idx_char > 0:
            self.idx_char -= 1

            self.idx_line = self.idx_line_prev
            self.idx_col = self.idx_col_prev            

    def get_text(self):
        return self.code[self.idx_start:self.idx_char-1]

    def add_token(self, yytext, yytype):
        node = TreeNode()
        node.type = yytype
        node.text = yytext
        node.idx_line = self.idx_start_line+1
        node.idx_col = self.idx_start_col+1
        self.list_tokens.append(node)

    def error_handler(self):
        text = self.code[self.idx_start:self.idx_char]
        if text != '\n' and text != '\t' and text != ' ' and text != '':
            print("Error: Unexpected token: '{}' in {}:{}".format(text, self.idx_line+1, self.idx_col+1))

    def scan(self, file_path):
        
        f = open(file_path, 'r')
        if f is not None:
            self.code = f.read()
            f.close()
            self.__scan()
            return True
        else:
             return False

    def __scan(self):
        state = 0
        self.list_tokens = []
        while self.idx_char <= len(self.code):
            c = self.get_char()

            if 0 == state:
                self.idx_start = self.idx_char - 1
                self.idx_start_col = self.idx_col
                self.idx_start_line = self.idx_line
                state = self.state_0(c)
            elif 1 == state:
                state = self.state_1(c)
            elif 2 == state:
                state = self.state_2(c)
            elif 3 == state:
                state = self.state_3(c)
            elif 4 == state:
                state = self.state_4(c)
            elif 5 == state:
                state = self.state_5(c)
            elif 6 == state:
                state = self.state_6(c)
            elif 7 == state:
                state = self.state_7(c)
            elif 8 == state:
                state = self.state_8(c)
            elif 9 == state:
                state = self.state_9(c)
            elif 10 == state:
                state = self.state_10(c)
            elif 11 == state:
                state = self.state_11(c)
            elif 12 == state:
                state = self.state_12(c)
            elif 13 == state:
                state = self.state_13(c)
            elif 14 == state:
                state = self.state_14(c)
            elif 15 == state:
                state = self.state_15(c)
            elif 16 == state:
                state = self.state_16(c)
            elif 17 == state:
                state = self.state_17(c)
            elif 18 == state:
                state = self.state_18(c)
            elif 19 == state:
                state = self.state_19(c)
            elif 20 == state:
                state = self.state_20(c)
            elif 21 == state:
                state = self.state_21(c)
            elif 22 == state:
                state = self.state_22(c)
            elif 23 == state:
                state = self.state_23(c)
            elif 24 == state:
                state = self.state_24(c)
            elif 25 == state:
                state = self.state_25(c)

        
    def state_0(self, c):
        #S0
        #  0:  _/ / .{0} \n
        #  1:  _[_a-zA-Z] [_a-zA-Z0-9]{0}
        #  2:  _[0-9]{1}
        #  3:  _" .{0} "
        #  4:  _+
        #  5:  _-
        #  6:  _*
        #  7:  _/
        #  8:  _=
        #  9:  _= =
        #  10:  _= <
        #  11:  _> =
        #  12:  _<
        #  13:  _>
        #  14:  _;
        #  15:  _(
        #  16:  _)
        #  17:  _{
        #  18:  _}
        #  19:  _,
        #  SHIFT FORWARD
        #    / -> 1
        #    [_a-zA-Z] -> 2
        #    [0-9]{1} -> 3
        #    " -> 4
        #    + -> 5
        #    - -> 6
        #    * -> 7
        #    = -> 8
        #    < -> 9
        #    > -> 10
        #    ; -> 11
        #    ( -> 12
        #    ) -> 13
        #    { -> 14
        #    } -> 15
        #    , -> 16
        #  SHIFT BACKWARD
        #  ACCEPT: -1
        state = 0
        # Shift Forward
        if ('/' == c):
            state = 1
        elif ('_' == c) or ('a' <= c <= 'z') or ('A' <= c <= 'Z'):
            state = 2
        elif ('0' <= c <= '9'):
            state = 3
        elif ('"' == c):
            state = 4
        elif ('+' == c):
            state = 5
        elif ('-' == c):
            state = 6
        elif ('*' == c):
            state = 7
        elif ('=' == c):
            state = 8
        elif ('<' == c):
            state = 9
        elif ('>' == c):
            state = 10
        elif (';' == c):
            state = 11
        elif ('(' == c):
            state = 12
        elif (')' == c):
            state = 13
        elif ('{' == c):
            state = 14
        elif ('}' == c):
            state = 15
        elif (',' == c):
            state = 16
        else:
            self.error_handler()
        return state

    def state_1(self, c):
        #S1
        #  0:  / _/ .{0} \n
        #  7:  /_
        #  SHIFT FORWARD
        #    / -> 17
        #  SHIFT BACKWARD
        #  ACCEPT: 7
        state = 0
        # Shift Forward
        if ('/' == c):
            state = 17
        # Accept
        else:
            yytext = self.get_text()
            yytype = yy_token_names['/']
            self.unget_char()
            self.add_token(yytext, yytype)
        return state

    def state_2(self, c):
        #S2
        #  1:  [_a-zA-Z] _[_a-zA-Z0-9]{0}
        #  SHIFT FORWARD
        #    [_a-zA-Z0-9]{0} -> 18
        #  SHIFT BACKWARD
        #  ACCEPT: -1
        state = 0
        # Shift Forward
        if ('_' == c) or ('a' <= c <= 'z') or ('A' <= c <= 'Z') or ('0' <= c <= '9'):
            state = 18
        # Handle minimum count=0 (?, {0}, {0,M})
        else:
            state = 18
            self.unget_char()
        return state

    def state_3(self, c):
        #S3
        #  2:  [0-9]{1}_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 2
        state = 0
        # Stay in the current state
        if ('0' <= c <= '9'):
            state = 3
        # Accept
        else:
            yytext = self.get_text()

            yytype = NUMBER
        
            self.unget_char()
            self.add_token(yytext, yytype)
        return state

    def state_4(self, c):
        #S4
        #  3:  " _.{0} "
        #  SHIFT FORWARD
        #    .{0} -> 19
        #  SHIFT BACKWARD
        #  ACCEPT: -1
        state = 0
        # Shift Forward
        if ('\n' != c):
            state = 19
        # Handle minimum count=0 (?, {0}, {0,M})
        else:
            state = 19
            self.unget_char()
        return state

    def state_5(self, c):
        #S5
        #  4:  +_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 4
        state = 0
        # Accept
        yytext = self.get_text()
        yytype = yy_token_names['+']
        self.unget_char()
        self.add_token(yytext, yytype)
        return state

    def state_6(self, c):
        #S6
        #  5:  -_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 5
        state = 0
        # Accept
        yytext = self.get_text()
        yytype = yy_token_names['-']
        self.unget_char()
        self.add_token(yytext, yytype)
        return state

    def state_7(self, c):
        #S7
        #  6:  *_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 6
        state = 0
        # Accept
        yytext = self.get_text()
        yytype = yy_token_names['*']
        self.unget_char()
        self.add_token(yytext, yytype)
        return state

    def state_8(self, c):
        #S8
        #  8:  =_
        #  9:  = _=
        #  10:  = _<
        #  SHIFT FORWARD
        #    = -> 20
        #    < -> 21
        #  SHIFT BACKWARD
        #  ACCEPT: 8
        state = 0
        # Shift Forward
        if ('=' == c):
            state = 20
        elif ('<' == c):
            state = 21
        # Accept
        else:
            yytext = self.get_text()
            yytype = yy_token_names['=']
            self.unget_char()
            self.add_token(yytext, yytype)
        return state

    def state_9(self, c):
        #S9
        #  12:  <_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 12
        state = 0
        # Accept
        yytext = self.get_text()
        yytype = yy_token_names['LT']
        self.unget_char()
        self.add_token(yytext, yytype)
        return state

    def state_10(self, c):
        #S10
        #  11:  > _=
        #  13:  >_
        #  SHIFT FORWARD
        #    = -> 22
        #  SHIFT BACKWARD
        #  ACCEPT: 13
        state = 0
        # Shift Forward
        if ('=' == c):
            state = 22
        # Accept
        else:
            yytext = self.get_text()
            yytype = yy_token_names['GT']
            self.unget_char()
            self.add_token(yytext, yytype)
        return state

    def state_11(self, c):
        #S11
        #  14:  ;_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 14
        state = 0
        # Accept
        yytext = self.get_text()
        yytype = yy_token_names[';']
        self.unget_char()
        self.add_token(yytext, yytype)
        return state

    def state_12(self, c):
        #S12
        #  15:  (_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 15
        state = 0
        # Accept
        yytext = self.get_text()
        yytype = yy_token_names['(']
        self.unget_char()
        self.add_token(yytext, yytype)
        return state

    def state_13(self, c):
        #S13
        #  16:  )_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 16
        state = 0
        # Accept
        yytext = self.get_text()
        yytype = yy_token_names[')']
        self.unget_char()
        self.add_token(yytext, yytype)
        return state

    def state_14(self, c):
        #S14
        #  17:  {_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 17
        state = 0
        # Accept
        yytext = self.get_text()
        yytype = yy_token_names['{']
        self.unget_char()
        self.add_token(yytext, yytype)
        return state

    def state_15(self, c):
        #S15
        #  18:  }_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 18
        state = 0
        # Accept
        yytext = self.get_text()
        yytype = yy_token_names['}']
        self.unget_char()
        self.add_token(yytext, yytype)
        return state

    def state_16(self, c):
        #S16
        #  19:  ,_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 19
        state = 0
        # Accept
        yytext = self.get_text()
        yytype = yy_token_names[',']
        self.unget_char()
        self.add_token(yytext, yytype)
        return state

    def state_17(self, c):
        #S17
        #  0:  / / _.{0} \n
        #  SHIFT FORWARD
        #    .{0} -> 23
        #  SHIFT BACKWARD
        #  ACCEPT: -1
        state = 0
        # Shift Forward
        if ('\n' != c):
            state = 23
        # Handle minimum count=0 (?, {0}, {0,M})
        else:
            state = 23
            self.unget_char()
        return state

    def state_18(self, c):
        #S18
        #  1:  [_a-zA-Z] [_a-zA-Z0-9]{0}_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 1
        state = 0
        # Stay in the current state
        if ('_' == c) or ('a' <= c <= 'z') or ('A' <= c <= 'Z') or ('0' <= c <= '9'):
            state = 18
        # Accept
        else:
            yytext = self.get_text()

        
            if yytext == 'char':
                yytype = CHAR
            elif yytext == 'int':
                yytype = INT
            elif yytext == 'float':
                yytype = FLOAT
            elif yytext == 'void':
                yytype = VOID
        
            elif yytext == 'if':
                yytype = IF
            elif yytext == 'else':
                yytype = ELSE
            elif yytext == 'for':
                yytype = FOR
            elif yytext == 'return':
                yytype = RETURN
            else:
                yytype = ID
        
            self.unget_char()
            self.add_token(yytext, yytype)
        return state

    def state_19(self, c):
        #S19
        #  3:  " .{0} _"
        #  SHIFT FORWARD
        #    " -> 24
        #  SHIFT BACKWARD
        #  ACCEPT: -1
        state = 0
        # Shift Forward
        if ('"' == c):
            state = 24
        # Stay in the current state
        elif ('\n' != c):
            state = 19
        else:
            self.error_handler()
        return state

    def state_20(self, c):
        #S20
        #  9:  = =_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 9
        state = 0
        # Accept
        yytext = self.get_text()
        yytype = yy_token_names['EQU']
        self.unget_char()
        self.add_token(yytext, yytype)
        return state

    def state_21(self, c):
        #S21
        #  10:  = <_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 10
        state = 0
        # Accept
        yytext = self.get_text()
        yytype = yy_token_names['LTE']
        self.unget_char()
        self.add_token(yytext, yytype)
        return state

    def state_22(self, c):
        #S22
        #  11:  > =_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 11
        state = 0
        # Accept
        yytext = self.get_text()
        yytype = yy_token_names['GTE']
        self.unget_char()
        self.add_token(yytext, yytype)
        return state

    def state_23(self, c):
        #S23
        #  0:  / / .{0} _\n
        #  SHIFT FORWARD
        #    \n -> 25
        #  SHIFT BACKWARD
        #  ACCEPT: -1
        state = 0
        # Shift Forward
        if ('\n' == c):
            state = 25
        # Stay in the current state
        elif ('\n' != c):
            state = 23
        else:
            self.error_handler()
        return state

    def state_24(self, c):
        #S24
        #  3:  " .{0} "_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 3
        state = 0
        # Accept
        yytext = self.get_text()

        yytype = STRING
        #yytext = yytext[1:-1]
    
        self.unget_char()
        self.add_token(yytext, yytype)
        return state

    def state_25(self, c):
        #S25
        #  0:  / / .{0} \n_
        #  SHIFT FORWARD
        #  SHIFT BACKWARD
        #  ACCEPT: 0
        state = 0
        # Accept
        yytext = self.get_text()

        yytype = COMMENT
    
        self.unget_char()
        self.add_token(yytext, yytype)
        return state




