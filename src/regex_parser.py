"""
RegEx Parser
@brief Regular Expression Parser
@author Jongmin Park (trip2eee@gmail.com)
@date 2023-06-07
"""

import enum

class State(enum.IntEnum):
    S0 = 0
    S1 = 1
    S2 = 2
    S3 = 3
    S4 = 4
    S5 = 5
    S6 = 6
    S7 = 7


class Condition:
    VALUE = 0
    RANGE = 1
    def __init__(self, type=0, value=0, min=0, max=0):
        self.type = type
        self.value = value
        self.min = min
        self.max = max

class Token:
    def __init__(self):
        self.conditions = []
        self.min_repeat = -1
        self.max_repeat = -1

class RegExParser:

    def __init__(self):
        self.state = State.S0
        self.cur_token = None
        self.tokens = []

    def parse(self, regx):

        for c in regx:
            if State.S0 == self.state:
                if c == '[':
                    self.state = State.S1
                    self.cur_token = Token()

                else:
                    self.state = State.S0
                    
                    token = Token()
                    token.conditions.append(c)
                    self.tokens.append(token)

            elif State.S1 == self.state:
                if c == ']':
                    self.state = State.S2
                elif c == '\\':
                    self.state = State.S3
                elif c == '-':
                    self.state = State.S6
                    self.cur_token.conditions.append(c)
                else:
                    self.cur_token.conditions.append(c)

            elif State.S2 == self.state:
                if c == '+':
                    self.cur_token.min_repeat = 1
                    self.cur_token.max_repeat = -1
                    self.tokens.append(self.cur_token)
                elif c =='*':
                    self.cur_token.min_repeat = 0
                    self.cur_token.max_repeat = -1
                    self.tokens.append(self.cur_token)
                elif c =='?':
                    self.cur_token.min_repeat = 0
                    self.cur_token.max_repeat = 1
                    self.tokens.append(self.cur_token)
                else:
                    self.tokens.append(self.cur_token)

                self.state = State.S0

            elif State.S6 == self.state:
                if c == ']':                    
                    self.state = State.S2
                else:
                    if self.cur_token.conditions[-1] == '-':
                        self.cur_token.conditions.pop()
                        c_first = ord(self.cur_token.conditions[-1])+1

                        c_last = ord(c)

                        for i in range(c_first, c_last+1):
                            self.cur_token.conditions.append(chr(i))
                                                
                        self.state = State.S1


    def print(self):
        t:Token
        for t in self.tokens:
            for c in t.conditions:
                print('{}'.format(c), end='')
            
            if t.min_repeat >= 0:
                print('{', end='')
                if t.max_repeat == -1:
                    print('{}, inf'.format(t.min_repeat), end='')
                else:
                    print('{}, {}'.format(t.min_repeat, t.max_repeat), end='')
                print('}', end='')
            print(' ', end='')

        print('')