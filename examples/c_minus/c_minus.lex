# C-- Lexer
%{

from cmm_parser_table import *


%}

%%


'\/\/(.*)\n' {
    yytype = COMMENT
}

'[_a-zA-Z][_a-zA-Z0-9]*' {

    if yytext == 'if':
        yytype = IF
    elif yytext == 'else':
        yytype = ELSE
    elif yytext == 'for':
        yytype = FOR
    else:
        yytype = ID
}

'[0-9]+' {
    yytype = NUMBER
}

'\+'
'\-'
'\*'
'\/'
'=' 
'==' EQU
'=<' LTE
'>=' GTE
'<'  LT
'>'  GT
';'
'\('
'\)'
'\{'
'\}'

%%



