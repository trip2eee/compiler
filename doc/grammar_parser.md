# Grammar File Parser
## 1. Grammar File Syntax

```python
# definitions

%{
# external dependencies in a language to be used for implementation.
%}

%%
# rules

NON_TERMINAL1 : 
    NUMBER PLUS NUMBER {
        # action to be done when the symbols are reduced to NON_TERMINAL1
        # $$ : return value
        # $1 : 1st symbol
        # $3 : 3rd symbol
        $$ = $1 + $3
    }
    |   # or operator
    NUMBER MINUS NUMBER {
        # action for the rule
        $$ = $1 - $3
    }
    ;   # The definition of a rule shall end with ';'

NON_TERMINAL2 : 
    SYMBOL1 {
        # action to be done when symbol1 is read
    }
    SYMBOL2 {
        # action to be done when symbols are reduced to NON_TERMINAL2
    }
    ;
%%
# auxiliary routines

```

The left symbol of the first rule is considered as a start symbol.

DFA of the Grammar Lexer

```mermaid
graph LR

IDLE["IDLE"]
SYMBOL["SYMBOL"]
SYMBOL2["SYMBOL2"]
ACTION["ACTION"]
COMMENT["COMMENT"]

IDLE -- "[_a-zA-Z]" --> SYMBOL
SYMBOL -- "[_a-zA-Z0-9]" --> SYMBOL
SYMBOL -- other --> IDLE

IDLE -- "{" --> ACTION
ACTION -- "}" --> IDLE

IDLE -- ":" --> IDLE
IDLE -- "|" --> IDLE
IDLE -- ";" --> IDLE
IDLE -- "#" --> COMMENT
COMMENT -- "\n" --> IDLE

IDLE -- "=_+-*/()$" --> SYMBOL2
SYMBOL2 --> IDLE
```

DFA of the Grammar Parser
```mermaid
graph LR

IDLE["IDLE"]
LEFT["LEFT"]
RIGHT["RIGHT"]

IDLE -- "symbol" --> LEFT
LEFT -- ":" --> RIGHT

RIGHT -- "symbol" --> RIGHT
RIGHT -- "action" --> RIGHT

RIGHT -- "|" --> RIGHT

RIGHT -- ";" --> IDLE


```