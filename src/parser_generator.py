"""
Parser Generator
@author Jongmin Park (trip2eee@gmail.com)
@date 2023-05-31
"""

EPSILON = 'ep'  # empty string epsilon

class Rule:
    def __init__(self, non_terminal):
        self.non_terminal = non_terminal
        self.strings = []   # two dimensional array of strings
        self.first = []
        self.follow = []

    def add_first(self, f):
        if f not in self.first:
            self.first.append(f)
            return 1
        else:
            return 0
        
    def add_follow(self, f):
        if f not in self.follow and f != EPSILON:
            self.follow.append(f)
            return 1
        else:
            return 0

class ParserGenerator:
    def __init__(self):
        self.rules = {}
        self.symbols = []
        self.non_terminals = []
        self.terminals = []

        self.cur_non_terminal = ''
        self.cur_rule = None

    def is_string(self, token):
        result = True
        for c in token:
            if not ('a' <= c <= 'z' or 'A' <= c <= 'Z' or c in '_+-*/()$'):
                result = False
                break
        return result

    def open(self, grammar_path):
        with open(grammar_path, 'r') as f:
            while True:
                line = f.readline()

                if line == '':
                    break
            
                tokens = line.split()
                if len(tokens) < 2:
                    continue
                
                if self.is_string(tokens[0]) and tokens[1] == ':':
                    non_terminal = tokens[0]
                    self.cur_non_terminal = non_terminal

                    if non_terminal not in self.symbols:
                        self.symbols.append(non_terminal)

                    if non_terminal not in self.non_terminals:
                        self.non_terminals.append(non_terminal)

                    rule = Rule(self.cur_non_terminal)
                    self.rules[self.cur_non_terminal] = rule
                    self.cur_rule = rule

                    string = []
                    self.cur_rule.strings.append(string)
                    for i in range(2, len(tokens)):
                        if tokens[i] == '#':
                            # if comment
                            break
                        elif tokens[i] == '{':
                            # if code
                            break
                        else:
                            string.append(tokens[i])

                            if self.is_string(tokens[i]) and tokens[i] not in self.symbols:
                                self.symbols.append(tokens[i])

                elif tokens[0] == '|':
                    string = []
                    self.cur_rule.strings.append(string)

                    for i in range(1, len(tokens)):
                        if tokens[i] == '#':
                            # if comment
                            break
                        elif tokens[i] == '{':
                            # if code
                            break
                        else:
                            string.append(tokens[i])

                            if self.is_string(tokens[i]) and tokens[i] not in self.symbols:
                                self.symbols.append(tokens[i])                
        
        for s in self.symbols:
            if s not in self.non_terminals:
                self.terminals.append(s)
        
        self.first()
        self.follow()

    def first(self):
        
        # while there are changes to any nonterminal
        num_changes = 1
        while num_changes > 0:
            num_changes = 0

            for key in self.rules:
                start_symbol = self.rules[key]

                # for each production choice
                for str in start_symbol.strings:
                    k = 0
                    s = str[k]
                    if s in self.terminals:
                        num_changes += start_symbol.add_first(s)

                    elif s in self.non_terminals:     
                        r = self.rules[s]
                        for f in r.first:
                            num_changes += start_symbol.add_first(f)

    def contain_epsilon(self, symbol):
        """check if Xk contains epsilon (empty string)
        """
        result = False
        # check if Xk contains epsilon (empty string)
        if symbol in self.non_terminals:
            for str in self.rules[symbol].strings:
                if str[0] == EPSILON:
                    result = True
                    break
            
        return result
                
    def follow(self):
        # Follow(start-symbol) = { $ }
        for key in self.rules:
            left_symbol = self.rules[key]

            append_end = False
            for str in left_symbol.strings:
                for s in str:
                    if s in self.non_terminals:
                        append_end = True
                        break

            if append_end:
                left_symbol.follow.append('$')

        # while there are changes to any follow set
        num_changes = 1
        while num_changes > 0:
            num_changes = 0

            for key in self.rules:
                left_symbol = self.rules[key]

                # for each production A -> X1 X2 ... Xn
                for str in left_symbol.strings:
                    for i in range(0, len(str)):
                        Xi = str[i]
                        
                        if Xi in self.non_terminals:
                            xk_empty = False

                            # if B -> aAb, b != empty string (epsilon), add First(b) to Follow(A)
                            n = len(str)-1
                            if i < n:
                                k = i+1                                                            
                                Xk = str[k] # Xk for k >= i+1
                                xk_empty = self.contain_epsilon(Xk)

                                if Xk in self.terminals:
                                    num_changes += self.rules[Xi].add_follow(Xk)
                                else:
                                    for f in self.rules[Xk].first:
                                        num_changes += self.rules[Xi].add_follow(f)
                        
                            # if B -> aAb, b = empty string (epsilon), which means B -> aA, add Follow(B) to Follow(A)
                            else:
                                xk_empty = True
                            
                            if xk_empty:
                                Xn = str[n]
                                if Xn in self.non_terminals:
                                    for f in left_symbol.follow:
                                        num_changes += self.rules[Xi].add_follow(f)

    def print_result(self):
        print('non-terminals')
        for s in self.non_terminals:
            print('{} '.format(s), end='')
        print('')

        print('terminals')
        for s in self.terminals:
            print('{} '.format(s), end='')
        print('')

        print('rules')

        for key in self.rules:
            r = self.rules[key]
            print(r.non_terminal, end='')
            print(' -> ', end='')
            for idx_str in range(len(r.strings)):
                for s in r.strings[idx_str]:
                    print('{} '.format(s), end='')
                if idx_str < len(r.strings)-1:
                    print(' | ', end='')
            print('')

        print('\nFirst')
        for key in self.rules:
            r = self.rules[key]
            print('First({}) = '.format(r.non_terminal), end='')
            print('{', end='')
            for f in r.first:
                print('{}, '.format(f), end='')
            print('}')

        print('\nFollow')
        for key in self.rules:
            r = self.rules[key]
            print('Follow({}) = '.format(r.non_terminal), end='')
            print('{', end='')
            for f in r.follow:
                print('{}, '.format(f), end='')
            print('}')

