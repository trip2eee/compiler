# Lexer Generator

## 1. Lex Syntax

## 2. Lex file parser

```mermaid
graph LR

S0["S0 - start"]
S1["S1"]
S2["S2 - comment"]
S10["S10 - definitions"]
S11["S11"]
S1["S1 - rules"]
S2["21 - rule regx"]
S3["S3"]
S4["S4 - subroutine"]
S30["S30"]
S31["S31 - user subroutines"]

S8["S8 - comment"]

S0 -- % --> S1
S0 -- # --> S2
S2 -- \n --> S0
S1 -- "{" --> S10
S10 -- % --> S11
S11 -- other --> S10
S11 -- "}" --> S0

S1 -- % --> S1

S1 -- other --> S2

S2 -- "SP" --> S3
S3 -- ";" --> S1
S3 -- "{" --> S4
S4 -- "}" --> S1
S4 -- other --> S4

S1 -- # --> S8
S8 -- "\n" --> S1

S1 -- % --> S30
S30 -- % --> S31
S30 -- other --> S1
```

## 2. Regx Parser
A limited regular expression parser

| Symbol | Description |
|-|-|
|[ ] | Matched a single character that is contained within the brackets. |
| {m} | Matched the preceding element at least m. |
| {m, n} | Matches the preceding element at least m and not more than n times. |
| ? | Matches the preceding element zero or one time. |
| + | Matches the preceding element one or more times. |
| * | Matches the preceding element zero or more times. |
|a-z| Specifies a range which matches any letter from a to z|

### 2.1 Supported Regular Expression

```mermaid
graph LR

S0["S0"]
S1["S1"]
S2["S2"]
S3["S3 - (esc)"]
S4["error"]
S5["S5"]
S6["S6 (a-z)"]

S0 -- other --> S0

S0 -- "[" --> S1
S1 --"]" --> S2
S1 -- "\" --> S3

S3 --"d, D, w, W, s, S, ., n, t"--> S1
S3 -- other --> S4

S2 -- "+, *, ?" --> S0
S2 -- other --> S0
S2 -- "{" --> S8
S8 -- "digit" --> S8
S8 -- "}" --> S0
S8 -- "," --> S5
S5 -- "digit" --> S5
S5 -- "}" --> S0

S1 -- char --> S1
S1 -- "-" --> S6
S6 -- char --> S1
S6 -- "]" --> S2


```
