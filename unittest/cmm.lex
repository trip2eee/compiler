%%
# Rules
# 'STRING' SYMBOL
# 'STRING' { ACTION }

'\/\/(.*)\n' {
    yytype = COMMENT
}

'[_a-zA-Z][_a-zA-Z0-9]*' {
    print(yytext)

    if yytext == 'if':
        yytype = IF
    elif yytext == 'for':
        yytype = FOR
    else:
        yytype = ID
}

'\+'  PLUS
'\-'  MINUS
'='  ASSIGN
'==' EQUAL
'=<' LTE
'>=' GTE
'<'  LT
'>'  GT

%%
