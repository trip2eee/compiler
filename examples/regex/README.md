# RegEx Parser

## 1. Introduction
The goal is to implement somewhat limited Regular Expression parser to be used in automaic lexer generation.

| Symbol | Description |
|-|-|
|[ ] | Matches a character in a set of characters, which is a class. x-y denotes character from x to y|
| . | Mathces all characters except new line \n. |
| \d | Mathces all digits. Equivalent to [0-9]|
| ? | Matches the preceding element zero or one time. |
| + | Matches the preceding element one or more times. |
| * | Matches the preceding element zero or more times. |
|( ) | Expression in ( ) is considered as a group. |
| \| | OR operator. |
| {m} | NOT IMPLEMENTED! ~~Matched the preceding element at least m.~~ |
| {m, n} | NOT IMPLEMENTED! ~~Matches the preceding element at least m and not more than n times.~~ |


## 2. Lexer
Since automatic lexer generation is not implemented yet, lexer must be written manually.

- 0-9, a-z, A-Z,- : CHAR
- \D, \d, ... : escape characters
- '[' : LBRACKET
- ']' : RBRACKET
- '{' : LBRACE
- '}' : RBRACE
- '(' : LPAREN
- ')' : RPAREN
- '+' : PLUS
- '*' : TIMES
- '?' : QUES

TODO: To implement recognition of \{ and \} as lexical symbols { and }.

## 3. Parser

Floating point number in C/C++ style can be expressed in regular expression as follows
```python
"[+-]?  (    \d+([.]\d*)?([eE][+-]?\d+)?    |    [.]\d+([eE][+-]?\d+)?    )"
```
For better readability, some strings are spaced.


$exp \rightarrow expsub \ exp \ \mid \ subexp \ \mid \ exp \ or \ exp$

$subexp \rightarrow class \ \mid char \ \mid group \ | \ subexp \ count$

$group \rightarrow ( \ exp \ )$

$class \rightarrow [ \ term \ ]$

$term \rightarrow term \ factor \ \mid factor \ \mid term \ -$

$factor \rightarrow char \ \mid \ char \ - \ char \ \mid \ esc$

$count \rightarrow + \ \mid \ * \ \mid \ ?$

esc denotes escape character.

### 3.1 Attributes

| Symbol | Child | Next |
|-|-|-|
| CLASS | List of character value or range | Next symbol |
| GROUP | List of subexp | Next symbol |





