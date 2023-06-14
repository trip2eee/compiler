"""
Lexer Generator
@author Jongmin Park (trip2eee@gmail.com)
@date 2023-06-07
"""

import enum
from src.lex_parser import *

class LexState:
    ITEM_ID = 0
    def __init__(self):
        self.rules = []
        self.id = LexState.ITEM_ID
        LexState.ITEM_ID += 1

        self.shift = {}
        self.reduce = []

    def __str__(self):
        s = 'S' + str(self.id) + '\n'
        for r in self.rules:
            s += '  ' + str(r.id) + ' ' + str(r) + '\n'
        
        s += '  SHIFT\n'
        for key in self.shift:
            if self.shift[key] != -1:
                s += '  \'' + str(key) + '\' -> s' + str(self.shift[key]) + '\n'

        s += '  REDUCE\n'
        for r in self.reduce:
            s += '  r' + str(r) + '\n'

        return s
    
class LexerGenerator:
    def __init__(self):
        self.states = []
        self.lex_parser = None
        self.terminals = []

    def open(self, lex_path):

        self.lex_parser = LexParser()
        self.lex_parser.open(lex_path)

        self.rules = self.lex_parser.rules

        # print rules
        print('Rules')
        for r in self.rules:
            for c in r.string:
                if c not in self.terminals:
                    self.terminals.append(c)
            print(r)

        print('Terminals')
        for t in self.terminals:
            print('{} '.format(t), end='')
        print('')

        self.compute_items()

    def compute_items(self):
        print('compute items')

        item0 = LexState()
        for r in self.rules:
            item0.rules.append(r)

        self.states = [item0]

        for item in self.states:
            for t in self.terminals:
                item.shift[t] = -1

                new_state = None
                for r in item.rules:
                    r: Rule
                    mark_symbol = r.mark_symbol()

                    if mark_symbol is not None and mark_symbol == t:
                        if new_state is None:
                            new_state = LexState()
                        
                        r_copy = r.copy()
                        r_copy.mark += 1
                        new_state.rules.append(r_copy)

                        item.shift[t] = new_state.id

                if new_state is not None:
                    self.states.append(new_state)

            for r in item.rules:
                mark_symbol = r.mark_symbol()
                if mark_symbol is None:
                    item.reduce.append(r.id)

        for item in self.states:
            print(item)


    