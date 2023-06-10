# Calc
## 1. Grammar
$exp \rightarrow exp \ addop \ term \ \mid \ term$

$addop \rightarrow + \ \mid \ -$

$term \rightarrow term \ mulop \ factor \ \mid \ factor$

$mulop \rightarrow * \ \mid \ /$

$factor \rightarrow  ( \ exp \ ) \ \mid \ number \ \mid addop \ factor$

This grammar is defined in [calc.gram](calc.gram)

## 2. Parser Generation

[generate_calc.py](generate_calc.py) generates calc parser.

## 3. Lexical Analysis
Currently a handwritten lexer code [calc_lexer.py](examples/calc/calc_lexer.py) is being used. This code will be replaced by automatically generated lexer.

## 4. Parser Execution
The main module of the calculator is [calc.py](calc.py). The resulting parser has been verified by unit test implemented in [ut_calc.py](ut_calc.py).