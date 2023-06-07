# Lex rule definition
%
# user code
%

%%

# semicolon
; {
    yylval.type = SEMI
}

[0-9]*[.]?[0-9]+[fF]? { 
    yylval.type = NUMBER
}

[a-zA-Z_]*[a-zA-Z0-9_]  {
    yylval.type = ID
}

+ {
    yylval.type = PLUS
}

- {
    yylval.type = MINUS
}

= {
    yylval.type = ASSIGN
}

== {
    yylval.type = EQ
}

if {
    yylval.type = IF
}

for {
    yylval.type = FOR
}


%%

