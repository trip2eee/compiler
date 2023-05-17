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

 - $exp \ \rightarrow \ exp \ addop \ term \mid \ term$
 - $addop \ \rightarrow \ + \ \mid \ -$
 - $term \ \rightarrow \ term \ mulop \ term \mid factor$
 - $mulop \ \rightarrow \ *$
 - $factor \ \rightarrow \ (\ exp \ ) \mid number$

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

  - $exp \ \rightarrow \ term \ \lbrace \ addop \ term \rbrace$
  - $term \ \rightarrow \ factor \ \lbrace \ mulop \ factor \ \rbrace$
  - $addop \ \rightarrow \ + \ \mid \ -$
  - $mulop \ \rightarrow \ *$
  - $factor \ \rightarrow \ (\ exp \ ) \mid number$

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

$exp \rightarrow exp \ addop \ term \ \mid \ term$

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


#### Figure 4.7 Simplied algorithm of Figure 4.6 in the abscence of $\epsilon$-productions
 - for all nonterminals $A$ do $First(A) := \lbrace \rbrace$
 - while there are changes to any $First(A)$ do
   - for each production choice $A \rightarrow X_1 X_2 \dots X_n$ do
     - add $First(X_1) \ to \ First(A)$

#### Definition
A nonterminal $A$ is *nullable* if there exists a derivation $A \Rightarrow * \  \epsilon$.

#### Theorem
A nonterminal $A$ is nullable if and only if $First(A)$ contains $\epsilon$.

#### Example 4.9
Consider our simple integer expression grammar:

  - $exp \rightarrow exp \ addop \ term \ \mid \ term$
  - $addop \rightarrow + \ \mid \ -$
  - $term \rightarrow term \ mulop \ factor \ \mid \ factor$
  - $mulop \rightarrow *$
  - $factor \rightarrow ( \ exp \ ) \ \mid \ number$

We write out each choice separately so that we may consider them in order.


  1. $exp \rightarrow exp \ addop \ term$
  2. $exp \rightarrow term$
  3. $addop \rightarrow +$
  4. $addop \rightarrow -$
  5. $term \rightarrow term \ mulop \ factor$
  6. $term \rightarrow factor$
  7. $mulop \rightarrow *$
  8. $factor \rightarrow ( \ exp \ )$
  9. $factor \rightarrow number$

This grammar contains no $\epsilon$-productions, so we may use the algorithm of Figure 4.7.

Note that the left recursive rules 1 and 5 will add nothing to the First sets. For example, grammar rule 1 states only that $First(exp)$ should be added to $First(exp)$.

Now we apply the algorithm of Figure 4.7

- Pass 1
  - Rule 1
    - No change
  - Rule 2
    - Add the contents of $First(term)$ to $First(exp)$.
    - But $First(term)$ is currently empty, so this also changes nothing.
  - Rule 3, 4
    - Add + and - to $First(addop)$, respectively.
    - $First(addop) = \lbrace \ +, \ - \ \rbrace$
  - Rule 5
    - No change
  - Rule 6
    - Add $First(factor)$ to $First(term)$
    - But $First(factor)$ is currently still empty, so no change occurs.
    - $First(factor) = \lbrace \ \rbrace$
  - Rule 7
    - Add * to $First(mulop)$
    - $First(mulop) = \lbrace \ * \ \rbrace$
  - Rule 8
    - Add ( to $First(factor)$
    - $First(factor) = \lbrace \ ( \ \rbrace$
  - Rule 9
    - Add $number$ to $First(factor)$
    - $First(factor) = \lbrace \ (, \ number \ \rbrace$

- Pass 2
  - Rule 6
    - Add $First(factor)$ to $First(term)$
    - $First(term) = \lbrace \ (, \ number \ \rbrace$

- Pass 3
  - Rule 2
    - Add $First(term)$ to $First(exp)$
    - $First(exp) = \lbrace \ (, \ number \ \rbrace$

- Pass 4
  - No change.


We have computed the following First sets:

- $First(exp) = \lbrace \ (, \ number \ \rbrace$
- $First(term) = \lbrace \ (, \ number \ \rbrace$
- $First(factor) = \lbrace \ (, \ number \ \rbrace$
- $First(addop) = \lbrace \ +, \ - \ \rbrace$
- $First(mulop) = \lbrace \ * \ \rbrace$

#### Table 4.6 Computation of First sets for the grammar of Example 4.9

|Grammar rule | Pass 1 | Pass 2 | Pass 3 |
|-|-|-|-
|1. $exp \rightarrow exp \ add \ term$ | | |
|2. $exp \rightarrow term$ | | | $First(exp) = \lbrace \ (, \ number \ \rbrace$ |
|3. $addop \rightarrow +$ | $First(addop) = \lbrace \ + \ \rbrace$ | | |
|4. $addop \rightarrow -$ | $First(addop) = \lbrace \ +, \ - \ \rbrace$ | | |
|5. $term \rightarrow term \ mulop \ factor$ | | | |
|6. $term \rightarrow factor$| | $First(term) = \lbrace \ (, \ number \ \rbrace$ | |
|7. $mulop \rightarrow *$ | $First(mulop) = \lbrace \ * \ \rbrace$ | | |
|8. $factor \rightarrow ( \ exp \ )$ | $First(factor) = \lbrace \ ( \ \rbrace$ | | |
|9. $factor \rightarrow number$ | $First(factor) = \lbrace \ (, \ number \ \rbrace$ | | |

#### Example 4.10
Consider the (left-factored) grammar of if-statements:

  - $stmt \rightarrow if \text-stmt \ \mid \ other$
  - $if\text-stmt \rightarrow if \ ( \ exp \ ) \ stmt \ else\text-part$
  - $else\text-part \rightarrow else \ stmt \ \mid \ \epsilon$
  - $exp \rightarrow 0 \ \mid \ 1$

We write out he grammar rule choices separately and number them:

  1. $stmt \rightarrow if \text-stmt$

  2. $stmt \rightarrow other$

  3. $if\text-stmt \rightarrow if \ ( \ exp \ ) \ stmt \ else\text-part$

  4. $else\text-part \rightarrow else \ stmt$

  5. $else\text-part \rightarrow \epsilon$

  6. $exp \rightarrow 0$

  7. $exp \rightarrow 1$

- Pass 1
  - Rule 1
    - No change since $if\text-stmt$ is nonterminal
  
  - Rule 2
    - Add the terminal $other$ to $First(stmt)$
    - $First(stmt) = \lbrace \ other \ \rbrace$
  
  - Rule 3
    - Add if to $First(if\text-stmt)$
    - $First(if\text-stmt) = \lbrace \ if \ \rbrace$
  
  - Rule 4
    - Add else to $First(else\text-part)$
    - $First(else\text-part) = \lbrace \ else \ \rbrace$
  
  - Rule 5
    - Add $\epsilon$ to $First(else\text-part)$
    - $First(else\text-part) = \lbrace \ else, \ \epsilon \ \rbrace$

  - Rule 6 and 7
    - Add 0 and 1 to $First(exp)$
    - $First(exp) = \lbrace \ 0, \ 1 \ \rbrace$
  
- Pass 2
  - Rule 1
    - Add $if$ and $other$, which are first of $if\text-stmt$ to $First(stmt)$
    - $First(stmt) = \lbrace \ if, \ other \ \rbrace$


We have computed the following First sets:

  - $First(stmt) = \lbrace \ if, \ other \ \rbrace$
  - $First(if\text-stmt) = \lbrace \ if \ \rbrace$
  - $First(else\text-part) = \lbrace \ else, \ \epsilon \ \rbrace$
  - $First(exp) = \lbrace \ 0, \ 1 \ \rbrace$


| Grammar rule | Pass 1 | Pass 2 |
| - | - | - |
| 1. $stmt \rightarrow if \text-stmt$ | |$First(stmt) = \lbrace \ if, \ other \ \rbrace$ |
| 2. $stmt \rightarrow other$ | $First(stmt) = \lbrace \ other \ \rbrace$| |
| 3. $if\text-stmt \rightarrow if \ ( \ exp \ ) \ stmt \ else\text-part$ | $First(if\text-stmt) = \lbrace \ if \ \rbrace$ | |
| 4. $else\text-part \rightarrow else \ stmt$ | $First(else\text-part) = \lbrace \ else \ \rbrace$| |
| 5. $else\text-part \rightarrow \epsilon$ |$First(else\text-part) = \lbrace \ else, \ \epsilon \ \rbrace$ | |
| 6. $exp \rightarrow 0$ | $First(exp) = \lbrace \ 0 \ \rbrace$| |
| 7. $exp \rightarrow 1$ | $First(exp) = \lbrace \ 0, \ 1 \ \rbrace$| |



### 4.3.2 Follow Sets

#### Definition
Given a nonterminal $A$, the set $Follow(A)$, consisting of terminals, and possibly $, is defined as follows.

1. If $A$ is the start symbol, then $ is in $Follow(A)$
2. If there is a production $B \rightarrow \alpha \  A \  \gamma$, then $First(\gamma) - \lbrace \ \epsilon \ \rbrace$ is in $Follow(A)$.
3. If there is a production $B \rightarrow \alpha \ A \ \gamma$ such that $\epsilon$ is in $First(\gamma)$, then $Follow(A)$ contains $Follow(B)$.

The first thing to notice that $, used to mark the end of the input, behaves as if it were a token in the computation of the Follow set.

The second thing to notice is "pseudotoken" $\epsilon$ is never an element of Follow set.

We also note that Follow sets are defined only for nonterminals, while Fist sets are also defined for terminals and for strings of terminals and nonterminals.

Finally, we note that the definition of Follow sets works "on the right" in productions, while the definition of the First sets works "on the left." By this mean that a production $A \rightarrow \alpha$ has no information about the Follow set of $A$ if $\alpha$ does not contain $A$.

FUrthermore, given a grammar rule $A \rightarrow \alpha B$, $Follow(B)$ will include $Follow(A)$ by case (3) of definition. This is because, in any string that contains $A$, $A$ could be replaced by $\alpha \ B$.

In Figure 4.8 we give the algorithm for the computation of the Follow sets that results from the definition of Follow sets.

#### Figure 4.8 Algorithm for the computation of Follow sets

- $Follow(start\text-symbol) := \lbrace \ \$ \ \rbrace ;$
- for all nonterminals $A \neq start\text-symbol$ do $Follow(A) := \lbrace \ \rbrace$
- while there are changes to any Follow sets do
  - for each production $A \rightarrow X_1 X_2 \dots X_n$ do
    - for each $X_i$ that is nonterminal do
      - add $First(X_{i+1} X_{i+2} \dots X_n) \ -\  \lbrace \ \epsilon \ \rbrace$ to $Follow(X_i)$
      - (* Note: $if \ i=n, \ then \ X_{i+1} X_{i+2} \dots X_n \ = \ \epsilon$ *)
      - if $\epsilon$ is in $First(X_{i+1} X_{i+2} \dots X_n)$ then
        - add $Follow(A)$ to $Follow(X_i)$



#### Example 4.12
Consider the simple expression grammar whose First sets we computed in Example 4.9.

Grammar Rules

- $exp \rightarrow exp \ addop \ term \ \mid \ term$
- $addop \rightarrow + \ \mid \ -$
- $term \rightarrow term \ mulop \ factor \ \mid \ factor$
- $mulop \rightarrow *$
- $factor \rightarrow ( \ exp \ ) \ \mid \ number$

First sets

- $First(exp) = \lbrace \ (, \ number \ \rbrace$
- $First(term) = \lbrace \ (, \ number \ \rbrace$
- $First(factor) = \lbrace \ (, \ number \ \rbrace$
- $First(addop) = \lbrace \ +, \ - \ \rbrace$
- $First(mulop) = \lbrace \ * \ \rbrace$

We write out each choice separately so that we may consider them in order.

  1. $exp \rightarrow exp \ addop \ term$
  2. $exp \rightarrow term$
  3. $addop \rightarrow +$
  4. $addop \rightarrow -$
  5. $term \rightarrow term \ mulop \ factor$
  6. $term \rightarrow factor$
  7. $mulop \rightarrow *$
  8. $factor \rightarrow ( \ exp \ )$
  9. $factor \rightarrow number$

- Pass 1
  - Rules 3, 4, 7, and 9
    - No nonterminals on thr right-hand sides
    - Nothing to add to the computation of Follow sets.

  - Rule 1
    - Affect the Follow sets of three nonterminals: $exp$, $addop$, and $term$.
    - Add $First(addop)$ to $Follow(exp)$
    - $Follow(exp) = \lbrace \ \$, \ +, \ - \ \rbrace$
    - Add $First(term)$ to $Follow(addop)$
    - $Follow(addop) = \lbrace \ (, \ number \ \rbrace$
    - $Follow(exp)$ is added to $Follow(term)$
    - $Follow(term) = \lbrace \ \$, \ +, \ - \rbrace$
  - Rule 2
    - $Follow(exp)$ is added to $Follow(term)$, which is done in Rule 1.
    - No change
  - Rule 5
    - $First(mulop)$ is added to $Follow(term)$
    - $Follow(term) = \lbrace \ \$, \ +, \ -, \ * \ \rbrace$
    - $First(factor)$ is added to $Follow(mulop)$
    - $Follow(mulop) = \lbrace \ (, \ number, \ \rbrace$
    - $Follow(term)$ is added to $Follow(factor)$
    - $Follow(factor) = \lbrace \ \$, \ +, \ -, \ * \ \rbrace$
  - Rule 6
    - Same effact as the step for rule 5.
    - No change

  - Rule 8
    - Adds $First()) = \lbrace \ ) \ \rbrace$ to $Follow(exp)$
    - $Follow(exp) = \lbrace \ \$, \ +, \ -, \ ) \ \rbrace$

- Pass 2
  - Rule 1
    - Adds ) to $Follow(term)$ since $Follow(exp)$ is updated by Rule 8 in Pass 1.
    - $Follow(term) = \lbrace \ \$, \ +, \ -, \ *, \ ) \ \rbrace$
  - Rule 5
    - Add ) to $Follow(factor)$
    - $Follow(factor) = \lbrace \ \$, \ +, \ -, \ *, \  ) \ \rbrace$
- Pass 3
  - No change

We have computed the following Follow sets.
- $Follow(exp) = \lbrace \ \$, \ +, \ -, \ ) \ \rbrace$
- $Follow(addop) = \lbrace \ (, \ number \ \rbrace$
- $Follow(term) = \lbrace \ \$, \ +, \ -, \ *, \ ) \ \rbrace$
- $Follow(mulop) = \lbrace \ (, \ number, \ \rbrace$
- $Follow(factor) = \lbrace \ \$, \ +, \ -, \ *, \  ) \ \rbrace$

#### Table 4.8 Computation of Follow sets for the grammar of Example 4.12
|Grammar rule | Pass 1 | Pass 2 |
| - | - | - |
| 1. $exp \rightarrow exp \ addop \ term$ | $Follow(exp) = \lbrace \ \$, \ +, \ - \ \rbrace$ <br> $Follow(addop) = \lbrace \ (, \ number \ \rbrace$ <br> $Follow(term) = \lbrace \ \$, \ +, \ - \rbrace$ | $Follow(term) = \lbrace \ \$, \ +, \ -, \ *, \ ) \ \rbrace$ |
| 2. $exp \rightarrow term$ | | |
| 5. $term \rightarrow term \ mulop \ factor$ | $Follow(term) = \lbrace \ \$, \ +, \ -, \ * \ \rbrace$ <br> $Follow(mulop) = \lbrace \ (, \ number, \ \rbrace$ <br> $Follow(factor) = \lbrace \  \$, \ +, \ -, \ * \ \rbrace$| $Follow(factor) = \lbrace \ \$, \ +, \ -, \ *, \  ) \ \rbrace$ |
| 6. $term \rightarrow factor$ | | |
| 8. $factor \rightarrow ( \ exp \ )$ | $Follow(exp) = \lbrace \ \$, \ +, \ -, \ ) \ \rbrace$ | |


### 4.3.3 Constructing LL(1) Parsing Tables
Consider now the original construction of the entries of the LL(1) parsing table, as given in Section 4.2.2:

1. If $A \rightarrow \alpha$ is a production choice, and there is a derivation $\alpha \Rightarrow * \ a \ \beta$, where $a$ is a token, then add $A \rightarrow \alpha$ to the table entry $M[A, a]$.

2. If $A \rightarrow \alpha$ is a production choice and there are derivation $\alpha \Rightarrow * \epsilon$ and $S \ \$ \Rightarrow * \ \beta\ A \ a \ \gamma$, where $S$ is the start symbol and $a$ is a token (or $), then add $A \rightarrow \alpha$ to the table entry $M[A, a]$.

Clearly, the token $a$ in rule 1 is $First(\alpha)$, and the token $a$ of rule 2 is in $Follow(A)$. Thus, we have arrived at the following algorithmic construction of the LL(1) parseing table:

Repeat the following two steps for each nonterminal $A$ and production choice $A \rightarrow \alpha$.
1. For each token $a$ in $First(\alpha)$, add $A \rightarrow \alpha$ to the entry $M[A, a]$.
2. If $\epsilon$ is in $First(\alpha)$, for each element $a$ of $Follow(A)$ (a token or $), add $A \rightarrow \alpha$ to $M[A, a]$.

The following theorem is essentially a direct consequence of the definition of an LL(1) grammar and the parsing table construction just given.

#### Theorem

A grammar in BNF is LL(1) if the following conditions are satisfied.
1. For every production $A \rightarrow \alpha_1 \ \mid \ \alpha_2 \ \mid \ \dots \ \mid \ \alpha_n$, $First(\alpha_i) \ \cap \ First(\alpha_j)$ is empty for all $i$ and $j$, $1 \ \le \  i, \ j \ \le n, \  i \neq j$
2. For every nonterminal $A$ such that $First(A)$ contains $\epsilon$, $First(A) \ \cap \ Follow(A)$ is empty.


#### Example 4.15
Consider the simple expression grammar we have been using as a starndard example.

- $exp \rightarrow term \ exp'$
- $exp' \rightarrow addop \ term \ exp' \ \mid \ \epsilon$
- $addop \rightarrow + \ \mid \ -$
- $term \rightarrow factor \ term'$
- $term' \rightarrow mulop \ factor \ term' \ \mid \ \epsilon$
- $mulop \rightarrow *$
- $factor \rightarrow ( \ exp \ ) \ \mid \ number$

We must compute First and Follow sets for the nonterminals for this grammar.

First(nonterminal): Set of the first terminal string of rule.

| Grammar rule | Pass 1 | Pass 2 | Pass 3 |
| - | - | - | - |
| 1. $exp \rightarrow term \ exp'$ | | | $First(exp) = \lbrace \ (, \ number \ \rbrace$ |
| 2. $exp' \rightarrow addop \ term \ exp'$ | | $First(exp') = \lbrace \ \epsilon, \ +, \ - \ \rbrace$ | |
| 3. $exp' \rightarrow \epsilon$ | $First(exp') = \lbrace \ \epsilon \ \rbrace$| | |
| 4. $addop \rightarrow +$ | $First(addop) = \lbrace \ + \ \rbrace$ | | |
| 5. $addop \rightarrow -$ | $First(addop) = \lbrace \ +, \ - \ \rbrace$ | | |
| 6. $term \rightarrow factor \ term'$ | | $First(term) = \lbrace \ (, \ number \ \rbrace$ | |
| 7. $term' \rightarrow mulop \ factor \ term'$ | | $First(term') = \lbrace \ \epsilon, \ * \ \rbrace$  | |
| 8. $term' \rightarrow \epsilon$ | $First(term') = \lbrace \ \epsilon \ \rbrace$ | | |
| 9. $mulop \rightarrow *$ | $First(mulop) = \lbrace \ * \ \rbrace$  | | |
| 10. $factor \rightarrow ( \ exp \ )$ | $First(factor) = \lbrace \ ( \ \rbrace$ | | |
| 11. $factor \rightarrow number$ | $First(factor) = \lbrace \ (, \ number \ \rbrace$ | | |


- $First(exp) = \lbrace \ (, \ number \ \rbrace$
- $First(exp') = \lbrace \ \epsilon, \ +, \ - \ \rbrace$
- $First(addop) = \lbrace \ +, \ - \ \rbrace$
- $First(term) = \lbrace \ (, \ number \ \rbrace$
- $First(term') = \lbrace \ \epsilon, \ * \ \rbrace$
- $First(mulop) = \lbrace \ * \ \rbrace$
- $First(factor) = \lbrace \ (, \ number \ \rbrace$

Now let's compute Follow set

- $Follow(exp) = \lbrace \ \$ \ \rbrace$
- $Follow(exp') = \lbrace \ \$ \ \rbrace$
- $Follow(term) = \lbrace \ \$ \ \rbrace$
- $Follow(term') = \lbrace \ \$ \ \rbrace$
- $Follow(factor) = \lbrace \ \$ \ \rbrace$


| Grammar rule | Pass 1 | Pass 2 |
| - | - | - |
| 1. $exp \rightarrow term \ exp'$ | Add $First(exp')$ to $Follow(term)$ <br>$Follow(term) = \lbrace \ \$, \ +, \ - \ \rbrace$| Add $Follow(exp)$ to $Follow(exp')$<br>$Follow(exp')=\lbrace \$, \ ) \ \rbrace$<br>Add $Follow(exp)$ to $Follow(term)$ since $\epsilon$ is in $First(exp')$<br>$Follow(term) = \lbrace \ \$, \ +, \, -, \ ) \ \rbrace$|
| 2. $exp' \rightarrow addop \ term \ exp'$ | Add $First(term)$ to $Follow(addop)$<br>$Follow(addop)=\lbrace \ (, \ number \ \rbrace$ <br> Add $First(exp')$ to $Follow(term)$<br>$Follow(term) = \lbrace \ \$, \ +, \ - \ \rbrace$| |
| 3. $exp' \rightarrow \epsilon$ | | |
| 4. $addop \rightarrow +$ | | |
| 5. $addop \rightarrow -$ | | |
| 6. $term \rightarrow factor \ term'$ | Add $First(term')$ to $Follow(factor)$<br>$Follow(factor) = \lbrace \ \$, \ * \ \rbrace$| Add $Follow(term)$ to $Follow(term')$<br>$Follow(term') = \lbrace \ \$, \ +, \ -, \ ) \ \rbrace$<br>Add $Follow(term)$ to $Follow(factor)$ since $\epsilon$ is in $First(term')$<br>$Follow(factor)=\lbrace \ \$, *, \ +, \ -, \ ) \ \rbrace$|
| 7. $term' \rightarrow mulop \ factor \ term'$ | Add $First(factor)$ to $Follow(mulop)$<br>$Follow(mulop) = \lbrace \ (, \ number \ \rbrace$<br> Add $First(term')$ to $Follow(factor)$<br>$Follow(factor) = \lbrace \ * \ \rbrace$| |
| 8. $term' \rightarrow \epsilon$ | | |
| 9. $mulop \rightarrow *$ | | |
| 10. $factor \rightarrow ( \ exp \ )$ | $Follow(exp) = \lbrace \ \$, \ ) \ \rbrace$ | |
| 11. $factor \rightarrow number$ | | |

- $Follow(exp) = \lbrace \ \$, \ ) \ \rbrace$
- $Follow(exp')=\lbrace \$, \ ) \ \rbrace$
- $Follow(addop)=\lbrace \ (, \ number \ \rbrace$
- $Follow(term) = \lbrace \ \$, \ +, \, -, \ ) \ \rbrace$
- $Follow(term') = \lbrace \ \$, \ +, \ -, \ ) \ \rbrace$
- $Follow(mulop) = \lbrace \ (, \ number \ \rbrace$
- $Follow(factor)=\lbrace \ \$, *, \ +, \ -, \ ) \ \rbrace$

## 4.5 Error Recovery in Top-Down Parsers
A parser must determine whether a program is synthactically correct or not. A parser that performs this task alone is called a recognizer.

Some parsers may go so far to attempt some from of error correction (or, perhaps more appropreately, error repair), where the parser attempts to infer a correct program from the incorrect one given.

Compiler writers find it difficult enough to generate meaningful error messages without trying to do error correction.

Some important considerations that apply are the following.
1. A parser should try to determine that an error has occurred as soon as possible. Waiting too long before declaring error means the location of the actual error may have been lost.

2. After an error has occurred, the parser must pick a likely place to resume the parse. A parser should always try to parse as much of the code as possible, in order to find as many real errors as possible during a single translation.

3. A parser should try to avoid the error cascade problem, in which one error generates a lengthy sequence of spurious error messages.

4. A parser must avoid infinite loops on errors, in which a unending cascade of error messages is generated without consuming any input.

Some of these goals conflict with each other, so that a compiler writer is forced to make trade-offs during the construction of an error handler. For example avoiding the rror cascade and infinite loop problems can cause the parser to skip some of the input, compromising the goal of processing as much of the input as possible.

### 4.5.1 Error Recovery in Recursive-Descent Parsers
A standard form of error recovery in recursive-descent parser is called *panic mode*.

The basic mechanism of panic mode is to provide each recursive procedure with an extra parameter consisting of a set of *synchronizing tokens*. As parsing proceeds, tokens that may function as synchronizing tokens are added to this set as each call occurs. If an error encountered, the parser *scans ahead*, throwing away tokens until one of the synchronizing set of tokens is seen in the input, whence parsing is resumed. Error cascades are avoided (to a certain extent) by not generating new error messages while this forward scan takes place.


What tokens to add to the synchronizing set at each point in the parse.
  - Generally, Follow sets are important candidates.
  - First sets may also be used to prevent the error handler from skipping important tokens that begin major new constructs. First stes are also importatnt, in that they allow a recursive descent parser to detect errors early in the parse, which is always helpful in any error recovery.
  - It is important to realize that panic mode works best when the compiler knows when not to panic. For example, missing punctuation symbols such as semicolons or commas, and even msssing right parentheses, should not always cause an error handler to consume tokens.

Panic mode error recoverty
- scanto : panic mode token consumer proper

```python
def scanto(synchset):
  while not (token in synchset or token is EOF):
    get_next_token()
```

- checkinput : performs the early lookahead checking
```python
def checkinput(firstset, followset):
  if not (token in firstset):
    error()
    scanto(firstset + followset)
```

### 4.5.2 Error Recovery in LL(1) Parsers
Panic mode error recovery can be implemented in LL(1) parsers in a similar manner to the way it is implemented in recursive-descent parsing.
