"""
@fn examples/regex/regex_parser.py
@brief LALR parser table generated by parser_generator.py
@date 2023-06-12 23:54:23
"""
# Definitions

class Symbol:
    def __init__(self):
        self.type = None
        self.value = None
        self.pattern = None

class Pattern:
    VALUE = 0
    RANGE = 1
    CLASS = 2
    GROUP = 3

    def __init__(self):
        self.type = Pattern.VALUE
        self.value = None
        self.range_min = None
        self.range_max = None
        self.child = None
        self.next = None
        self.count_min = 1
        self.count_max = 1
        self.matched = False
        self.matched_str = ''
        self.matched_count = 0
        self.idx_begin = 0
        self.idx_end = 0


# Parsing Table
NUM_TERMINALS = 11
NUM_NON_TERMINALS = 8
# Terminals
OR = 0
CHAR = 1
LPAREN = 2  # (
RPAREN = 3  # )
LBRACKET = 4  # [
RBRACET = 5  # ]
MINUS = 6  # -
ESC = 7
PLUS = 8  # +
TIMES = 9  # *
QUES = 10  # ?
END = 11
# Non-Terminals
CMD = 12
EXP = 13
SUBEXP = 14
GROUP = 15
CLASS = 16
TERM = 17
FACTOR = 18
COUNT = 19
CMDp = 20
# RULE table
NUM_RULES = 20 # ACCEPT in tbl_reduce
tbl_rule = [
    [20,12,],    # 0 : CMD' -> CMD 
    [12,13,],    # 1 : CMD -> EXP 
    [13,14,13,],    # 2 : EXP -> SUBEXP EXP 
    [13,14,],    # 3 : EXP -> SUBEXP 
    [13,13,0,14,],    # 4 : EXP -> EXP OR SUBEXP 
    [14,16,],    # 5 : SUBEXP -> CLASS 
    [14,1,],    # 6 : SUBEXP -> CHAR 
    [14,15,],    # 7 : SUBEXP -> GROUP 
    [14,14,19,],    # 8 : SUBEXP -> SUBEXP COUNT 
    [15,2,13,3,],    # 9 : GROUP -> ( EXP ) 
    [16,4,17,5,],    # 10 : CLASS -> [ TERM ] 
    [17,18,17,],    # 11 : TERM -> FACTOR TERM 
    [17,18,],    # 12 : TERM -> FACTOR 
    [17,18,6,],    # 13 : TERM -> FACTOR - 
    [18,1,],    # 14 : FACTOR -> CHAR 
    [18,1,6,1,],    # 15 : FACTOR -> CHAR - CHAR 
    [18,7,],    # 16 : FACTOR -> ESC 
    [19,8,],    # 17 : COUNT -> + 
    [19,9,],    # 18 : COUNT -> * 
    [19,10,],    # 19 : COUNT -> ? 
]
# SHIFT / GOTO table
# OR CHAR ( ) [ ] - ESC + * ? $ CMD EXP SUBEXP GROUP CLASS TERM FACTOR COUNT 
tbl_shift = [
    [-1, 5, 8, -1, 7, -1, -1, -1, -1, -1, -1, -1, 1, 2, 3, 6, 4, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, 5, 8, -1, 7, -1, -1, -1, 12, 13, 14, -1, -1, 10, 3, 6, 4, -1, -1, 11, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, 17, -1, -1, -1, -1, -1, 18, -1, -1, -1, -1, -1, -1, -1, -1, -1, 15, 16, -1, ],
    [-1, 5, 8, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, 19, 3, 6, 4, -1, -1, -1, ],
    [-1, 5, 8, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, 20, 6, 4, -1, -1, -1, ],
    [9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, 21, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, 17, -1, -1, -1, -1, 23, 18, -1, -1, -1, -1, -1, -1, -1, -1, -1, 22, 16, -1, ],
    [-1, -1, -1, -1, -1, -1, 24, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [9, -1, -1, 25, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, 12, 13, 14, -1, -1, -1, -1, -1, -1, -1, -1, 11, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, 26, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
]
# REDUCE / ACCEPT table
tbl_reduce = [
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 20, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, ],
    [3, -1, -1, 3, -1, -1, -1, -1, -1, -1, -1, 3, ],
    [5, 5, 5, 5, 5, -1, -1, -1, 5, 5, 5, 5, ],
    [6, 6, 6, 6, 6, -1, -1, -1, 6, 6, 6, 6, ],
    [7, 7, 7, 7, 7, -1, -1, -1, 7, 7, 7, 7, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, 2, 2, 2, 2, -1, -1, -1, -1, -1, -1, 2, ],
    [8, 8, 8, 8, 8, -1, -1, -1, 8, 8, 8, 8, ],
    [17, 17, 17, 17, 17, -1, -1, -1, 17, 17, 17, 17, ],
    [18, 18, 18, 18, 18, -1, -1, -1, 18, 18, 18, 18, ],
    [19, 19, 19, 19, 19, -1, -1, -1, 19, 19, 19, 19, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [12, -1, 12, -1, 12, 12, -1, -1, -1, -1, -1, 12, ],
    [14, 14, 14, -1, 14, 14, -1, 14, -1, -1, -1, 14, ],
    [16, 16, 16, -1, 16, 16, 16, 16, -1, -1, -1, 16, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [4, 4, 4, 4, 4, -1, -1, -1, -1, -1, -1, 4, ],
    [10, 10, 10, 10, 10, -1, -1, -1, 10, 10, 10, 10, ],
    [11, 11, 11, -1, 11, 11, -1, -1, -1, -1, -1, 11, ],
    [13, 13, 13, -1, 13, 13, -1, -1, -1, -1, -1, 13, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [9, 9, 9, 9, 9, -1, -1, -1, 9, 9, 9, 9, ],
    [15, 15, 15, -1, 15, 15, 15, 15, -1, -1, -1, 15, ],
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
    # EXP -> EXP OR SUBEXP 
    result = Symbol()
    result = p1
    result.type = EXP
    return result

def reduce_rule_5(p1):
    # SUBEXP -> CLASS 
    result = Symbol()
    result = p1
    result.type = SUBEXP
    return result

def reduce_rule_6(p1):
    # SUBEXP -> CHAR 
    result = Symbol()
    pattern = Pattern()
    pattern.type = Pattern.VALUE
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

def reduce_rule_9(p1, p2, p3):
    # GROUP -> ( EXP ) 
    result = Symbol()
    pattern = Pattern()
    pattern.type = Pattern.GROUP
    pattern.child = p2.pattern

    result.pattern = pattern

    result.type = GROUP
    return result

def reduce_rule_10(p1, p2, p3):
    # CLASS -> [ TERM ] 
    result = Symbol()
    pattern = Pattern()
    pattern.type = Pattern.CLASS
    pattern.child = p2.pattern    
    result.pattern = pattern

    result.type = CLASS
    return result

def reduce_rule_11(p1, p2):
    # TERM -> FACTOR TERM 
    result = Symbol()
    
    p1.pattern.next = p2.pattern
    result = p1

    result.type = TERM
    return result

def reduce_rule_12(p1):
    # TERM -> FACTOR 
    result = Symbol()
    result = p1
    result.type = TERM
    return result

def reduce_rule_13(p1, p2):
    # TERM -> FACTOR - 
    result = Symbol()
    result = p1
    result.type = TERM
    return result

def reduce_rule_14(p1):
    # FACTOR -> CHAR 
    result = Symbol()
    pattern = Pattern()
    pattern.type = Pattern.VALUE
    pattern.value = p1.value
    result.pattern = pattern

    result.type = FACTOR
    return result

def reduce_rule_15(p1, p2, p3):
    # FACTOR -> CHAR - CHAR 
    result = Symbol()
    pattern = Pattern()
    pattern.type = Pattern.RANGE
    pattern.range_min = p1.value
    pattern.range_max = p3.value
    result.pattern = pattern

    result.type = FACTOR
    return result

def reduce_rule_16(p1):
    # FACTOR -> ESC 
    result = Symbol()
    result = p1
    result.type = FACTOR
    return result

def reduce_rule_17(p1):
    # COUNT -> + 
    result = Symbol()
    pattern = Pattern()
    pattern.count_min = 0
    pattern.count_max = -1
    result.pattern = pattern

    result.type = COUNT
    return result

def reduce_rule_18(p1):
    # COUNT -> * 
    result = Symbol()
    pattern = Pattern()
    pattern.count_min = 1
    pattern.count_max = -1
    result.pattern = pattern

    result.type = COUNT
    return result

def reduce_rule_19(p1):
    # COUNT -> ? 
    result = Symbol()
    pattern = Pattern()
    pattern.count_min = 0
    pattern.count_max = 1
    result.pattern = pattern

    result.type = COUNT
    return result

# Embedded Actions
