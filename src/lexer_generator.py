"""
Lexer Generator
@author Jongmin Park (trip2eee@gmail.com)
@date 2023-06-07
"""

import enum


class LexState:
    STATE_ID = 0
    def __init__(self):
        self.id = LexState.STATE_ID     # state ID
        self.inputs = []
        self.next_states = []

        LexState.STATE_ID += 1


class LexerGenerator:
    def __init__(self):
        state0 = LexState()
        self.states = [state0]

    def open(self, lex_path):

        with open(lex_path, 'r') as f:
            pass

    