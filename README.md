# Compiler

## 1. Introduction
The goal of this project is as follows
1. To develop parser generator similar to YACC(Yet Another Compiler Compiler) based on LALR(1) method in python (*DONE*).
2. To develop lexical analyzer similar to lex in python.
3. To develop an interpreter to execute a script language.
4. To develop a compiler to make executable file.

## 2. Current Status

1. Handwritten C-- lexer [scanner.py](src/scanner.py) and parser based on Recurrent-Descent [rd_parser.py](src/rd_parser.py) have been implemented. Due to the limitation of applied method, the codes are not going to be updated.
2. Parser generator has been implemented.
   - Parser code: [parser_generator.py](src/parser_generator.py)

3. Parser generator has been tested for simple calculator ([examples/calc/](examples/calc)).
    1. run generate_calc.py to generate parser from [calc.gram](examples/calc/calc.gram)
    2. [calc_parser_table.py](examples/calc/calc_parser_table.py) and [calc_parser.py](examples/calc/calc_parser.py) are generated.
    3. Currently handwritten lexer code is being used since lexer generator is not implemented yet.
    4. run units test by executing ut_calc.py

4. Lexer generator based on RegEx is under development.

## 3. Usages
#### 3.1.1 Grammar File Format

```python
# definitions

%{
# definitions of class, structure, variables to be copied to parser code.
class Symbol:
    def __init__(self):
        self.type = None
        self.value = None
%}

%%
# rules

NON_TERMINAL1 : 
    NUMBER PLUS NUMBER {
        # action to be done when the symbols are reduced to NON_TERMINAL1
        # $$ : return value
        # $1 : 1st symbol NUMBER
        # $2 : 2nd symbol PLUS
        # $3 : 3rd symbol NUMBER
        $$.value = $1.value + $3.value
    }
    |   # or operator
    NUMBER MINUS NUMBER {
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
## 4. Examples
### 4.1 Calculator
#### 4.1.1 Grammar
$exp \rightarrow exp \ addop \ term \ \mid \ term$

$addop \rightarrow + \ \mid \ -$

$term \rightarrow term \ mulop \ factor \ \mid \ addop \ term \ \mid \ factor$

$mulop \rightarrow * \ \mid \ /$

$factor \rightarrow  ( \ exp \ ) \ \mid \ number$

```python
%{
class Symbol:
    def __init__(self):
        self.type = None
        self.value = None
%}

%%
exp : 
exp addop term {
    if $2.value == '+':
        $$.value = $1.value + $3.value
    else:
        $$.value = $1.value - $3.value
}|
term;

addop : + | -;

term :
term {
    print('term: ' + str($1.value)) # for embedded action test. it's not necessary
} mulop factor {
    if $2.value == '*':
        $$.value = $1.value * $3.value
    else:
        $$.value = $1.value / $3.value
}|
addop term {
    if $1.value == '+':
        $$.value = $2.value
    else:
        $$.value = -1.0 * $2.value
} |
factor;

mulop : * | /;

factor : 
( exp ) {
    $$ = $2
} |
number;

%%

```
#### 4.1.2 Parser Generation
```python
import sys
sys.path += '../../'
from src.parser_generator import ParserGenerator

gen = ParserGenerator()
# generate a parser from a grammar file.
gen.generate_parser('examples/calc/calc.gram')
# export the parser in python code.
gen.export('examples/calc/calc_parser.py')

```
#### 4.1.3 Lexical Analysis
Currently a handwritten lexer code [calc_lexer.py](examples/calc/calc_lexer.py) is being used. This code will be replaced by automatically generated lexer.
#### 4.1.4 Parser Execution
```python
from examples.calc.calc_parser_table import *
from examples.calc.calc_parser import parse
from examples.calc.calc_lexer import CalcLexer

class Calc:
    def __init__(self):
        self.list_symbol = []
        self.lexer = CalcLexer()
    
    def compute(self, expr):
        list_symbol = self.lexer.lexer(expr)
        result = parse(list_symbol)
        
        return result
```

# Reference

1. Louden, K. C. (1997). Compiler Construction: Principles and Practice. Course Technology.

2. 박두순 (2020). 컴파일러의 이해. 한빛출판사