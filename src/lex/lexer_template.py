%FILE_COMMENT%

# Definitions
%DEFINITIONS%

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
        print('{} - {} in {}:{}'.format(yytext, yytype, self.idx_start_line+1, self.idx_start_col+1))
        symbol = Symbol()
        symbol.type = yytype
        symbol.text = yytext
        symbol.idx_line = self.idx_start_line+1
        symbol.idx_col = self.idx_start_col+1
        self.list_tokens.append(symbol)

    def error_handler(self):
        text = self.code[self.idx_start:self.idx_char]
        if text != '\n' and text != '\t' and text != ' ' and text != '':
            print("Unexpected Character: '{}' in {}:{}".format(text, self.idx_line+1, self.idx_col+1))

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

%SCAN_BODY%
        
%STATE_FUNCTIONS%


