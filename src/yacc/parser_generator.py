"""
Parser Generator
@author Jongmin Park (trip2eee@gmail.com)
@date 2023-05-31
"""
import enum
import time
from src.yacc.grammar_parser import GarmmarParser
from src.yacc.grammar_parser import Rule
from src.yacc.grammar_parser import EPSILON

class LRItem:
    """LR(0) Item - A production choice with a distinguished position in its right-hand side.
    """
    def __init__(self):
        self.left_symbol = ''
        self.string = []
        self.lookahead = []
        self.mark = 0   # index(position) of symbol to read
        self.rule_id = 0
        self.searched = False

    def mark_symbol(self):
        """ This method returns mark symbol (symbol to read)
        """
        if self.mark < len(self.string):
            return self.string[self.mark]
        else:
            return None

    def prev_mark_symbol(self):
        if self.mark-1 >= 0:
            return self.string[self.mark-1]
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
        """ This method converts LR(0) Item in string
            I<id>
              [RULE -> STRING, Lookaheads separated by '/']
        """
        # print rule
        str = '[ ' + self.left_symbol + ' -> '
        for idx in range(len(self.string)):
            if self.mark == idx:
                str += '.'

            str += self.string[idx]
            if idx < len(self.string)-1:
                str += ' '

        if self.mark == len(self.string):
            str += '.'

        # print Lookaheads
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
    """ Set of closure items in a state
    """
    def __init__(self):
        self.items = []        # set of closure items
        self.mark_symbols = [] # set of mark symbols of closure items.
                               # they are used in computing GOTO

    def print(self):
        for i in self.items:
            print('  ' + str(i))

    def write(self, f):
        for i in self.items:
            f.write('  ' + str(i) + '\n')

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

        return s

class State:
    STATE_ID = 0
    def __init__(self, closure:Closure):
        self.id = State.STATE_ID
        State.STATE_ID += 1

        self.closure = closure
        self.action = {}              # shift/reduce
        self.goto = {}                # The next state to transition to on nonterminals
        self.next_state_table = {}    # dictionary for next state. next_state = next_state_table[lookahead]
        self.prev_state_table = {}

    def __eq__(self, value: 'State') -> bool:
        return self.closure == value.closure

    def print(self):
        print('I{}'.format(self.id))
        self.closure.print()

    def write(self, f):
        """ This method writes state in file f.
        """
        f.write('I{}\n'.format(self.id))
        self.closure.write(f)


    def print_with_padding(self, s, len_padded=7):
        """ This method print s with leading white spaces to make padded length of string len_padded.
        """
        s_pad = s
        while len(s_pad) < len_padded:
            s_pad = ' ' + s_pad
        
        print(s_pad, end='')

    def print_table_header(self):
        """ This method prints headers with padds
            Terminal symbols, Nonterminal symbols
        """
        self.print_with_padding('|')
        
        # Action: shift and reduce actions on terminals
        for key in self.action:
            self.print_with_padding(key)

        # GOTO: The next state to transition to on nonterminals
        for key in self.goto:
            self.print_with_padding(key)

        print('')

    def print_table_row(self):
        """ This method prints actions/gotos of the state
        """
        self.print_with_padding('{}|'.format(self.id))

        # Action
        for key in self.action:
            self.print_with_padding('{}'.format(str(self.action[key])))
        # GOTO
        for key in self.goto:
            if self.goto[key] >= 0:
                self.print_with_padding('{}'.format(self.goto[key]))
            else:
                self.print_with_padding('')

        print('')

class ParserGenerator:
    """ This class generates parser
    """
    def __init__(self):
        self.rules = {}
        self.aug_rules = []
        
        self.symbols = []
        self.non_terminals = []
        self.terminals = []

        self.cur_non_terminal = ''
        self.cur_rule = None

        self.start_symbol = None    # the start symbol of program (the first non-terminal of grammar file)
        self.states = []            # List of states
        self.verbose = True

        State.STATE_ID = 0
        self.grammar_parser = None

    def open(self, grammar_path):
        
        self.grammar_parser = GarmmarParser()
        self.grammar_parser.open(grammar_path)

        self.rules = self.grammar_parser.rules
        self.start_symbol = self.grammar_parser.start_symbol
        self.symbols = self.grammar_parser.symbols
        self.non_terminals = self.grammar_parser.non_terminals
        self.terminals = self.grammar_parser.terminals
        self.list_tokens = self.grammar_parser.list_tokens
        
        self.compute_first()
        self.compute_follow()        

    def compute_first(self):
        """ This method computes first symbols
        """
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
        """ This method computes LR(0) closures.
            If I is a set of LR(0) items, CLOSURE(I) can be computed as follows
            1. All LR(0) items in I are added.
            2. If A -> X1 .X2 X3 is included in CLOSURE(I) and X2 -> X4 exists, X2 -> .X4 is added

            @param items [in] List of LR(0) items
        """
        num_changes = 1

        closure = Closure()

        for i in items:
            closure.items.append(i)

        while num_changes > 0:
            num_changes = 0

            item : LRItem
            for item in closure.items:
                if item.mark < len(item.string):
                    # symbol to read (mark symbol)
                    mark_symbol = item.mark_symbol()
                    
                    if mark_symbol not in closure.mark_symbols:
                        closure.mark_symbols.append(mark_symbol)

                    # for mark symbol A, if rules A -> X1... exist, add A -> X1...
                    if mark_symbol in self.rules:
                        rule: Rule
                        rule = self.rules[mark_symbol]

                        for str, rule_id in zip(rule.strings, rule.rule_ids):
                            # create LR(0) item with mark = 0
                            new_item = LRItem()
                            new_item.left_symbol = mark_symbol
                            new_item.string = str
                            new_item.rule_id = rule_id

                            if new_item not in closure.items:
                                closure.items.append(new_item)
                                num_changes += 1
                                # print(new_item)

        return closure

    def comptue_LR0_goto(self, closure:Closure, x):
        """ This method computes LR(0) item GOTOs.            
            If I is set of items and A -> a.Xb is in I,
            GOTO(I, x) = CLOSURE( A -> aX.b )

            @param closure [in] closure from which transition to other states on the mark item
            @param x       [in] mark item
        """
        items = []

        item: LRItem
        for item in closure.items:
            if item.mark < len(item.string) and item.string[item.mark] == x:
                new_item = item.copy()
                # A -> a.Xb ==> A -> aX.b
                new_item.mark += 1

                if new_item not in items:
                    items.append(new_item)
        
        closure = self.compute_LR0_closures(items)
        return closure

    def compute_LR0_items(self):
        """ This method computes LR(0) items (0 lookahead)
            LR(0) items: Production rules with mark '.' on the right hand side.
            1. The start of augmented rules e.g. S' -> S (kernel item).
            2. Items with mark=0 e.g. A -> .a (closure item).
            3. Items with mark=end e.g. A -> a. (reduction item).
        """
        # augmented grammar        
        self.generate_augmented_rules()
                
        rule0 = self.aug_rules[0]
        item0 = LRItem()
        item0.left_symbol = rule0.left_symbol
        item0.string = rule0.strings[0]
        
        self.start_item = item0

        start_item_accept = item0.copy()
        start_item_accept.mark += 1
        self.start_item_accept = start_item_accept

        closure = self.compute_LR0_closures([item0])
        s0 = State(closure)
        self.states.append(s0)

        if self.verbose:
            s0.print()

        state:State
        for state in self.states:
            for m in state.closure.mark_symbols:

                closure = self.comptue_LR0_goto(state.closure, m)
                new_state = State(closure)

                if new_state not in self.states:
                    if self.verbose:
                        print('GOTO(I{}, {}) = '.format(state.id, m), end='')

                    self.states.append(new_state)
                    if self.verbose:
                        new_state.print()

                    # mark the next state to be used in construction of parsing table.
                    state.next_state_table[m] = new_state.id
                    
                    if m in new_state.prev_state_table:
                        if state.id not in new_state.prev_state_table[m]:
                            new_state.prev_state_table[m].append(state.id)
                    else:
                        new_state.prev_state_table[m] = [state.id]
                else:
                    
                    new_state_id = -1
                    for idx_state in range(len(self.states)):
                        if self.states[idx_state] == new_state:
                            new_state_id = self.states[idx_state].id                            
                            break
                    
                    new_state = self.states[new_state_id]
                    # mark the next state to be used in construction of parsing table.
                    state.next_state_table[m] = new_state_id
                    
                    if m in new_state.prev_state_table:
                        if state.id not in new_state.prev_state_table[m]:
                            new_state.prev_state_table[m].append(state.id)
                    else:
                        new_state.prev_state_table[m] = [state.id]

                    if self.verbose:
                        print('GOTO(I{}, {}) = I{}'.format(state.id, m, new_state_id))

                    State.STATE_ID -= 1

    def generate_augmented_rules(self):
        # augmented grammar with numbering
        self.aug_rules = []
        rule_id = 0

        aug_rule = Rule(self.start_symbol + "'")
        aug_rule.left_symbol = self.start_symbol + "'"
        aug_rule.strings = [[self.start_symbol]]        
        aug_rule.rule_ids.append(0)
        self.aug_rules.append(aug_rule)
        rule_id += 1

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

    def clear_search_flag(self):
        for state in self.states:
            for item in state.closure.items:
                item:LRItem
                item.searched = False

    def compute_lookahead(self):
        """ This method computes lookaheads
            Lookaheads: Set of terminals that can be the next symbol.
            Lookaheads of A: First(b) for S' -> a.Ab if reduction item [A -> c.]
        """
        class SearchElem:
            def __init__(self):
                self.item = None
                self.state = None
                self.mark_symbol = None
                self.epsilon = False    # epsilon-transition flag

        state: State
        for state in self.states:
            
            if self.verbose:
                print(state.id)

            item: LRItem
            for item in state.closure.items:
                self.clear_search_flag()
                stack_search = []

                # if reduction item [ A -> a.] (dot at the end of the item)
                if item.mark == len(item.string):
                    elem = SearchElem()
                    # item.searched = True
                    elem.item = item
                    elem.state = state
                    stack_search.append(elem)

                while len(stack_search) > 0:
                    elem: SearchElem
                    elem = stack_search.pop()
                    
                    cur_item: LRItem                    
                    cur_state:State
                    cur_item = elem.item
                    cur_state = elem.state
                    
                    prev_mark_symbol = cur_item.prev_mark_symbol()
                    if prev_mark_symbol is not None and prev_mark_symbol in cur_state.prev_state_table:
                        list_prev_states = cur_state.prev_state_table[prev_mark_symbol]
                    else:
                        list_prev_states = []
                    
                    if self.verbose:
                        print('cur item: I' + str(cur_state.id) + ' ' + str(cur_item))

                    if cur_item.mark == 0:
                        # add lookahead
                        if cur_item.mark == 0 and cur_item.mark_symbol() == elem.mark_symbol:
                            idx_la = cur_item.mark+1
                            if idx_la < len(cur_item.string):
                                la = cur_item.string[idx_la]
                                if la in self.terminals:
                                    item.add_lookahead(la)
                                else:
                                    item.add_lookahead(self.rules[la].first)

                                if self.verbose:
                                    print('add first 1: I' + str(cur_state.id) + ' ' + la)
                                    if la in self.terminals:
                                        print(la)
                                    else:
                                        for f in self.rules[la].first:
                                            print('{} '.format(f), end='')
                                        print('')

                        # epsilon transition [A -> .a], [B -> .A]
                        trans_item: LRItem
                        for trans_item in cur_state.closure.items:
                            # prevent cyclic epsilon transition
                            if trans_item.mark_symbol() == cur_item.left_symbol and trans_item.left_symbol != cur_item.left_symbol:

                                new_elem = SearchElem()
                                trans_item.searched = True
                                new_elem.item = trans_item
                                new_elem.mark_symbol = cur_item.left_symbol
                                new_elem.state = cur_state
                                new_elem.epsilon = True
                                stack_search.append(new_elem)
                                
                                if self.verbose:
                                    print('epsilon transition 1: I' + str(cur_state.id) + ' ' + str(cur_item) + ' -> I' + str(cur_state.id) + ' ' + str(trans_item))

                    # transition to the previous state
                    for idx_prev_state in list_prev_states:
                        prev_state: State
                        prev_state = self.states[idx_prev_state]

                        prev_item: LRItem
                        for prev_item in prev_state.closure.items:

                            # if prev_item: [B -> .A b], cur_item: [B -> A .b]
                            if (prev_item.rule_id == cur_item.rule_id and prev_item.mark == cur_item.mark-1):                                
                                # prevent cyclic state transition
                                if prev_item.searched == False:
                                    new_elem = SearchElem()
                                    prev_item.searched = True
                                    new_elem.item = prev_item
                                    new_elem.mark_symbol = cur_item.left_symbol
                                    new_elem.state = prev_state                                    
                                    stack_search.append(new_elem)

                                    if self.verbose:
                                        print('transition : I' + str(cur_state.id) + ' ' + str(cur_item) + ' -> I' + str(prev_state.id) + ' ' + str(prev_item))
            if self.verbose:
                state.print()

    def construct_lalr_parsing_table(self):
        """ This method constructs LALR parsing table
        """
        self.compute_lookahead()

        if self.verbose:
            print('')
        
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
                    # if [A -> alpha .a beta]
                    if mark_symbol in self.terminals:
                        state.action[mark_symbol].next_state = state.next_state_table[mark_symbol]
                        state.action[mark_symbol].action = Action.SHIFT
                    else:
                        state.goto[mark_symbol] = state.next_state_table[mark_symbol]
                else:
                    # if [A -> a.]
                    mark_symbol = '$'
                    if self.start_item_accept in state.closure.items:
                        # state.action[mark_symbol] = Action()
                        state.action[mark_symbol].action = Action.ACCEPT

                    else:
                        for la in item.lookahead:
                            state.action[la].action = Action.REDUCE
                            state.action[la].reduction_rule = item.rule_id

                        # For Follow(A) of a non-terminal symbol A, reduce.
                        for f in self.rules[item.left_symbol].follow:
                            if state.action[f].action == Action.NONE:
                                state.action[f].action = Action.REDUCE
                                state.action[f].reduction_rule = item.rule_id
                            else:
                                if state.action[f].action == Action.SHIFT:
                                    print('ERROR: shift - reduce conflict')

        state: State
        state.print_table_header()
        for state in self.states:
            state.print_table_row()

        with open('state.log', 'w') as f:
            for state in self.states:
                state.write(f)

        print('done')

    def generate_parser(self, grammar_path, verbose=True):
        """ This method generate parser of grammar defined in grammar_path
            @param grammar_path [in] Grammar file path
            @param verbose      [in] Verbosity flag. If True, parser generation takes much longer time than verbose is False.
        """
        self.verbose = verbose

        self.open(grammar_path)
        self.compute_LR0_items()
        self.construct_lalr_parsing_table()
    
    def find_symbol_alias(self, symbol):
        alias = ''
        for t in self.list_tokens:
            if t.string == symbol and t.alias != '':
                alias = t.alias
                break
        return alias

    def export(self, file_path):
        """ This method exportes generated parser code.
            @param file_path [in] Path of parser to be generated
        """
        INDENT1 = '            '
        INDENT2 = '                '
        INDENT3 = '                    '

        module_name = file_path
        if module_name.endswith('.py'):
            module_name = module_name[:-3]
        parser_table_path = module_name + '_table.py'
        f = open(parser_table_path, 'w')
        
        f.write('"""\n')
        f.write('@fn {}\n'.format(file_path))
        f.write('@brief LALR parser table generated by parser_generator.py\n')

        cur_time = time.strftime('%Y-%m-%d %H:%M:%S')
        f.write('@date {}\n'.format(cur_time))
        f.write('"""\n')

        f.write('# Definitions\n')
        definition = self.grammar_parser.definition
        idx_start = definition.find('%{')
        idx_end = definition.find('%}')
        
        if idx_start >= 0 and idx_end > idx_start:            
            f.write(definition[idx_start+2:idx_end])
            f.write("\n")
        
        f.write('# Auxiliary Routines\n')
        f.write(self.grammar_parser.aux_routines)
        f.write('\n')

        f.write('# Parsing Table\n')
        symbol_table = []
        symbol_id_table = {}

        NUM_TERMINALS = len(self.terminals)
        NUM_NON_TERMINALS = len(self.non_terminals)

        # terminals
        symbol_id = 0
        for idx_rule in range(NUM_TERMINALS):
            symbol = self.terminals[idx_rule]
            symbol_table.append(symbol)
            symbol_id_table[symbol] = symbol_id
            symbol_id += 1

        symbol = 'END__RESERVED'
        symbol_table.append(symbol)
        symbol_id_table[symbol] = symbol_id
        symbol_id += 1

        # non-terminals
        for idx_rule in range(NUM_NON_TERMINALS):
            symbol = self.non_terminals[idx_rule]
            symbol_table.append(symbol)
            symbol_id_table[symbol] = symbol_id
            symbol_id += 1        

        symbol = self.aug_rules[0].left_symbol
        symbol = symbol.replace("'", "p")
        symbol_table.append(symbol)
        symbol_id_table[symbol] = symbol_id
        symbol_id += 1
        
        f.write('NUM_TERMINALS = {}\n'.format(NUM_TERMINALS))
        f.write('NUM_NON_TERMINALS = {}\n'.format(NUM_NON_TERMINALS))

        f.write('# Terminals\n')
        for idx_rule in range(NUM_TERMINALS+1):
            symbol = symbol_table[idx_rule]
            # if the symbol does not begin with special character
            if 'a' <= symbol[0] <= 'z' or 'A' <= symbol[0] <= 'Z' or symbol[0] == '_':
                f.write('{} = {}\n'.format(symbol, symbol_id_table[symbol]))

        f.write('# Non-Terminals\n')
        for idx_rule in range(NUM_TERMINALS+1, NUM_TERMINALS + NUM_NON_TERMINALS + 2):
            symbol = symbol_table[idx_rule]
            f.write('{} = {}\n'.format(symbol, symbol_id_table[symbol]))

        str_token_names = ''
        str_token_names += 'yy_token_names = {\n    '
        for i, symbol in enumerate(symbol_id_table):
            if i > 0:
                str_token_names += ', '
                if i % 10 == 0:
                  str_token_names += '\n    '

            str_token_names += "'"
            str_token_names += symbol
            str_token_names += "':"
            str_token_names += str(i)

        str_token_names += '\n}\n'

        f.write(str_token_names)

        f.write('# RULE table\n')
        NUM_RULES = len(self.aug_rules)
        f.write('NUM_RULES = {} # ACCEPT in tbl_reduce\n'.format(NUM_RULES))
        f.write('tbl_rule = [\n')
        rule: Rule
        for rule in self.aug_rules:
            f.write('    [')
            left_symbol = rule.left_symbol
            left_symbol = left_symbol.replace("'", "p")
            f.write('{},'.format(symbol_id_table[left_symbol]))
            for s in rule.strings[0]:
                f.write('{},'.format(symbol_id_table[s]))

            f.write('],    # {} : {}\n'.format(rule.rule_ids[0], str(rule)))

        f.write(']\n')

        f.write('# SHIFT / GOTO table\n')
        f.write('# ')
        for key in self.states[0].action:
            f.write('{} '.format(key))
        for key in self.states[0].goto:
            f.write('{} '.format(key))
        f.write('\n')

        f.write('tbl_shift = [\n')

        state: State
        for state in self.states:
            f.write('    [')
            for key in state.action:
                action: Action
                action = state.action[key]
                if action.action == Action.SHIFT:
                    f.write('{}, '.format(action.next_state))
                else:
                    f.write('{}, '.format(-1))

            for key in state.goto:
                f.write('{}, '.format(state.goto[key]))

            f.write('],\n')

        f.write(']\n')

        f.write('# REDUCE / ACCEPT table\n')
        f.write('tbl_reduce = [\n')
        for state in self.states:
            f.write('    [')
            for key in state.action:
                action: Action
                action = state.action[key]
                if action.action == Action.REDUCE:
                    f.write('{}, '.format(action.reduction_rule))
                elif action.action == Action.ACCEPT:
                    f.write('{}, '.format(NUM_RULES))
                else:
                    f.write('{}, '.format(-1))

            f.write('],\n')
        f.write(']\n')

        # reduce actions
        f.write('# Reduce Actions\n')
        reduce_action_calls = ''

        rule: Rule
        for key in self.rules:
            rule = self.rules[key]

            for idx_rule in range(len(rule.rule_ids)):
                rule_id = rule.rule_ids[idx_rule]

                action_code = rule.reduce_actions[idx_rule]
                
                idx_nl = 0
                while idx_nl < (len(action_code)-1) and action_code[idx_nl] == '\n':
                    idx_nl += 1
                action_code = action_code[idx_nl:]

                f.write('def reduce_rule_{}('.format(rule_id))
                for idx_arg in range(len(rule.strings[idx_rule])):
                    if idx_arg > 0:
                        f.write(', ')
                    f.write('p{}'.format(idx_arg + 1))
                f.write('):\n')
                
                # Comment
                f.write('    # ' + str(self.aug_rules[rule_id]) + '\n')

                if action_code == '':
                    action_code = '    $$ = $1'

                action_code = action_code.replace('$$', 'result')
                action_code = action_code.replace('$', 'p')

                action_code += '\n    result.type = {}'.format(rule.left_symbol)
                action_code += '\n    return result\n'

                action_code = action_code.replace('$', 'p')

                f.write(action_code)
                f.write('\n')

                if rule_id == 1:
                    reduce_action_calls += INDENT2 + 'if reduce=={}:\n'.format(rule_id)
                else:
                    reduce_action_calls += INDENT2 + 'elif reduce=={}:\n'.format(rule_id)

                reduce_action_calls += INDENT3 + 'node = reduce_rule_{}('.format(rule_id)
                for idx_arg in range(len(rule.strings[idx_rule])):
                    if idx_arg > 0:
                        reduce_action_calls += ', '
                    reduce_action_calls += 'params[{}]'.format(idx_arg)
                reduce_action_calls += ')\n'

        # embedded actions
        f.write('# Embedded Actions\n')
        embedded_action_calls = ''
        embedded_actions = self.grammar_parser.embedded_action
        for key in embedded_actions:
            action_code = embedded_actions[key]

            if action_code != '':
                f.write('def embedded_{}(p1):\n'.format(key))

                if '$$' in action_code:
                    action_code = action_code.replace('$$', 'result')
                    action_code = action_code.replace('$', 'p')
                    action_code += '\n    return result\n'
                else:
                    action_code = action_code.replace('$', 'p')

                f.write(action_code)
                f.write('\n')

                embedded_action_calls += INDENT2 + 'if node.type=={}:\n'.format(key)
                embedded_action_calls += INDENT3 + 'embedded_{}(node)\n'.format(key)

        f.close()

        import_path = module_name
        import_path = import_path.replace('/', '.')
        import_path = import_path.replace('\\', '.')
        import_table = 'from ' + import_path + '_table import *\n'

        f = open('src/yacc/parser_template.py', 'r')
        parser_template = f.read()
        f.close()

        parser_template = parser_template.replace('%IMPORT%', import_table)
        parser_template = parser_template.replace('%REDUCE_ACTIONS%', reduce_action_calls)
        parser_template = parser_template.replace('%EMBEDDED_ACTIONS%', embedded_action_calls)

        f = open(module_name + '.py', 'w')
        f.write(parser_template)
        f.close()

    def parse_string(self, input):
        input = input.split()
            
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

            if action.action == Action.SHIFT:
                s = action.next_state
                print('SHIFT {}'.format(s))
                input.pop(0)

                e = StackElem()
                e.symbol = token
                e.state = s
                stack.append(e)

            elif action.action == Action.REDUCE:
                
                rule_id = action.reduction_rule
                rule: Rule
                rule = self.aug_rules[rule_id]
                
                print('REDUCE {}'.format(rule_id))

                for i in range(len(rule.strings[0])):
                    stack.pop()
                s = stack[-1].state

                e = StackElem()
                e.symbol = rule.left_symbol
                e.state = self.states[s].goto[rule.left_symbol]

                print('GOTO {}'.format(e.state))
                s = e.state

                stack.append(e)

            elif action.action == Action.ACCEPT:
                print('ACCEPT')
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

