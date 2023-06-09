"""
@fn examples/calc/calc_parser_table.py
@brief LALR parser table generated by parser_generator.py
@date 2023-06-09 18:40:01
"""
# Definitions

class Symbol:
    def __init__(self):
        self.type = None
        self.value = None

# Parsing Table
NUM_TERMINALS = 7
NUM_NON_TERMINALS = 5
# Terminals
PLUS = 0  # +
MINUS = 1  # -
TIMES = 2  # *
DIV = 3  # /
LPAREN = 4  # (
RPAREN = 5  # )
number = 6
END = 7
# Non-Terminals
exp = 8
addop = 9
term = 10
mulop = 11
factor = 12
expp = 13
# RULE table
NUM_RULES = 11 # ACCEPT in tbl_reduce
tbl_rule = [
    [13,8,],    # 0 : exp' -> exp 
    [8,8,9,10,],    # 1 : exp -> exp addop term 
    [8,10,],    # 2 : exp -> term 
    [9,0,],    # 3 : addop -> + 
    [9,1,],    # 4 : addop -> - 
    [10,10,11,12,],    # 5 : term -> term mulop factor 
    [10,12,],    # 6 : term -> factor 
    [11,2,],    # 7 : mulop -> * 
    [11,3,],    # 8 : mulop -> / 
    [12,4,8,5,],    # 9 : factor -> ( exp ) 
    [12,6,],    # 10 : factor -> number 
]
# SHIFT / GOTO table
# + - * / ( ) number $ exp addop term mulop factor 
tbl_shift = [
    [-1, -1, -1, -1, 4, -1, 5, -1, 1, -1, 2, -1, 3, ],
    [7, 8, -1, -1, -1, -1, -1, -1, -1, 6, -1, -1, -1, ],
    [-1, -1, 10, 11, -1, -1, -1, -1, -1, -1, -1, 9, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, 4, -1, 5, -1, 12, -1, 2, -1, 3, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, 4, -1, 5, -1, -1, -1, 13, -1, 3, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, 4, -1, 5, -1, -1, -1, -1, -1, 14, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [7, 8, -1, -1, -1, 15, -1, -1, -1, 6, -1, -1, -1, ],
    [-1, -1, 10, 11, -1, -1, -1, -1, -1, -1, -1, 9, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
]
# REDUCE / ACCEPT table
tbl_reduce = [
    [-1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, 11, ],
    [2, 2, -1, -1, -1, 2, -1, 2, ],
    [6, 6, 6, 6, -1, 6, -1, 6, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, ],
    [10, 10, 10, 10, -1, 10, -1, 10, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, ],
    [3, 3, 3, 3, 3, -1, 3, -1, ],
    [4, 4, 4, 4, 4, -1, 4, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, ],
    [7, 7, 7, 7, 7, -1, 7, -1, ],
    [8, 8, 8, 8, 8, -1, 8, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, ],
    [1, 1, -1, -1, -1, 1, -1, 1, ],
    [5, 5, 5, 5, -1, 5, -1, 5, ],
    [9, 9, 9, 9, -1, 9, -1, 9, ],
]
# Reduce Actions
def reduce_rule_1(p1, p2, p3):
    result = Symbol()
    if p2.value == '+':
        result.value = p1.value + p3.value
    else:
        result.value = p1.value - p3.value

    result.type = exp
    return result

def reduce_rule_2(p1):
    result = Symbol()
    result = p1

    result.type = exp
    return result

def reduce_rule_3(p1):
    result = Symbol()
    result.value = '+'

    result.type = addop
    return result

def reduce_rule_4(p1):
    result = Symbol()
    result.value = '-'

    result.type = addop
    return result

def reduce_rule_5(p1, p2, p3):
    result = Symbol()
    if p2.value == '*':
        result.value = p1.value * p3.value
    else:
        result.value = p1.value / p3.value

    result.type = term
    return result

def reduce_rule_6(p1):
    result = Symbol()
    result = p1

    result.type = term
    return result

def reduce_rule_7(p1):
    result = Symbol()
    result.value = '*'

    result.type = mulop
    return result

def reduce_rule_8(p1):
    result = Symbol()
    result.value = '/'

    result.type = mulop
    return result

def reduce_rule_9(p1, p2, p3):
    result = Symbol()
    result = p2

    result.type = factor
    return result

def reduce_rule_10(p1):
    result = Symbol()
    result  = p1

    result.type = factor
    return result

# Embedded Actions
