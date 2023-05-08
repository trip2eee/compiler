"""
Syntax Tree
@author Jongmin Park (trip2eee@gmail.com)
@date 2023-05-08
"""

import enum
from src.scanner import *

class NodeKind(enum.IntEnum):
    NONE = 0
    STMT = 1
    EXP = 2

class StmtKind(enum.IntEnum):
    NONE = 0
    IF = 1
    FOR = 2
    WHILE = 3
    ASSIGN = 4
    READ = 5
    WRITE = 6

class ExpKind(enum.IntEnum):
    NONE = 0
    OP = 1
    CONST = 2
    ID = 3

class ExpType(enum.IntEnum):
    NONE = 0
    VOID = 1
    BOOLEAN = 2
    INTEGER = 3
    FLOAT = 4
    DOUBLE = 5

class TreeNode:
    MAX_CHILDREN = 3
    def __init__(self):
        self.child = [None] * TreeNode.MAX_CHILDREN
        self.sibling = None
        self.node_kind = NodeKind.NONE
        self.stmt_kind = StmtKind.NONE
        self.exp_kind = ExpKind.NONE
        self.op = TokenType.UNDEF
        self.integer = 0
        self.float = 0.0
        self.string = ""
        self.exp_type = ExpType.NONE
        
