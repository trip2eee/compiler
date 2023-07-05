"""
@fn examples/regex/regex_parser.py
@brief LALR parser table generated by parser_generator.py
@date 2023-07-05 23:05:33
"""
# Definitions

import enum

class Symbol:
    def __init__(self):
        self.type = None
        self.value = None
        self.pattern = None
        self.idx_col = 0

class PatternType(enum.IntEnum):
    VALUE = 0
    NOT_VALUE = 1
    RANGE = 2
    CLASS = 3
    GROUP = 4
    OR = 5

class Pattern:
    def __init__(self):
        self.type = PatternType.VALUE
        self.value = None
        self.range_min = None
        self.range_max = None
        self.childs = []
        self.next = None
        self.count_min = 1
        self.count_max = 1
        self.matched = False
        self.matched_str = ''
        self.matched_count = 0
        self.idx_begin = 0
        self.idx_end = 0


# Auxiliary Routines
# Auxiliary Routines

def add_esc(p1):
    pattern = Pattern()
    if p1.value == 'd':        
        pattern.type = PatternType.RANGE
        pattern.range_min = '0'
        pattern.range_max = '9'
        
    else:
        pattern.type = PatternType.VALUE
        pattern.value = p1.value

    return pattern
# Parsing Table
NUM_TERMINALS = 15
NUM_NON_TERMINALS = 10
# Terminals
ESC = 1
CHAR = 8
DIGIT = 9
END__RESERVED = 15
# Non-Terminals
CMD = 16
EXP = 17
SUBEXP = 18
GROUP = 19
CLASS = 20
TERM = 21
FACTOR = 22
BASE = 23
NUMBER = 24
COUNT = 25
CMDp = 26
yy_token_names = {
    '|':0, 'ESC':1, '(':2, ')':3, '[':4, ']':5, '-':6, '+':7, 'CHAR':8, 'DIGIT':9, 
    '*':10, '?':11, '{':12, '}':13, ',':14, 'END__RESERVED':15, 'CMD':16, 'EXP':17, 'SUBEXP':18, 'GROUP':19, 
    'CLASS':20, 'TERM':21, 'FACTOR':22, 'BASE':23, 'NUMBER':24, 'COUNT':25, 'CMDp':26
}
# RULE table
NUM_RULES = 29 # ACCEPT in tbl_reduce
tbl_rule = [
    [26,16,],    # 0 : CMD' -> CMD 
    [16,17,],    # 1 : CMD -> EXP 
    [17,18,17,],    # 2 : EXP -> SUBEXP EXP 
    [17,18,],    # 3 : EXP -> SUBEXP 
    [17,17,0,17,],    # 4 : EXP -> EXP | EXP 
    [18,20,],    # 5 : SUBEXP -> CLASS 
    [18,23,],    # 6 : SUBEXP -> BASE 
    [18,19,],    # 7 : SUBEXP -> GROUP 
    [18,18,25,],    # 8 : SUBEXP -> SUBEXP COUNT 
    [18,1,],    # 9 : SUBEXP -> ESC 
    [19,2,17,3,],    # 10 : GROUP -> ( EXP ) 
    [20,4,21,5,],    # 11 : CLASS -> [ TERM ] 
    [21,22,21,],    # 12 : TERM -> FACTOR TERM 
    [21,22,],    # 13 : TERM -> FACTOR 
    [21,22,6,],    # 14 : TERM -> FACTOR - 
    [22,23,],    # 15 : FACTOR -> BASE 
    [22,23,6,23,],    # 16 : FACTOR -> BASE - BASE 
    [22,1,],    # 17 : FACTOR -> ESC 
    [22,7,],    # 18 : FACTOR -> + 
    [22,6,],    # 19 : FACTOR -> - 
    [23,8,],    # 20 : BASE -> CHAR 
    [23,9,],    # 21 : BASE -> DIGIT 
    [24,24,9,],    # 22 : NUMBER -> NUMBER DIGIT 
    [24,9,],    # 23 : NUMBER -> DIGIT 
    [25,7,],    # 24 : COUNT -> + 
    [25,10,],    # 25 : COUNT -> * 
    [25,11,],    # 26 : COUNT -> ? 
    [25,12,24,13,],    # 27 : COUNT -> { NUMBER } 
    [25,12,24,14,24,13,],    # 28 : COUNT -> { NUMBER , NUMBER } 
]
# SHIFT / GOTO table
# | ESC ( ) [ ] - + CHAR DIGIT * ? { } , $ CMD EXP SUBEXP GROUP CLASS TERM FACTOR BASE NUMBER COUNT 
tbl_shift = [
    [-1, 7, 11, -1, 8, -1, -1, -1, 9, 10, -1, -1, -1, -1, -1, -1, 1, 2, 3, 6, 4, -1, -1, 5, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, 7, 11, -1, 8, -1, -1, 15, 9, 10, 16, 17, 18, -1, -1, -1, -1, 13, 3, 6, 4, -1, -1, 5, -1, 14, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, 22, -1, -1, -1, -1, 24, 23, 9, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 19, 20, 21, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, 7, 11, -1, 8, -1, -1, -1, 9, 10, -1, -1, -1, -1, -1, -1, -1, 25, 3, 6, 4, -1, -1, 5, -1, -1, ],
    [-1, 7, 11, -1, 8, -1, -1, -1, 9, 10, -1, -1, -1, -1, -1, -1, -1, 26, 3, 6, 4, -1, -1, 5, -1, -1, ],
    [12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 28, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 27, -1, ],
    [-1, -1, -1, -1, -1, 29, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, 22, -1, -1, -1, -1, 31, 23, 9, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, 20, 21, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, 32, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [12, -1, -1, 33, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 36, -1, -1, -1, 34, 35, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, 9, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 37, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 28, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 38, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 36, -1, -1, -1, 39, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
]
# REDUCE / ACCEPT table
tbl_reduce = [
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 29, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, ],
    [3, -1, -1, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, ],
    [5, 5, 5, 5, 5, -1, -1, 5, 5, 5, 5, 5, 5, -1, -1, 5, ],
    [6, 6, 6, 6, 6, -1, -1, 6, 6, 6, 6, 6, 6, -1, -1, 6, ],
    [7, 7, 7, 7, 7, -1, -1, 7, 7, 7, 7, 7, 7, -1, -1, 7, ],
    [9, 9, 9, 9, 9, -1, -1, 9, 9, 9, 9, 9, 9, -1, -1, 9, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, -1, -1, 20, ],
    [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, -1, -1, 21, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, 2, 2, 2, 2, -1, -1, -1, 2, 2, -1, -1, -1, -1, -1, 2, ],
    [8, 8, 8, 8, 8, -1, -1, 8, 8, 8, 8, 8, 8, -1, -1, 8, ],
    [24, 24, 24, 24, 24, -1, -1, 24, 24, 24, 24, 24, 24, -1, -1, 24, ],
    [25, 25, 25, 25, 25, -1, -1, 25, 25, 25, 25, 25, 25, -1, -1, 25, ],
    [26, 26, 26, 26, 26, -1, -1, 26, 26, 26, 26, 26, 26, -1, -1, 26, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, 13, -1, 13, 13, -1, -1, -1, -1, -1, -1, -1, -1, -1, 13, ],
    [-1, 15, 15, -1, 15, 15, -1, 15, 15, 15, -1, -1, -1, -1, -1, 15, ],
    [-1, 17, 17, -1, 17, 17, 17, 17, 17, 17, -1, -1, -1, -1, -1, 17, ],
    [-1, 18, 18, -1, 18, 18, 18, 18, 18, 18, -1, -1, -1, -1, -1, 18, ],
    [-1, 19, 19, -1, 19, 19, 19, 19, 19, 19, -1, -1, -1, -1, -1, 19, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, 4, 4, 4, 4, -1, -1, -1, 4, 4, -1, -1, -1, -1, -1, 4, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, 23, 23, -1, 23, -1, -1, 23, 23, 23, 23, 23, 23, 23, 23, 23, ],
    [11, 11, 11, 11, 11, -1, -1, 11, 11, 11, 11, 11, 11, -1, -1, 11, ],
    [-1, 12, 12, -1, 12, 12, -1, -1, 12, 12, -1, -1, -1, -1, -1, 12, ],
    [-1, 19, 14, -1, 14, 14, 19, 19, 19, 19, -1, -1, -1, -1, -1, 14, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [10, 10, 10, 10, 10, -1, -1, 10, 10, 10, 10, 10, 10, -1, -1, 10, ],
    [27, 27, 27, 27, 27, -1, -1, 27, 27, 27, 27, 27, 27, -1, -1, 27, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, 22, 22, -1, 22, -1, -1, 22, 22, 22, 22, 22, 22, 22, 22, 22, ],
    [-1, 16, 16, -1, 16, 16, 16, 16, 16, 16, -1, -1, -1, -1, -1, 16, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [28, 28, 28, 28, 28, -1, -1, 28, 28, 28, 28, 28, 28, -1, -1, 28, ],
]
# Reduce Actions
def reduce_rule_1(p1):
    # CMD -> EXP 
    result = Symbol()
    result = p1

    result.type = CMD
    return result

def reduce_rule_2(p1, p2):
    # EXP -> SUBEXP EXP 
    result = Symbol()
    
    p1.pattern.next = p2.pattern
    result = p1

    result.type = EXP
    return result

def reduce_rule_3(p1):
    # EXP -> SUBEXP 
    result = Symbol()
    result = p1
    result.type = EXP
    return result

def reduce_rule_4(p1, p2, p3):
    # EXP -> EXP | EXP 
    result = Symbol()
    pattern = Pattern()
    pattern.type = PatternType.OR
    pattern.childs = [p1.pattern, p3.pattern]
    result.pattern = pattern

    result.type = EXP
    return result

def reduce_rule_5(p1):
    # SUBEXP -> CLASS 
    result = Symbol()
    result = p1
    result.type = SUBEXP
    return result

def reduce_rule_6(p1):
    # SUBEXP -> BASE 
    result = Symbol()
    pattern = Pattern()
    if p1.value == '.':
        pattern.type = PatternType.NOT_VALUE
        pattern.value = '\n'
    else:
        pattern.type = PatternType.VALUE
        pattern.value = p1.value
    result.pattern = pattern

    result.type = SUBEXP
    return result

def reduce_rule_7(p1):
    # SUBEXP -> GROUP 
    result = Symbol()
    result = p1
    result.type = SUBEXP
    return result

def reduce_rule_8(p1, p2):
    # SUBEXP -> SUBEXP COUNT 
    result = Symbol()
    p1.pattern.count_min = p2.pattern.count_min
    p1.pattern.count_max = p2.pattern.count_max
    result = p1

    result.type = SUBEXP
    return result

def reduce_rule_9(p1):
    # SUBEXP -> ESC 
    result = Symbol()
    result.pattern = add_esc(p1)

    result.type = SUBEXP
    return result

def reduce_rule_10(p1, p2, p3):
    # GROUP -> ( EXP ) 
    result = Symbol()
    if p2.pattern.next is not None:
        pattern = Pattern()
        pattern.type = PatternType.GROUP
        pattern.childs = [p2.pattern]
    else:
        pattern = p2.pattern

    result.pattern = pattern

    result.type = GROUP
    return result

def reduce_rule_11(p1, p2, p3):
    # CLASS -> [ TERM ] 
    result = Symbol()
    pattern = Pattern()
    pattern.type = PatternType.CLASS
    
    pattern.childs = []
    child = p2.pattern
    while child is not None:
        pattern.childs.append(child)
        child = child.next

    result.pattern = pattern

    result.type = CLASS
    return result

def reduce_rule_12(p1, p2):
    # TERM -> FACTOR TERM 
    result = Symbol()
    
    p1.pattern.next = p2.pattern
    result = p1

    result.type = TERM
    return result

def reduce_rule_13(p1):
    # TERM -> FACTOR 
    result = Symbol()
    result = p1
    result.type = TERM
    return result

def reduce_rule_14(p1, p2):
    # TERM -> FACTOR - 
    result = Symbol()
    pattern = Pattern()
    pattern.type = PatternType.VALUE
    pattern.value = '-'
    result.pattern = p1.pattern
    p1.pattern.next = pattern

    result.type = TERM
    return result

def reduce_rule_15(p1):
    # FACTOR -> BASE 
    result = Symbol()
    pattern = Pattern()
    pattern.type = PatternType.VALUE
    pattern.value = p1.value
    result.pattern = pattern

    result.type = FACTOR
    return result

def reduce_rule_16(p1, p2, p3):
    # FACTOR -> BASE - BASE 
    result = Symbol()
    pattern = Pattern()
    pattern.type = PatternType.RANGE
    pattern.range_min = p1.value
    pattern.range_max = p3.value
    result.pattern = pattern

    result.type = FACTOR
    return result

def reduce_rule_17(p1):
    # FACTOR -> ESC 
    result = Symbol()
    result.pattern = add_esc(p1)

    result.type = FACTOR
    return result

def reduce_rule_18(p1):
    # FACTOR -> + 
    result = Symbol()
    pattern = Pattern()
    pattern.type = PatternType.VALUE
    pattern.value = p1.value
    result.pattern = pattern

    result.type = FACTOR
    return result

def reduce_rule_19(p1):
    # FACTOR -> - 
    result = Symbol()
    pattern = Pattern()
    pattern.type = PatternType.VALUE
    pattern.value = p1.value
    result.pattern = pattern

    result.type = FACTOR
    return result

def reduce_rule_20(p1):
    # BASE -> CHAR 
    result = Symbol()
    result = p1
    result.type = BASE
    return result

def reduce_rule_21(p1):
    # BASE -> DIGIT 
    result = Symbol()
    result = p1
    result.type = BASE
    return result

def reduce_rule_22(p1, p2):
    # NUMBER -> NUMBER DIGIT 
    result = Symbol()
    result.value = p1.value + p2.value

    result.type = NUMBER
    return result

def reduce_rule_23(p1):
    # NUMBER -> DIGIT 
    result = Symbol()
    result = p1
    result.type = NUMBER
    return result

def reduce_rule_24(p1):
    # COUNT -> + 
    result = Symbol()
    pattern = Pattern()
    pattern.count_min = 1
    pattern.count_max = -1
    result.pattern = pattern

    result.type = COUNT
    return result

def reduce_rule_25(p1):
    # COUNT -> * 
    result = Symbol()
    pattern = Pattern()
    pattern.count_min = 0
    pattern.count_max = -1
    result.pattern = pattern

    result.type = COUNT
    return result

def reduce_rule_26(p1):
    # COUNT -> ? 
    result = Symbol()
    pattern = Pattern()
    pattern.count_min = 0
    pattern.count_max = 1
    result.pattern = pattern

    result.type = COUNT
    return result

def reduce_rule_27(p1, p2, p3):
    # COUNT -> { NUMBER } 
    result = Symbol()
    pattern = Pattern()
    pattern.count_min = int(p2.value)
    pattern.count_max = -1
    result.pattern = pattern

    result.type = COUNT
    return result

def reduce_rule_28(p1, p2, p3, p4, p5):
    # COUNT -> { NUMBER , NUMBER } 
    result = Symbol()
    pattern = Pattern()
    pattern.count_min = int(p2.value)
    pattern.count_max = int(p4.value)
    result.pattern = pattern

    result.type = COUNT
    return result

# Embedded Actions
