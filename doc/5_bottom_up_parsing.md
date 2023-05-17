# 5. Bottom-Up Parsing
The most general bottom-up algorithm is called LR(1) parsing.
- L indicates the input is processed from left to right.
- R indicates that a rightmost derivation is produced.
- (1) indicates that one symbol of lookahead is used.

LR(0) parsing - No lookahead is consulted in making parsing decisions.

SLR(1) - An improvement of LR(0) parsing (for simple LR(1) parsing).

LALR(1) parsing - A method that is slightly more powerful than SLR(1) parsing but less complex than general LR(1) parsing (for lookahead LR(1) parsing).

Bottom-up parsing algorithms are in general more powerful than top-down methods. For example, left recursion is not a problem in bottom-up parsing. Not unexpectedly, the constructions involved in these algorithms are also more complex. Bottom-up methods are really too complex for hand coding, but are well suited for parser generators like Yacc.

## 5.1 Overview of Bottom-Up Parsing
A bottom-up parser uses an explicit stack to perfrom a parse, similar to a nonrecursive top-down parser. The parsing stack will contain both tokens and nonterminals, and also some extra state information. The stack is empty at the beginning of a bottom-up parse and will contain the start symbol at the end of a successful parse.

A bottom-up parser has two possible actions (besides "accept")
1. Shift a terminal from the front of the input to the top of the stack.
2. Reduce a string $\alpha$ at the top of the stack to nonterminal $A$, given the BNF choice $A \rightarrow \alpha$.

A bottom-up parser is thus sometimes called a *shift-reduce* parser. One further feature of botom-up parsers is that grammars are always augmented with a new start symbol. This means that if $S$ is the start symbol, a new start symbol $S'$ is added to the grammar, with a single unit production to the previous start symbol: $S' \rightarrow S$.


#### Example 5.1
Consider the following augmented grammar for balanced parentheses:

$S' \rightarrow S$

$S \rightarrow ( \ S \ ) \ S \ \mid \ \epsilon$

A bottom-up parse of the string () using this grammar is given in Table 5.1.

Table 5.1 Parsing actions of a bottom-up parser for the grammar of Example 5.1
|#|Parsing stack|Input|Action|
|-|-|-|-|
|1|\$ | $( )$     $| shift|
|2|\$ $($ | $)$ $| reduce $S \rightarrow \epsilon$|
|3|\$ $( \ S \  $| $)$ $| shift |
|4|\$ $( \ S \ )$| $| reduce $S \rightarrow \epsilon$|
|5|\$ $( \ S \ ) \ S$ | $| reduce $S \rightarrow ( \ S \ ) \ S$|
|6|\$ $S$ | $| reduce $S' \rightarrow S$|
|7|\$ $S'$ | $| accept|


