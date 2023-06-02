"""
Parser Generator
@author Jongmin Park (trip2eee@gmail.com)
@date 2023-05-31
"""
import enum

EPSILON = 'ep'  # empty string epsilon

class Rule:
    def __init__(self, non_terminal):
        self.left_symbol = non_terminal
        self.strings = []   # two dimensional array of strings
        self.rule_ids = []  # IDs of rules
        self.first = []
        self.follow = []

    def __str__(self):
        str = self.left_symbol
        str += ' -> '
        
        for idx_str in range(len(self.strings)):
            for s in self.strings[idx_str]:
                str += s + ' '
            if idx_str < len(self.strings)-1:
                str += '| '

        return str
    
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

    def print_first(self):
        print('First({}) = '.format(self.left_symbol), end='')
        print('{', end='')
        for f in self.first:
            print('{}, '.format(f), end='')
        print('}')
    
    def print_follow(self):
        print('Follow({}) = '.format(self.left_symbol), end='')
        print('{', end='')
        for f in self.follow:
            print('{}, '.format(f), end='')
        print('}')

class LRItem:
    """LR(0) Item
    """
    def __init__(self):
        self.left_symbol = ''
        self.string = []
        self.lookahead = []
        self.mark = 0   # index of symbol to read
        self.rule_id = 0

    def mark_symbol(self):
        if self.mark < len(self.string):
            return self.string[self.mark]
        else:
            return None

    def is_lookahead_empty(self):
        return len(self.lookahead) == 0
    
    def add_lookahead(self, la):
        if isinstance(la, list):
            for s in la:
                if s not in self.lookahead:
                    self.lookahead.append(s)
        else:
            if la not in self.lookahead:
                self.lookahead.append(la)

    def set_string(self, str):
        self.string = []
        for s in str:
            self.string.append(s)

    def __str__(self):
        str = '[ ' + self.left_symbol + ' -> '
        for idx in range(len(self.string)):
            if self.mark == idx:
                str += '.'

            str += self.string[idx]
            if idx < len(self.string)-1:
                str += ' '

        if self.mark == len(self.string):
            str += '.'

        str += ', '
        if len(self.lookahead) == 0:
            str += '$'
        else:
            for i in range(len(self.lookahead)):
                if i != 0:
                    str += '/'
                str += self.lookahead[i]
                
        str += ']'

        return str
    
    def __eq__(self, value: 'LRItem') -> bool:
        result = True

        if (self.left_symbol == value.left_symbol) and (self.mark == value.mark):
            if (len(self.string) == len(value.string)) and (len(self.lookahead) == len(value.lookahead)):
                for i in range(len(self.string)):
                    if self.string[i] != value.string[i]:
                        result = False
                        break

                if result:
                    for i in range(len(self.lookahead)):
                        if self.lookahead[i] != value.lookahead[i]:
                            result = False
                            break
            else:
                result = False
        else:
            result = False

        return result
    
    def copy(self):
        new_item = LRItem()
        new_item.left_symbol = self.left_symbol
        
        for s in self.string:
            new_item.string.append(s)
        for l in self.lookahead:
            new_item.lookahead.append(l)
        new_item.mark = self.mark
        new_item.rule_id = self.rule_id

        return new_item

class Closure:
    def __init__(self):
        self.items = []
        self.mark_symbols = []

    def print(self):
        for i in self.items:
            print('  ' + str(i))

        # next_state = self.id+1
        # for m in self.mark_symbols:
        #     print('  -- ' + m + ' --> I' + str(next_state))
        #     next_state += 1

    def __eq__(self, value: 'Closure') -> bool:
        result = True

        if len(self.items) == len(value.items):
            for i in range(len(self.items)):
                if self.items[i] != value.items[i]:
                    result = False
                    break
        else:
            result = False

        return result

class Action:
    NONE   = ''
    SHIFT  = 's'
    REDUCE = 'r'
    ACCEPT = 'a'

    def __init__(self):
        self.next_state = 0
        self.reduction_rule = 0
        self.action = Action.NONE

    def __str__(self):
        
        if self.action == Action.SHIFT:
            s = self.action + str(self.next_state)
        elif self.action == Action.REDUCE:
            s = self.action + str(self.reduction_rule)
        elif self.action == Action.ACCEPT:
            s = self.action        
        else:
            s = ''
        
        while len(s) < 5:
            s += ' '
        return s

class StackElem:
    def __init__(self):
        self.symbol = None
        self.state = 0        

    def __str__(self):
        s = ''
        if self.symbol is not None:
            s += self.symbol
        s += str(self.state)
        return s

class State:
    STATE_ID = 0
    def __init__(self, closure:Closure):
        self.id = State.STATE_ID
        State.STATE_ID += 1

        self.closure = closure
        self.action = {}
        self.goto = {}
        self.next_state_table = {}    # dictionary for next state. next_state = next_state_table[lookahead]

    def __eq__(self, value: 'State') -> bool:
        return self.closure == value.closure

    def print(self):
        print('I{}'.format(self.id))
        self.closure.print()


    def print_table_row(self):
        print('{:5d} |'.format(self.id), end='')

        # action
        for key in self.action:
            print('{} '.format(str(self.action[key])), end='')
        # goto
        for key in self.goto:
            if self.goto[key] >= 0:
                print('{:5d} '.format(self.goto[key]), end='')
            else:
                print('      ', end='')

        print('')

class ParserGenerator:
    def __init__(self):
        self.rules = {}
        self.aug_rules = []
        
        self.symbols = []
        self.non_terminals = []
        self.terminals = []

        self.cur_non_terminal = ''
        self.cur_rule = None

        self.start_symbol = None
        self.states = []        # List of states

        State.STATE_ID = 0

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

                    #  TODO: To check definition of the start symbol
                    if self.start_symbol is None:
                        self.start_symbol = non_terminal

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
        
        self.compute_first()
        self.compute_follow()        

    def compute_first(self):
        
        # while there are changes to any nonterminal
        num_changes = 1
        while num_changes > 0:
            num_changes = 0

            for key in self.rules:
                left_symbol = self.rules[key]

                # for each production choice
                for str in left_symbol.strings:
                    k = 0
                    s = str[k]
                    if s in self.terminals:
                        num_changes += left_symbol.add_first(s)

                    elif s in self.non_terminals:     
                        r = self.rules[s]
                        for f in r.first:
                            num_changes += left_symbol.add_first(f)

    def epsilon_in_first(self, symbol):
        """check if Xk has epsilon (empty string) in its first
        """
        result = False
        if symbol in self.non_terminals:
            if EPSILON in self.rules[symbol].first:
                result = True

        return result
                
    def compute_follow(self):
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
                                Xk = str[i+1] # Xk for k >= i+1
                                xk_empty = self.epsilon_in_first(Xk)

                                if Xk in self.terminals:
                                    num_changes += self.rules[Xi].add_follow(Xk)
                                else:
                                    for f in self.rules[Xk].first:
                                        num_changes += self.rules[Xi].add_follow(f)
                            else:
                                xk_empty = True
                            
                            if xk_empty:
                                # if B -> aAb, b = empty string (epsilon), which means B -> aA, add Follow(B) to Follow(A)
                                # because the follow set of B can be follow set of aA.
                                Xn = str[n]
                                if Xn in self.non_terminals:
                                    for f in left_symbol.follow:
                                        num_changes += self.rules[Xi].add_follow(f)

    def compute_LR0_closures(self, items) -> Closure:
        num_changes = 1

        closure = Closure()
        for i in items:
            closure.items.append(i)
            # print(i)

        while num_changes > 0:
            num_changes = 0

            item : LRItem
            for item in closure.items:
                if item.mark < len(item.string):
                    # symbol to read (mark symbol)
                    mark_symbol = item.string[item.mark]

                    if mark_symbol not in closure.mark_symbols:
                        closure.mark_symbols.append(mark_symbol)

                    # for mark symbol A, if rules A -> X1... exist, add A -> X1...
                    if mark_symbol in self.rules:
                        rule: Rule
                        rule = self.rules[mark_symbol]

                        for str in rule.strings:
                            new_item = LRItem()
                            new_item.left_symbol = mark_symbol
                            new_item.string = str
                                                        
                            if new_item not in closure.items:
                                closure.items.append(new_item)
                                num_changes += 1
                                # print(new_item)

        return closure

    def comptue_LR0_goto(self, closure:Closure, x):
        items = []

        item: LRItem
        for item in closure.items:
            if item.mark < len(item.string) and item.string[item.mark] == x:
                new_item = item.copy()
                new_item.mark += 1

                if new_item not in items:
                    items.append(new_item)
        
        closure = self.compute_LR0_closures(items)
        return closure

    def compute_LR0_items(self):
        """ This method computes LR(0) items
        """
        # augmented grammar        
        aug_rule = Rule(self.start_symbol + "'")
        aug_rule.left_symbol = self.start_symbol + "'"
        aug_rule.strings = [[self.start_symbol]]

        print(aug_rule)
        
        item0 = LRItem()
        item0.left_symbol = aug_rule.left_symbol
        item0.string = aug_rule.strings[0]
        
        closure = self.compute_LR0_closures([item0])
        s0 = State(closure)
        self.states.append(s0)

        s0.print()

        state:State
        for state in self.states:
            for m in state.closure.mark_symbols:

                closure = self.comptue_LR0_goto(state.closure, m)
                new_state = State(closure)

                if new_state not in self.states:
                    print('GOTO(I{}, {}) = '.format(state.id, m), end='')

                    self.states.append(new_state)
                    new_state.print()
                else:

                    next_state_id = -1
                    for idx_state in range(len(self.states)):
                        if self.states[idx_state] == new_state:
                            next_state_id = self.states[idx_state].id
                            break

                    print('GOTO(I{}, {}) = I{}'.format(state.id, m, next_state_id))

                    State.STATE_ID -= 1


    def compute_LR1_closures(self, items) -> Closure:        
        """ This method computes LR(1) closures
        """
        closure = Closure()
        for i in items:
            closure.items.append(i)
            # print(i)

        changed = True
        while changed:
            changed = False

            item : LRItem
            for item in closure.items:
                if item.mark < len(item.string):
                    # symbol to read (mark symbol)
                    mark_symbol = item.string[item.mark]

                    if mark_symbol not in closure.mark_symbols:
                        closure.mark_symbols.append(mark_symbol)

                    # for mark symbol A, if rules A -> X1... exist, add A -> X1...
                    if mark_symbol in self.rules:
                        rule: Rule
                        rule = self.rules[mark_symbol]

                        for str, rule_id in zip(rule.strings, rule.rule_ids):
                            new_item = LRItem()
                            new_item.left_symbol = mark_symbol
                            new_item.string = str
                            new_item.rule_id = rule_id
                            new_item.add_lookahead(item.lookahead)

                            if item.mark+1 < len(item.string):
                                la = item.string[item.mark+1]
                                if la in self.terminals:
                                    new_item.add_lookahead(la)
                                else:
                                    new_item.add_lookahead(self.rules[la].first)

                                for la in item.lookahead:
                                    if la in self.terminals:
                                        new_item.add_lookahead(la)
                                    else:
                                        new_item.add_lookahead(self.rules[la].first)

                            if new_item not in closure.items:
                                closure.items.append(new_item)
                                changed = True
                                # print(new_item)

        return closure

    def comptue_LR1_goto(self, closure:Closure, x):
        """GOTO for computing LR(1) items
        """
        items = []

        item: LRItem
        for item in closure.items:
            if item.mark < len(item.string) and item.string[item.mark] == x:
                new_item = item.copy()
                new_item.mark += 1

                if new_item not in items:
                    items.append(new_item)
        
        closure = self.compute_LR1_closures(items)
        return closure
    
    def compute_LR1_items(self):
        """ This method computes LR(1) items
        """
        # augmented grammar with numbering
        self.aug_rules = []
        rule_id = 0

        aug_rule = Rule(self.start_symbol + "'")
        aug_rule.left_symbol = self.start_symbol + "'"
        aug_rule.strings = [[self.start_symbol]]        
        aug_rule.rule_ids.append(0)
        self.aug_rules.append(aug_rule)
        rule_id += 1

        print(aug_rule)

        # assign rule IDs
        for key in self.rules:
            r:Rule
            r = self.rules[key]
            for s in r.strings:
                r.rule_ids.append(rule_id)                

                ar = Rule(r.left_symbol)
                ar.strings = [s]
                ar.rule_ids = [rule_id]
                self.aug_rules.append(ar)

                rule_id += 1

        item0 = LRItem()
        item0.left_symbol = aug_rule.left_symbol
        item0.string = aug_rule.strings[0]

        self.start_item = item0

        start_item_accept = item0.copy()
        start_item_accept.mark += 1
        self.start_item_accept = start_item_accept

        closure = self.compute_LR1_closures([item0])
        s0 = State(closure)
        self.states.append(s0)
        s0.print()

        changed = True
        while changed:
            changed = False

            state:State
            for state in self.states:
                for m in state.closure.mark_symbols:

                    closure = self.comptue_LR1_goto(state.closure, m)
                    new_state = State(closure)

                    if new_state not in self.states:
                        print('GOTO(I{}, {}) = '.format(state.id, m), end='')                        
                        self.states.append(new_state)

                        # mark the next state to be used in construction of parsing table.
                        state.next_state_table[m] = new_state.id

                        new_state.print()
                        # changed = True
                    else:

                        next_state_id = -1
                        for idx_state in range(len(self.states)):
                            if self.states[idx_state] == new_state:
                                next_state_id = self.states[idx_state].id
                                break
                        
                        state.next_state_table[m] = next_state_id
                        print('GOTO(I{}, {}) = I{}'.format(state.id, m, next_state_id))

                        State.STATE_ID -= 1

    def construct_clr_parsing_table(self):
        """ This method constructs CLR parsing table
        """
        state: State
        for state in self.states:
            
            for t in self.terminals:
                state.action[t] = Action()
            state.action['$'] = Action()
            
            for n in self.non_terminals:
                state.goto[n] = -1
                
            item: LRItem
            for item in state.closure.items:
                mark_symbol = item.mark_symbol()
                
                if mark_symbol is not None:
                    if mark_symbol in self.terminals:
                        # state.action[mark_symbol] = Action()
                        state.action[mark_symbol].next_state = state.next_state_table[mark_symbol]
                        state.action[mark_symbol].action = Action.SHIFT
                    else:
                        state.goto[mark_symbol] = state.next_state_table[mark_symbol]
                
                else:
                    mark_symbol = '$'
                    if self.start_item_accept in state.closure.items:
                        # state.action[mark_symbol] = Action()
                        state.action[mark_symbol].action = Action.ACCEPT

                    else:
                        for lk in item.lookahead:
                            state.action[lk].action = Action.REDUCE
                            state.action[lk].reduction_rule = item.rule_id
                        if item.is_lookahead_empty():
                            state.action['$'].action = Action.REDUCE
                            state.action['$'].reduction_rule = item.rule_id

            state.print_table_row()        
        print('done')

    def construct_lalr_parsing_table(self):
        """ This method constructs LALR parsing table
        """
        pass

    def parse_string(self, input):
        input = input.split()

        e = StackElem()
        stack = [e]
        s = 0

        while True:            
            if len(input) > 0:
                token = input[0]
            else:
                token = '$'
            
            action:Action
            action = self.states[s].action[token]
            # print(str(action))

            if action.action == Action.SHIFT:
                s = action.next_state

                print('shift {}'.format(s))

                input.pop(0)

                e = StackElem()
                e.symbol = token
                e.state = s
                stack.append(e)
            
            elif action.action == Action.REDUCE:
                
                rule_id = action.reduction_rule
                rule: Rule
                rule = self.aug_rules[rule_id]
                
                print('reduce {}'.format(rule_id))

                for i in range(len(rule.strings[0])):
                    stack.pop()
                s = stack[-1].state

                e = StackElem()
                e.symbol = rule.left_symbol                
                e.state = self.states[s].goto[rule.left_symbol]

                print('goto {}'.format(e.state))
                s = e.state

                stack.append(e)

            elif action.action == Action.ACCEPT:
                print('accept')
                break
        
            for e in stack:
                print(str(e), end='')
            print('')




    def print_nonterminals(self):
        print('Non-terminals')
        for s in self.non_terminals:
            print('{} '.format(s), end='')
        print('')
    
    def print_terminals(self):
        print('Terminals')
        for s in self.terminals:
            print('{} '.format(s), end='')
        print('')
    
    def print_rules(self):
        print('Rules')
        for key in self.rules:
            r = self.rules[key]
            print(r)
        print('')
    
    def print_first_follow(self):
        print('First set')
        for key in self.rules:
            r:Rule
            r = self.rules[key]  
            r.print_first()          

        print('')
        print('Follow set')
        for key in self.rules:
            r:Rule
            r = self.rules[key]
            r.print_follow()

