# Compiler

## 1. Introduction
The goal of this project is as follows
1. To develop parser generator similar to YACC(Yet Another Compiler Compiler) based on LALR(1) method in python (*DONE*).
2. To develop lexical analyzer similar to lex in python.
3. To develop an interpreter to execute C-- language.

## 2. Current Status

1. Handwritten C-- lexer [scanner.py](src/scanner.py) and parser based on Recurrent-Descent [rd_parser.py](src/rd_parser.py) have been implemented. Due to the limitation of applied method, the codes are not going to be updated.
2. Parser generator has been implemented.
   - Parser code: [src/yacc](src/yacc)

3. Parser generator has been tested for simple calculator ([examples/calc/](examples/calc)).
    1. run generate_calc.py to generate parser from [calc.gram](examples/calc/calc.gram)
    2. [calc_parser_table.py](examples/calc/calc_parser_table.py) and [calc_parser.py](examples/calc/calc_parser.py) are generated.
    3. In this example, handwritten lexer code is used since lexer generator was not implemented in this moment.
    4. run units test by executing ut_calc.py

4. Lexer generator based on RegEx is under development [src/lex](src/lex) (*DONE*).

5. C-- interpreter (code generation & runtime environment) [examples/c_minus](examples/c_minus) (*DONE*).

## 3. Usages
#### 3.1 Grammar File Format

```python
# definitions

%{
# definitions of class, structure, variables to be copied to parser code.
class TreeNode:
    def __init__(self):
        self.type = None
        self.value = None
%}

%%
# rules

NON_TERMINAL1 : 
    NUMBER '+' NUMBER {
        # action to be done when the symbols are reduced to NON_TERMINAL1
        # $$ : return value
        # $1 : 1st symbol NUMBER
        # $2 : 2nd symbol +
        # $3 : 3rd symbol NUMBER
        $$.value = $1.value + $3.value
    }
    |   # or operator
    NUMBER '-' NUMBER {
        # action for the rule
        $$.value = $1.value - $3.value
    }
    ;   # The definition of a rule shall end with ';'

NON_TERMINAL2 : 
    SYMBOL1 {
        # Embedded Action to be done when SYMBOL1 is read or rules are reduced to SYMBOL1.
    }
    SYMBOL2 {
        # Action to be done when rules are reduced to NON_TERMINAL2
    }
    ;
%%
# auxiliary routines
```
### 3.2 Lex File Format
```python
#definitions

%{

%}

# lexical rules
# 'RegEx' { action }
'\/\/(.*)\n' {
    yytype = COMMENT #yytype : The type of this token.
}

'[_a-zA-Z][_a-zA-Z0-9]*' {
    # yytext : The string matched by the regular expression.
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

# if action is not specified, the ID of the symbol is searched in yy_token_names.
# yy_token_names: token dictionary generated by yacc/parser_generator.py
'\+'
'\-'
'\*'
'\/'
'=' 
'=='
'=<'
'>='
'<'
'>'
';'


%%
# auxiliary routines

```

## 4. Examples
### 4.1 Calculator

Calculator example is implemented in [examples/calc](examples/calc).

### 4.2 Regular Expression

Regular Expression example is implemented in [examples/regex](examples/regex).

### 4.3 C-- Language

An interpreter language with C-like syntax. In this example the following codes are implemented in [examples/c_minus](examples/c_minus).

- C-- language parser (generated by [src/yacc](src/yacc))
- C-- language lexer (generated by [src/lex](src/lex))
- C-- language compiler
- C-- language runtime environment


# Reference

1. Louden, K. C. (1997). Compiler Construction: Principles and Practice. Course Technology.

2. 박두순 (2020). 컴파일러의 이해. 한빛출판사

