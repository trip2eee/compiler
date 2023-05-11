# 4. Top-Down Parsing
A top-down parsing algorithm parses an input string of tokens by tracing out the steps in a leftmost derivation. 

Top-down parsers comes in two forms.

- Backtracing parsers - More powerful than predictive parsers, much slower, requiring exponential time in general. Therefore, they are unsuitable for practical compilers.

- Predictive parsers - attempts to predict the next construction in the input string using one or more lookahead tokens. 
   - Recursive-descent parsing - versatile and most suitable method for a handwritten parser.
   - LL(1) parsing - no longer often used in practice. Prelude to the more powerful (but also more complex) bottom-up algorithms. 
    
      1st L: process input from left to right

      2nd L: leftmost derivation

      (1): It uses only one symbol of input to predict the direction of the parse.

  - Both recursive-descent parsing and LL(1) parsing require in general the computation of lookahead sets that are called First and Follow sets.

## 4.1 Top-Down Parsing by Recursive-Descent
  
Example: Consider the expression grammar

$exp \ \rightarrow \ exp \ addop \ term \mid \ term$

$addop \ \rightarrow \ + \ \mid \ -$

$term \ \rightarrow \ term \ mulop \ term \mid factor$

$mulop \ \rightarrow \ *$

$factor \ \rightarrow \ (\ exp \ ) \mid number$

and consider the grammar rule for a factor. A recursive-descent proceduer that recognizes a factor can be written in pseudocode as follows:

```python
def factor(token):
    if token == '(':
        match('(')        
        exp()
        match(')')
    elif token == number:
        match(number)
    else:
        error # print error message and exit.
    

def match(expectedToken):
    if token == expectedToken:
        get_next_token()
    else:
        error # print error message and exit
```
In the above code, exp() precedure will call term(), term() will call factor(), factor() will call exp().
So all these procedures must be able to call each other. Unfortunately, writing recursive-descent procedures for the remaining rules in the expression grammar is not as easy as for factor and requires the use of EBNF.

### 4.1.2 Repetition and Choice: Using EBNF
Consider as a second example the simplified grammar rule for an if-statement.

$$ 
\begin{split}
if\text-stmt \rightarrow & if \ (\ exp\ ) \ statement  \\
& if \ (\ exp\ ) \ statement \ else \ statement \\
\end{split}
$$

This can be translated into the procedure

```python
def ifstmt:
    match('if')
    match('(')
    exp()
    match(')')
    statement()

    if token == 'else':
        match('else')
        statement()
```

In this example, we could not immediately distinguish the two choices on the right-hand side of the grammar rule (they both start with the token if). Instead, we must put off the decision on whether to recognize the optional else-part until we see the token 'else' in the input. Tuhs, the code for the if-statement corresponds more to the EBNF

$if\text-stmt \rightarrow if \ ( \ exp \ ) \ statement \ [\  else \ statement \ ]$


Solution to the first example is to use EBNF rule. The curly brackets {} expresses repetition.

$exp \ \rightarrow \ term \ \lbrace \ addop \ term \rbrace$

$term \ \rightarrow \ factor \ \lbrace \ mulop \ factor \ \rbrace$

$addop \ \rightarrow \ + \ \mid \ -$

$mulop \ \rightarrow \ *$

$factor \ \rightarrow \ (\ exp \ ) \mid number$

```python
def exp():
    term()
    while token == '+' or token == '-':
        match('+' or '-')
        term()

def term():
    factor()
    while token == '*':
        match('*')
        factor()
```

Python implementation of RD parser: src/rd_parser.py

### 4.1.3 Further Decision Problems
1. It may be difficult to convert a grammar originally written in BNF into EBNF form.
2. When formulating a test to distinguish two or more grammar rule options $A \rightarrow \alpha \ \mid \ \beta \ \mid \ \cdots$, it may be difficult to decide when to use the choice $A \rightarrow \alpha$ and when to use the choice $A \rightarrow \beta$, if both $\alpha$ and $\beta$ begin with nonterminals.
  
   - First sets of $\alpha$ and $\beta$: The set of tokens that can legally begin each string

3. In writing code for an $\epsilon$-production $A \rightarrow \epsilon$ it may be necessary to know what tokens can legally come after the nonterminal $A$.
   - Follow set of $A$: Set of tokens that can legally come after the nonterminal $A$.

## 4.2 LL(1) Parsing
### 4.2.1 The Basic Method of LL(1) Parsing

LL(1) parsing uses an explicit stack rather than recursive calls.

The following table shows the actions of a top-down parser given grammar $S \rightarrow ( \ S \ ) \ S \ \mid \ \epsilon$


#### Table 4.1 Parsing actions of a top-down parser
- Parsing Stack
  - Left:Bottom of Stack($)
  - Right:Top of Stack

- Input
  - Input symbols are listed from left to right. $ represents end of the input.

- Action
  - Shorthand description of the action taken by the parser

| Step | Parsing Stack | Input | Action |
|-|-|-|-|
| 1 | $ S      | ( ) $ | $S \rightarrow ( \ S \ ) \ S$|
| 2 | $ S ) S (| ( ) $ | match |
| 3 | $ S ) S  |   ) $ | $S \rightarrow \epsilon$ |
| 4 | $ S )    |   ) $ | match|
| 5 | $ S      |     $ | $S \rightarrow \epsilon$|
| 6 | $        |     $ | accept|

A top-down parser begins by pushing the start symbol onto the stack. It accepts an input string if, after a series of actions, the stack and the input become empty.

Basic actions in a top-down parser

 1. Replace a nonterminal $A$ at the top of the stack by a string $\alpha$ using the grammar rule choice $A \rightarrow \alpha$. This action could be called generate; left-hand side must be the nonterminal currently at the top of the stack.
 2. Match a token on top of the stack with the next input token.

### 4.2.2 The LL(1) Parsing Table and Algorithm

- When a nonterminal $A$ is at the top of the parsing stack: A decision must be makde, based on the current input token (the lookahead).

- When a token is at the top of the stack: No decision is neccessary since it is either the same as the current input token (a match occurs), or it isn't (an error occurs).

LL(1) Parsing Table: We can express the choices that are possible by constructing an LL(1) parsing table, which is a two-dimensional array indexed by nonterminals and terminals $M[N, T]$ containing production choices to use at the appropriate parsing step.

$\$$ : End of input

$M[N, T]$ : LL(1) Parsing Table

$N$: The set of nonterminals

$T$: The set of terminals or tokens.


We assume that the table $M[N, T]$ starts out with all its entries empty. Any entries that remain empty after the construction represent potential errors that may occur during a parse.

1. If $A \rightarrow \alpha$ is a production choice, and there is a derivation $\alpha \Rightarrow * \ a \ \beta$, where $a$ is a token, then add $A \rightarrow \alpha$ to the table entry $M[A, a]$.

2. If $A \rightarrow \alpha$ is a production choice, and there are derivations $\alpha \Rightarrow * \ \epsilon$ and $S \ \$ \Rightarrow \beta \ A \ a \ \gamma$, where $S$ is the start symbol and $a$ is a token (or $, which is end of input), then add $A \rightarrow \alpha$ to the table entry $M[A, a]$.


The symbols $\Rightarrow *$ stand for a derivation consisting of a sequence of replacements

$empty \rightarrow \epsilon$

#### Example
There is one nonterminal ($S$), three tokens (, ), and $, and two production choices.

- Rule 1

Nonempty production: $S \rightarrow ( \ S \ ) \ S$, every string derived from $S$ must be either empty or begin with (, and this production choice is added to the entry $M[S, (]$.

$S \Rightarrow ( \ S \ ) \ S$

- Rule 2

$\alpha = \epsilon$, $\beta = ($, $A = S$, $a = )$, and $\gamma = S \ \$$, so $S \rightarrow \epsilon$ is added to $M[S, )]$.

| $M[N,T]$ | ( | ) | $ |
|-|-|-|-|
| $S$ | $S \rightarrow ( \ S \ ) \ S$| $S \rightarrow \epsilon$| $S \rightarrow \epsilon$ |

#### Definition
A grammar is an LL(1) grammar if the associated LL(1) parsing table has at most one production in each table entry.

#### Example

$stmt \rightarrow if\text-stmt \ \mid \ other$

$if\text-stmt \rightarrow if \ ( \ exp \ ) \ stmt \ else\text-part$

$else\text-part \rightarrow else \ stmt \ \mid \ \epsilon$

$exp \rightarrow 0 \ \mid \ 1$

#### Table 4.2 LL(1) parsing table for (ambiguous) if-statements
| $M[N,T]$ | if | other | else | 0 | 1 | $ |
|-|-|-|-|-|-|-|
|$stmt$| $stmt \rightarrow if\text-stmt$| $stmt \rightarrow other$ | | | | |
|$if\text-stmt$| $if\text-stmt \rightarrow if \ ( \ exp \ ) \ stmt \ else\text-part$ | | | | | |
|$else\text-part$| | | $else\text-part \rightarrow else \ stmt$ <br> $else\text-part \rightarrow \epsilon$| | | $else\text-part \rightarrow \epsilon$|
|$exp$| | | | $exp \rightarrow 0$ | $exp \rightarrow 1$ | |


In the table, the entry $M[else\text-part, else]$ contains two entries, corresponding to the dangling else ambiguity.

$else\text-part \rightarrow else \ stmt$ is preferred over $else\text-part \rightarrow \epsilon$.

### 4.2.3 Left Recursion Removal and Left Factoring

#### Left Recursion Removal
Left recursion is commonly used to make operations left associative, as in the simple expression grammar, where

$ exp \rightarrow exp \ addop \ term \ \mid \ term$

The above case involve immediate left recursion.

A more difficult case is indirect left recursion, such as in the rules

$A \rightarrow B \ b \ \mid \ \dots$

$B \rightarrow A \ a \ \mid \ \dots$

Case 1: Simple immediate left recursion

In this case the left recursion is present only in grammar rule of the form

$A \rightarrow A \ \alpha \ \mid \ \beta$

where $\alpha$ and $\beta$ are strings of terminals and nonterminals and $\beta$ does not begin with $A$.

To remove the left recursion, we rewrite this grammar rule into two rules:

$A \rightarrow \beta \ A'$

$A' \rightarrow \alpha \ A' \ \mid \epsilon$

Consider again the left recursive rule from the simple expression grammar:

$exp \rightarrow exp \ addop \ term \ \mid \ term$

This is the form $A \rightarrow A \ \alpha \ \mid \ \beta$, with $A \ = \ exp$, $\alpha \ = \ addop \ term$, and $\beta \ = \ term$.

Rewriting this rule to remove left recursion, we obtain

$exp \rightarrow term \ exp'$

$exp' \rightarrow addop \ term \ exp' \ \mid \ \epsilon$

## 4.3 First and Follow Sets

### 4.3.1 First Sets

Let $X$ be a grammar symbol (a terminal or nonterminal) or $\epsilon$. Then the set $First(X)$ consisting of terminals, and possibly $\epsilon$, is defined as follows.

1. If $X$ is a terminal or $\epsilon$, then $First(X) = \lbrace X \rbrace$.

2. If $X$ is a nonterminal, then for each production choice $X \rightarrow X_1 X_2 \dots X_n$, $First(X)$ contains $First(X_1) - \lbrace \epsilon \rbrace$. If also for some $i < n$, all the sets $First(X_1), \dots, First(X_i)$ contain $\epsilon$, then $First(X)$ contains $First(X_{i+1}) - \lbrace \epsilon \rbrace$. If all the sets $First(X_1), \dots, First(X_n)$ contain $\epsilon$, then $First(X)$ also contains $\epsilon$.

Now define $First(\alpha)$ for any string $\alpha=X_1 X_2 \dots X_n$ (a string of terminals and non-terminals), as follows. $First(\alpha)$ contains $First(X_1) - \lbrace \epsilon \rbrace$. For each $i = 2,\dots,n$, if $First(X_k)$ contains $\epsilon$ for all $k=1,\dots,i-1$, then $First(\alpha)$ contains $First(X_i)-\lbrace \epsilon \rbrace$. Finally, if for all $i=1,\dots,n$, $First(X_i)$ contains $\epsilon$, then $First(\alpha)$ contains $\epsilon$.

#### Figure 4.6 Algorithm for computing $First(A)$ for all nonterminals $A$


- for all nonterminals A do $First(A) := \lbrace \rbrace$
  - while there are changes to any $First(A)$ do
    - for each production choice $A \rightarrow X_1 X_2 \dots X_n$ do
      - $k := 1$;
      - $Continue := true$;
      - while $Continue = true$ and $k \le n$ do
        - $add \ First(X_k) - \lbrace \epsilon \rbrace \  to \ First(A)$;
        - if $\epsilon$ is nont in $First(X_k)$ then
          - $Continue := false$;
        - $k := k + 1$;
      - if $Continue = true$ then
        - $add \ \epsilon \ to \ First(A)$;

#### Definition
A nonterminal $A$ is *nullable* if there exists a derivation $A \Rightarrow * \  \epsilon$.

#### Theorem
A nonterminal $A$ is nullable if and only if $First(A)$ contains $\epsilon$.

#### Example 4.9
Consider our simple integer expression grammar:

$exp \rightarrow exp \ addop \ term \ \mid \ term$

$addop \rightarrow + \ \mid \ -$

$term \rightarrow term \ mulop \ factor \ \mid \ factor$

$mulop \rightarrow *$

$factor \rightarrow ( \ exp \ ) \ \mid \ number$

We write out each choice separately so that we may consider them in order.










 







