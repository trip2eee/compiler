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
    def __init__(self, type=0, value=None, min=None, max=None):
        self.type = type
        self.value = value
        self.min = min
        self.max = max

    def __str__(self):
        if self.type == Condition.VALUE:
            if self.value == '\n':
                return '\\n'
            else:
                return str(self.value)
        else:
            return str(self.min) + "~" + str(self.max)
        
class Pattern:
    def __init__(self):
        self.conditions = []
        self.min_repeat = -1
        self.max_repeat = -1

    def __str__(self):
        s = ""

        s += '['
        for i in range(len(self.conditions)):
            if i > 0:
                s += '|'
            s += str(self.conditions[i])
        s += ']'
        
        if self.min_repeat >= 0:
            s += '{'
            if self.max_repeat == -1:
                s += '{}, inf'.format(self.min_repeat)
            else:
                s += '{}, {}'.format(self.min_repeat, self.max_repeat)
            s += '}'

        return s
    
class RegExParser:

    def __init__(self):
        self.state = State.S0
        self.cur_pattern = None
        self.patterns = []

    def add_cond_value(self, val):
        return Condition(Condition.VALUE, value=val)
    
    def parse(self, regx):
        self.state = State.S0
        self.cur_pattern = None
        self.patterns = []

        for c in regx:
            if State.S0 == self.state:
                if c == '[':
                    self.state = State.S1
                    self.cur_pattern = Pattern()
                elif c == '\\':
                    self.state = State.S7
                else:
                    self.state = State.S0
                    
                    pattern = Pattern()
                    cond = self.add_cond_value(c)
                    pattern.conditions.append(cond)

                    self.patterns.append(pattern)

            elif State.S1 == self.state:
                if c == ']':
                    self.state = State.S2
                elif c == '\\':
                    self.state = State.S3
                elif c == '-':
                    self.state = State.S6
                    cond = self.add_cond_value(c)
                    self.cur_pattern.conditions.append(cond)
                else:
                    cond = self.add_cond_value(c)
                    self.cur_pattern.conditions.append(cond)

            elif State.S2 == self.state:
                if c == '+':
                    self.cur_pattern.min_repeat = 1
                    self.cur_pattern.max_repeat = -1
                    self.patterns.append(self.cur_pattern)
                elif c =='*':
                    self.cur_pattern.min_repeat = 0
                    self.cur_pattern.max_repeat = -1
                    self.patterns.append(self.cur_pattern)
                elif c =='?':
                    self.cur_pattern.min_repeat = 0
                    self.cur_pattern.max_repeat = 1
                    self.patterns.append(self.cur_pattern)
                else:
                    self.patterns.append(self.cur_pattern)

                self.state = State.S0

            elif State.S6 == self.state:
                if c == ']':                    
                    self.state = State.S2
                else:
                    last_cond : Condition
                    last_cond = self.cur_pattern.conditions[-1]
                    if last_cond.value == '-':
                        self.cur_pattern.conditions.pop()

                        last_cond = self.cur_pattern.conditions[-1]

                        last_cond.type = Condition.RANGE
                        last_cond.min = last_cond.value
                        last_cond.max = c
                        last_cond.value = None
                        self.state = State.S1
            elif State.S7 == self.state:
                self.state = State.S0
                cond = self.add_cond_value(c)
                pattern = Pattern()
                pattern.conditions.append(cond)
                self.patterns.append(pattern)

        return self.patterns
    
    def print(self):
        pattern:Pattern
        for i in range(len(self.patterns)):
            pattern = self.patterns[i]
            if i > 0:
                print(' ', end='')
            print(str(pattern), end='')
            
        print('')