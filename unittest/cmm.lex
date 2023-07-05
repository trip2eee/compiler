# Definitions
%{
COMMENT = 1
ID = 2
ASSIGN = 3
IF = 4
FOR = 5
PLUS = 6
MINUS = 7
LTE = 8
GTE = 9
EQUAL = 10
LT = 11
GT = 12
MUL = 13
DIV = 14
%}

%%
# Rules
# 'STRING' SYMBOL
# 'STRING' { ACTION }

#'\/\/(.*)\n' {
#    yytype = COMMENT
#}

'\/(\*(.|\n)*\*\/)|(\/.*\n)' {
    yytype = COMMENT
}

'[_a-zA-Z][_a-zA-Z0-9]*' {

    if yytext == 'if':
        yytype = IF
    elif yytext == 'for':
        yytype = FOR
    else:
        yytype = ID
}

'\+'  PLUS
'\-'  MINUS
'\*'  MUL
'\/'  DIV
'='  ASSIGN
'==' EQUAL
'=<' LTE
'>=' GTE
'<'  LT
'>'  GT

%%
