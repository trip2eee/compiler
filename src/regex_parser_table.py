"""
@fn ./src/regex_parser_table.py
@brief LALR parser table generated by parser_generator.py
@date 2023-06-09 15:41:51
"""
NUM_TERMINALS = 9
NUM_NON_TERMINALS = 6
# Terminals
LPAR = 0
RPAR = 1
CHAR = 2
MINUS = 3
LBR = 4
RBR = 5
PLUS = 6
TIMES = 7
QUES = 8
END = 9
# Non-Terminals
CMD = 10
EXP = 11
GROUP = 12
TERM = 13
FACTOR = 14
REPEAT = 15
CMDp = 16
# RULE table
NUM_RULES = 17
tbl_rule = [
    [16,10,],    # 0 : CMD' -> CMD 
    [10,11,],    # 1 : CMD -> EXP 
    [11,11,13,],    # 2 : EXP -> EXP TERM 
    [11,11,12,],    # 3 : EXP -> EXP GROUP 
    [11,13,],    # 4 : EXP -> TERM 
    [11,12,],    # 5 : EXP -> GROUP 
    [12,0,13,1,],    # 6 : GROUP -> LPAR TERM RPAR 
    [12,0,13,1,15,],    # 7 : GROUP -> LPAR TERM RPAR REPEAT 
    [13,13,14,],    # 8 : TERM -> TERM FACTOR 
    [13,14,],    # 9 : TERM -> FACTOR 
    [14,2,],    # 10 : FACTOR -> CHAR 
    [14,2,3,2,],    # 11 : FACTOR -> CHAR MINUS CHAR 
    [14,4,13,5,],    # 12 : FACTOR -> LBR TERM RBR 
    [14,4,13,5,15,],    # 13 : FACTOR -> LBR TERM RBR REPEAT 
    [15,6,],    # 14 : REPEAT -> PLUS 
    [15,7,],    # 15 : REPEAT -> TIMES 
    [15,8,],    # 16 : REPEAT -> QUES 
]
# SHIFT / GOTO table
# LPAR RPAR CHAR MINUS LBR RBR PLUS TIMES QUES $ CMD EXP GROUP TERM FACTOR REPEAT 
tbl_shift = [
    [6, -1, 7, -1, 8, -1, -1, -1, -1, -1, 1, 2, 4, 3, 5, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [6, -1, 7, -1, 8, -1, -1, -1, -1, -1, -1, -1, 10, 9, 5, -1, ],
    [-1, -1, 7, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, 11, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, 7, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, 12, 5, -1, ],
    [-1, -1, -1, 13, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, 7, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, 14, 5, -1, ],
    [-1, -1, 7, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, 11, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, 15, 7, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, 11, -1, ],
    [-1, -1, 16, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, 7, -1, 8, 17, -1, -1, -1, -1, -1, -1, -1, -1, 11, -1, ],
    [-1, -1, -1, -1, -1, -1, 19, 20, 21, -1, -1, -1, -1, -1, -1, 18, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, 19, 20, 21, -1, -1, -1, -1, -1, -1, 22, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
]
# REDUCE / ACCEPT table
tbl_reduce = [
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 17, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 1, ],
    [4, -1, -1, -1, -1, -1, -1, -1, -1, 4, ],
    [5, -1, 5, -1, 5, -1, -1, -1, -1, 5, ],
    [9, 9, 9, -1, 9, 9, -1, -1, -1, 9, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [10, 10, 10, -1, 10, 10, -1, -1, -1, 10, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [2, -1, -1, -1, -1, -1, -1, -1, -1, 2, ],
    [3, -1, 3, -1, 3, -1, -1, -1, -1, 3, ],
    [8, 8, 8, -1, 8, 8, -1, -1, -1, 8, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
    [6, -1, 6, -1, 6, -1, -1, -1, -1, 6, ],
    [11, 11, 11, -1, 11, 11, -1, -1, -1, 11, ],
    [12, 12, 12, -1, 12, 12, -1, -1, -1, 12, ],
    [7, -1, 7, -1, 7, -1, -1, -1, -1, 7, ],
    [14, 14, 14, -1, 14, 14, -1, -1, -1, 14, ],
    [15, 15, 15, -1, 15, 15, -1, -1, -1, 15, ],
    [16, 16, 16, -1, 16, 16, -1, -1, -1, 16, ],
    [13, 13, 13, -1, 13, 13, -1, -1, -1, 13, ],
]