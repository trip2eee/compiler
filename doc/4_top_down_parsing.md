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

$ exp \ \rightarrow \ exp \ addop \ term \mid \ term $

$ addop \ \rightarrow \ + \ \mid \ - $

$ term \ \rightarrow \ term \ mulop \ term \mid factor $

$ mulop \ \rightarrow \ * $

$ factor \ \rightarrow \ (\ exp \ ) \mid number $

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

$ exp \ \rightarrow \ term \ \lbrace \ addop \ term \rbrace $

$ term \ \rightarrow \ factor \ \lbrace \ mulop \ factor \ \rbrace$

$ addop \ \rightarrow \ + \ \mid \ - $

$ mulop \ \rightarrow \ * $

$ factor \ \rightarrow \ (\ exp \ ) \mid number $

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





