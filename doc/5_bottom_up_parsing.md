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

A bottom-up parse of the string "( )" using this grammar is given in Table 5.1.

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


#### Example 5.2

Consider the following augmented grammar for rudimentary arithmetic expressions (no parentheses and one operation):

$E' \rightarrow E$

$E \rightarrow E + n \ \mid \ n$

A bottom-up parse of the string $n + n$ using this grammar is given in Table 5.2.

Table 5.2 Parsing actions of a bottom-up parser for the grammar of Example 5.2

|#|Parsing Stack|Input|Action|
|-|-|-|-|
|1| $| $n+n$ $| shift|
|2| $ $n$| $+n$ $| reduce $E \rightarrow n$|
|3| $ $E$| $+n$ $| shift |
|4| $ $E+$| $n$ $| shift |
|5| $ $E+n$| $| reduce $E \rightarrow E + n$ |
|6| $ $E$| $| reduce $E' \rightarrow E$ |
|7| $ $E'$| $| accept |

General observations on characteristics of intermediate stages of the bottom-up parse.

A shift-reduce parser traces out a rightmost derivation of the input string, but the steps of the derivation occur in reverse order (*right sentential form*).
$$ S' \Rightarrow S \Rightarrow ( \ S \ ) \ S \Rightarrow ( \ S \ ) \Rightarrow ( \ )$$
$$ E' \Rightarrow E \Rightarrow E + n \Rightarrow n+n$$
viable prefix: the sequence of symbols on the parsing stack.

A shift-reduce parser will shift terminals from the input to the stack until it is possible to perform a reduction to obtain the next right sentential form. This will occur when the string of symbols on the top of the stack matches the right-hand side of the production that is used in the next reduction. 

This string, together with the position in the right sentential form where it occurs, and the production used to reducte it is called the *handle* of the right sentential form.

Determining the next handle in a parse is the main task of a shift-reduce parser.

## 5.2 Finite Automata of LR(0) Items And LR(0) Parsing

### 5.2.1 LR(0) Items
An LR(0) item (or just item for short) of a context-free grammar is a production choice with a distinguished position in its right-hand side. Thus, if $A \rightarrow \alpha$ is a production choice, and if $\beta$ and $\gamma$ are any two strings of symbols (including empty string $\epsilon$) such that $\beta \gamma = \alpha$, then $A \rightarrow \beta . \gamma$ is an LR(0) item. These are called LR(0) items because they contain no explicit reference to lookahead.

#### Dot symbol (.)
$A \rightarrow BCD$

LR(0) item: Production rules that have dot (.) on the right.

$A \rightarrow .BCD$

$A \rightarrow B.CD$ : $B$ is already seen. $CD$ is string to be read.

$A \rightarrow BC.D$

$A \rightarrow BCD.$ : $BCD$ is already seen. Now we can reduce $BCD$ to $A$.

#### Example 5.3
Consider the grammar of Example 5.1:

$S' \rightarrow S$

$S \rightarrow ( \ S \ ) \ S \ \mid \ \epsilon$

This grammar has three production choices and eight items:

1. $S' \rightarrow .S$
2. $S' \rightarrow S.$
3. $S \rightarrow .(S)S$
4. $S \rightarrow (.S)S$
5. $S \rightarrow (S.)S$
6. $S \rightarrow (S).S$
7. $S \rightarrow (S)S.$
8. $S \rightarrow .$



The idea behind the concept of an item
- Item $A \rightarrow \beta . \gamma$ constructed from $A \rightarrow \alpha$ means that $\beta$ has already been seen and that it may be possible to derive the next input tokens from $\gamma$.
- In terms of parsing stack, this means that $\beta$ must appear at the top of the stack.
- An itme $A \rightarrow .\alpha$ means that we may be about to recognize an $A$ by using the grammar rule choice $A \rightarrow \alpha$ (*initial items*).
- An item $A \rightarrow \alpha.$ means that $\alpha$ now resides on the top of the parsing stack and may be the handle, if $A \rightarrow \alpha$ is to be used for the next reduction (*complete items*).

### 5.2.2 Finite Automata of Items
