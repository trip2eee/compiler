# YACC - Parser Generator

## Terminologies

### First sets
Set of symbols that can come first in each production rule.

1. If $X$ is a terminal, then $First(X) = \lbrace X \rbrace$.

2. If $X$ is a nonterminal, then for each production choice $X \rightarrow X_1 X_2 ... X_n$, $First(x)$ contains $First(X_1) - \lbrace \epsilon \rbrace$.


### Follow sets

Set of symbols that can follow a nonterminal.

1. If $X$ is the start symbol, then $ is in $Follow(X)$

2. If there is a production $X \rightarrow X_1 X_2 X_3$, then $First(X_3) - \lbrace \epsilon \rbrace$ is in $Follow (X_2)$.

3. If there is a production $X \rightarrow X_1 X_2 X_3$ such that $\epsilon$ is in $First(X_3)$, then $Follow(X_2)$ contains $Follow(X)$.


### LR(1)
- L indicates that the input is processed from left to right
- R indicates that a rightmost derivation is produced
- (1) indicates that no symbol of lookahead is used


### LR(0) items
A production choice with a distinguished position in its right-hand side.

### LALR parser
Lookahead LR parsing

### Closure ($\epsilon$-Closure)

The closure of a single state $s$ is the set of states reachable by a series of zero or more $\epsilon$-transitions.

Items with mark=0 e.g. $A \rightarrow .X_1 X_2$

If $A \rightarrow X_1 .X_2$ is in closure and production rule for $X_2$ such as $X_2 \rightarrow a$ exists, $X_2 \rightarrow a$ is also added to the closure.

## Class

### ParserGenerator
