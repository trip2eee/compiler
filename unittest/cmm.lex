%%
# Rules
# 'STRING' ACTION

COMMENT '\/\/(.*)\n' {

}

ID '[_a-zA-Z][_a-zA-Z0-9]*' {
    print(yytext)
}

IF    'if'
FOR   'for'
WHILE 'while'

PLUS   '+'
MINUS  '-'
ASSIGN '='
EQUAL  '=='
LTE    '=<'
GTE    '>='
LT     '<'
GT     '>'
END    '$'

%%

