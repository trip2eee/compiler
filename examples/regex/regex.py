from examples.regex.regex_parser_table import *
from examples.regex.regex_parser import parse
from examples.regex.regex_lexer import RegExLexer

class RegExUtils:

    @staticmethod
    def symbol_to_str(pattern:Pattern):
        s = ''

        if pattern is not None:
            if pattern.type == PatternType.VALUE:
                if pattern.value == '\n':
                    s += '\\n'
                else:
                    s += pattern.value
            elif pattern.type == PatternType.NOT_VALUE:
                if pattern.value == '\n':
                    s += '.'
                else:
                    s += '^' + pattern.value

            elif pattern.type == PatternType.RANGE:
                s += pattern.range_min + '-' + pattern.range_max

            elif pattern.type == PatternType.OR:
                for i in range(len(pattern.childs)):
                    if i > 0:
                        s += '|'
                    s += RegExUtils.symbol_to_str(pattern.childs[i])
            elif pattern.type == PatternType.CLASS:
                s += '['
                child : Pattern
                for child in pattern.childs:
                    s += RegExUtils.symbol_to_str(child)
                s += ']'
                    
            if pattern.count_min != 1 or pattern.count_max != 1:
                if pattern.count_min == 0 and pattern.count_max == 1:
                    s += '{0,1}'
                elif pattern.count_min == 0 and pattern.count_max == -1:
                    s += '{0}'
                elif pattern.count_min == 1 and pattern.count_max == -1:
                    s += '{1}'
                else:
                    s += '{'
                    s += '{},{}'.format(pattern.count_min, pattern.count_max)
                    s += '}'
        
        return s

    @staticmethod
    def symbols_to_str(pattern:Pattern, ws=True, trace_next=True):

        s = ''
        while pattern is not None:
            
            if pattern.type == PatternType.VALUE:
                if pattern.value == '\n':
                    s += '\\n'
                else:
                    s += pattern.value
            elif pattern.type == PatternType.NOT_VALUE:
                if pattern.value == '\n':
                    s += '.'
                else:
                    s += '^' + pattern.value

            elif pattern.type == PatternType.RANGE:
                s += pattern.range_min + '-' + pattern.range_max

            elif pattern.type == PatternType.CLASS:
                s += '['
                child : Pattern
                for child in pattern.childs:
                    s += RegExUtils.symbols_to_str(child, trace_next=False)
                s += ']'

            elif pattern.type == PatternType.GROUP:
                s += '('
                child : Pattern
                child = pattern.childs[0]
                if child is not None:
                    s += RegExUtils.symbols_to_str(child)
                s += ')'
            elif pattern.type == PatternType.OR:
                for i in range(len(pattern.childs)):
                    if i > 0:
                        s += '|'
                    s += RegExUtils.symbols_to_str(pattern.childs[i], ws=False)

            if pattern.count_min != 1 or pattern.count_max != 1:
                if pattern.count_min == 0 and pattern.count_max == 1:
                    s += '{0,1}'
                elif pattern.count_min == 0 and pattern.count_max == -1:
                    s += '{0}'
                elif pattern.count_min == 1 and pattern.count_max == -1:
                    s += '{1}'
                else:
                    s += '{'
                    s += '{},{}'.format(pattern.count_min, pattern.count_max)
                    s += '}'

            pattern = pattern.next

            if trace_next == False:
                break

            if ws:
                s += ' '
        return s
    
class RegExState:
    STATE_ID = 0
    def __init__(self):
        self.id = RegExState.STATE_ID
        RegExState.STATE_ID += 1

        self.list_rules = []
        self.shift_forward = {}
        self.shift_backward = {}
        self.accept = -1
        self.prev_state = -1
        self.count = 0

    def __str__(self):
        str_state = ''
        str_state += 'S{}\n'.format(self.id)

        for rule in self.list_rules:
            str_state += '  {}:  {}\n'.format(rule.id, str(rule))

        str_state += '  SHIFT FORWARD\n'
        for key in self.shift_forward:
            str_key = RegExUtils.symbol_to_str(key)
            str_state += '  {} -> {}\n'.format(str_key, self.shift_forward[key])
        
        str_state += '  SHIFT BACKWARD\n'
        for key in self.shift_backward:
            str_key = RegExUtils.symbol_to_str(key)
            str_state += '  {} -> {}\n'.format(str_key, self.shift_backward[key])

        str_state += '  REDUCE\n'
        if self.accept != -1:
            str_state += '  {}'.format(self.accept)

        return str_state

class RegExRule:
    RULE_ID = 0
    def __init__(self):
        self.id = RegExRule.RULE_ID
        RegExRule.RULE_ID += 1
        self.symbols = []
        self.mark = 0

    def copy(self):
        new_rule = RegExRule()
        RegExRule.RULE_ID -= 1
        new_rule.id = self.id
        new_rule.mark = self.mark
        for s in self.symbols:
            new_rule.symbols.append(s)
    
        return new_rule
    
    def set_pattern(self, pattern):
        self.symbols = []
        p = pattern
        while p is not None:
            self.symbols.append(p)
            p = p.next
    
    def mark_symbol(self):
        if self.mark < len(self.symbols):
            return self.symbols[self.mark]
        else:
            return None

    def __str__(self):
        str_rule = ''
        m = '_'
        for i in range(len(self.symbols)):
            if i > 0:
                str_rule += ' '
            
            if i == self.mark:
                str_rule += m
            str_rule += RegExUtils.symbol_to_str(self.symbols[i])
        if self.mark >= len(self.symbols):
            str_rule += m
            
        return str_rule
    
class RegEx:
    def __init__(self):
        self.list_symbol = []
        self.lexer = RegExLexer()
        self.pattern = None
        self.list_patterns = []
        self.list_terminals = []
        self.utils = RegExUtils()

        RegExState.STATE_ID = 0

    def set_pattern(self, expr):
        list_symbol = self.lexer.lexer(expr)
        result = parse(list_symbol)
        
        self.pattern = result.pattern

    def match(self, str):
        self.string = str
        self.matched = []

        idx_begin = 0
        while idx_begin < len(str):

            # match
            matched_pattern = self.__match_substring(self.pattern, str, idx_begin)
            if matched_pattern is not None:
                self.matched.append(matched_pattern.matched_str)
                idx_begin = matched_pattern.idx_end + 1
            else:
                idx_begin += 1

        return self.matched
    
    def __match_substring(self, pattern, str, idx_begin):
        pattern: Pattern
        pattern.matched_str = ''
        matched_pattern = None
        idx_char = idx_begin

        while pattern is not None and idx_char < len(str):
            pattern.idx_begin = idx_char
            self.__match_pattern(pattern, str)

            if pattern.matched:
                if matched_pattern is None:
                    matched_pattern = pattern
                else:
                    matched_pattern.matched_str += pattern.matched_str
                matched_pattern.idx_end = pattern.idx_end

                idx_char = pattern.idx_end + 1
                pattern = pattern.next
            else:
                if pattern.count_min == 0:
                    pattern = pattern.next
                else:
                    matched_pattern = None
                    break
        
        while pattern is not None:
            if pattern.count_min > 0:
                matched_pattern = None
                break
            pattern = pattern.next

        return matched_pattern
    
    
    def __match_pattern(self, pattern: Pattern, str):

        pattern.matched_count = 0
        pattern.matched = False
        pattern.matched_str = ''
        idx_char = pattern.idx_begin
        matched = False

        while (pattern.matched_count < pattern.count_max or pattern.count_max == -1) and idx_char < len(str):
            matched = False
            c = str[idx_char]

            if pattern.type == PatternType.VALUE and pattern.value == c:
                matched = True
                pattern.idx_end = idx_char
                pattern.matched_str += c
            elif pattern.type == PatternType.NOT_VALUE and pattern.value != c:
                matched = True
                pattern.idx_end = idx_char
                pattern.matched_str += c
            elif pattern.type == PatternType.RANGE and pattern.range_min <= c <= pattern.range_max:
                matched = True
                pattern.idx_end = idx_char
                pattern.matched_str += c
            elif pattern.type == PatternType.CLASS:
                child: Pattern

                for child in pattern.childs:
                    child.count_min = max(1, pattern.count_min)
                    child.count_max = pattern.count_max

                    child.idx_begin = idx_char
                    self.__match_pattern(child, str)

                    if child.matched:
                        matched = True
                        pattern.matched_str += child.matched_str
                        pattern.idx_end = child.idx_end
                        idx_char = child.idx_end
                        break

            elif pattern.type == PatternType.GROUP:
                child: Pattern
                child = pattern.childs[0]
                idx_child_begin = idx_char
                while child is not None:

                    child.idx_begin = idx_child_begin
                    self.__match_pattern(child, str)

                    if child.matched:
                        matched = True
                        pattern.matched_str += child.matched_str
                        pattern.idx_end = child.idx_end
                        idx_char = child.idx_end
                        idx_child_begin = idx_char + 1
                        child = child.next
                    else:
                        if child.count_min == 0:
                            child = child.next
                        else:
                            matched = False
                            break

            elif pattern.type == PatternType.OR:
                
                child1 = pattern.childs[0]
                child2 = pattern.childs[1]
                child1.idx_begin = idx_char
                self.__match_pattern(child1, str)

                child2.idx_begin = idx_char
                self.__match_pattern(child2, str)

                if child1.matched and child2.matched:
                    matched = True
                    if child1.idx_end > child2.idx_end:
                        pattern.matched_str += child1.matched_str
                        pattern.idx_end = child1.idx_end
                    else:
                        pattern.matched_str += child2.matched_str
                        pattern.idx_end = child2.idx_end

                elif child1.matched:
                    matched = True
                    pattern.matched_str += child1.matched_str
                    pattern.idx_end = child1.idx_end
                elif child2.matched:
                    matched = True
                    pattern.matched_str += child2.matched_str
                    pattern.idx_end = child2.idx_end
                else:
                    matched = False

            if matched:
                pattern.matched_count += 1                
                idx_char += 1

                if pattern.next is not None and ((pattern.matched_count >= pattern.count_min and pattern.matched_count < pattern.count_max) or pattern.count_max == -1):
                    follow = pattern.next
                    follow.idx_begin = pattern.idx_end+1
                    while follow is not None:
                        self.__match_pattern(follow, str)
                        if follow.matched:
                            if follow.next is not None:
                                follow.next.idx_begin = follow.idx_end+1
                            follow = follow.next
                        else:
                            break
                    if follow is None:
                        break
            else:
                break

        if pattern.matched_count >= max(1, pattern.count_min):
            pattern.matched = True


    def copy_pattern(self, pattern:Pattern):
        if pattern is not None:
            cp = Pattern()
            cp.type = pattern.type
            cp.value = pattern.value
            cp.range_min = pattern.range_min
            cp.range_max = pattern.range_max
            cp.count_min = pattern.count_min
            cp.count_max = pattern.count_max

            cp.next = self.copy_pattern(pattern.next)
            for c in pattern.childs:
                cp.childs.append(self.copy_pattern(c))
        else:
            cp = None

        return cp

    def is_leaf(self, pattern: Pattern):
        if pattern.next is None and len(pattern.childs) == 0:
            return True
        else:
            return False

    def augment_rules(self, pattern: Pattern, level=0, parent=None):

        list_patterns = []
        stack = []
        stack.append(pattern)

        while len(stack) > 0:
            root = stack.pop()

            print('POP {}'.format(RegExUtils.symbols_to_str(root)))

            no_split = True
            no_group = True
            next:Pattern
            next = root
        
            while next is not None:

                if next.type == PatternType.OR:
                    print('OR {}'.format(RegExUtils.symbols_to_str(next)))

                    if next.next is not None:
                        print(' - next {}'.format(RegExUtils.symbols_to_str(next.next)))

                    print(' - child1 {}'.format(RegExUtils.symbols_to_str(next.childs[0])))
                    print(' - child2 {}'.format(RegExUtils.symbols_to_str(next.childs[1])))


                    terminal = False
                    if self.is_leaf(next.childs[0]) and self.is_leaf(next.childs[1]):
                        print(' -- Leaf OR')

                        terminal = True
                    elif next.childs[1].type == PatternType.OR:
                        if self.is_leaf(next.childs[1].childs[0]) and self.is_leaf(next.childs[1].childs[1]):
                            print(' -- Leaf OR 2')
                            c1 = next.childs[1].childs[0]
                            c2 = next.childs[1].childs[1]
                            next.childs[1] = c1
                            next.childs.append(c2)
                            terminal = True

                    if terminal == False:
                        no_split = False

                        if root == next:
                            child1 = self.copy_pattern(next.childs[0])
                            child2 = self.copy_pattern(next.childs[1])
                            stack.append(child1)
                            stack.append(child2)
                            
                            while child1.next is not None:
                                child1 = child1.next
                            child1.next = next.next

                            while child2.next is not None:
                                child2 = child2.next
                            child2.next = next.next

                            print('push -> {}'.format(RegExUtils.symbols_to_str(child1)))
                            print('push -> {}'.format(RegExUtils.symbols_to_str(child2)))

                        else:
                            for child in next.childs:
                                root1 = self.copy_pattern(root)
                                child_next = root1
                                
                                while child_next.next.type != PatternType.OR:
                                    child_next = child_next.next
                                
                                if child_next is not None:
                                    child_next.next = child
                                    child_next.next.next = next.next

                                stack.append(root1)
                                print('push -> {}'.format(RegExUtils.symbols_to_str(root1)))

                            # root2 = self.copy_pattern(root)

                            # child_next = root2
                            
                            # while child_next.next.type != PatternType.OR:
                            #     child_next = child_next.next

                            # if child_next is not None:
                            #     child_next.next = next.childs[1]
                            
                            # stack.append(root2)
                            # print('push2 -> {}'.format(RegExUtils.symbols_to_str(root2)))

                elif next.type == PatternType.GROUP:
                    print('GROUP {}'.format(RegExUtils.symbols_to_str(next)))
                    if next.next is not None:
                        print(' - next {}'.format(RegExUtils.symbols_to_str(next.next)))

                    no_group = False
                    # if next.next is None:
                    #     print('next.next == None')
                    #     for child in next.childs:
                    #         stack.append(child)
                    #         print('push -> {}'.format(RegExUtils.symbols_to_str(child)))
                    # else:

                    list_group_elem, no_split_elem = self.augment_rules(next.childs[0], level+1, next)
                    if no_split_elem == False:
                        no_split = False

                    for elem in list_group_elem:

                        if root == next:
                            print('push -> {}'.format(RegExUtils.symbols_to_str(elem)))
                            stack.append(elem)

                            while elem.next is not None:
                                elem = elem.next
                            elem.next = next.next

                            # prevent cyclic link
                            if elem.next == elem:
                                elem.next = None

                        else:    
                            root1 = self.copy_pattern(root)
                            prev = root1
                            while prev.next.type != PatternType.GROUP:
                                prev = prev.next

                            if prev is not None:
                                prev.next = elem

                            while elem.next is not None:
                                elem = elem.next
                            elem.next = next.next
                            
                            # prevent cyclic link
                            if elem.next == elem:
                                elem.next = None
                            
                            print('push -> {}'.format(RegExUtils.symbols_to_str(root1)))
                            stack.append(root1)

                next = next.next
            
            if no_split and no_group:

                str_root = RegExUtils.symbols_to_str(root)
                exists = False
                # print('check existence')
                # print('*   {}'.format(str_root))
                for p in list_patterns:
                    str_p = RegExUtils.symbols_to_str(p)
                    # print('    {}'.format(str_p))

                    if str_root == str_p:
                        exists = True
                        break

                if exists == False:
                    list_patterns.append(root)

            if level == 0:
                self.list_patterns = list_patterns
        return list_patterns, (no_split and no_group)

    
    def find_terminals(self):
        
        terminal_types = [PatternType.VALUE, PatternType.NOT_VALUE, PatternType.RANGE, PatternType.CLASS, PatternType.OR]
        
        self.list_terminals = []
        for pattern in self.list_patterns:
            node = pattern
            while node is not None:

                if node.type in terminal_types:
                    str_node = RegExUtils.symbol_to_str(node)
                    exists = False
                    for t in self.list_terminals:
                        str_t = RegExUtils.symbol_to_str(t)
                        if str_node == str_t:
                            exists = True
                            break
                    if exists == False:
                        self.list_terminals.append(node)

                node = node.next
        
        return self.list_terminals

    def compile(self, expr):
        list_symbol = self.lexer.lexer(expr)
        result = parse(list_symbol)
        
        self.pattern = result.pattern
        self.list_pattern, _ = self.augment_rules(self.pattern)
        self.list_terminals = self.find_terminals()
        self.list_states = self.create_states(self.list_pattern, self.list_terminals)
    

        
    def check_inclusion(self, set_pattern:Pattern, elem_pattern:Pattern):
        result = True

        if set_pattern.type == PatternType.RANGE:
            if elem_pattern.type == PatternType.VALUE:
                if set_pattern.range_min <= elem_pattern.value <= set_pattern.range_max:
                    result = True
                else:
                    result = False
            elif elem_pattern.type == PatternType.NOT_VALUE:
                if set_pattern.range_min <= elem_pattern.value <= set_pattern.range_max:
                    result = False
                else:
                    result = True

            elif elem_pattern.type == PatternType.CLASS:
                result = False
                for c in elem_pattern.childs:
                    result_child = self.check_inclusion(set_pattern, c)
                    if result_child == True:
                        result = True
                        break
        
        elif set_pattern.type == PatternType.VALUE:
            if elem_pattern.type == PatternType.VALUE:
                if set_pattern.value == elem_pattern.value:
                    result = True
                else:
                    result = False
            
            elif elem_pattern.type == PatternType.NOT_VALUE:
                if set_pattern.value != elem_pattern.value:
                    result = True
                else:
                    result = False
            
            else:
                result = False
        
        elif set_pattern.type == PatternType.NOT_VALUE:
            if elem_pattern.type == PatternType.VALUE:
                if set_pattern.value != elem_pattern.value:
                    result = True
                else:
                    result = False
            
            elif elem_pattern.type == PatternType.NOT_VALUE:
                if set_pattern.value == elem_pattern.value:
                    result = True
                else:
                    result = False
            
            else:
                result = False

        elif set_pattern.type == PatternType.OR or set_pattern.type == PatternType.CLASS:
            result = False
            for child in set_pattern.childs:
                result_child = self.check_inclusion(child, elem_pattern)
                if result_child == True:
                    result = True
                    break


        return result

    def match_char(self, pattern:Pattern, char):

        result = False
        if pattern is not None:
            if pattern.type == PatternType.VALUE:
                if pattern.value == char:
                    result = True
                else:
                    result = False

            elif pattern.type == PatternType.NOT_VALUE:
                if pattern.value != char:
                    result = True
                else:
                    result = False
                
            elif pattern.type == PatternType.RANGE:
                if pattern.range_min <= char <= pattern.range_max:
                    result = True
                else:
                    result = False
                
            elif pattern.type == PatternType.OR or pattern.type == PatternType.CLASS:
                for child in pattern.childs:
                    result_child = self.match_char(child, char)
                    if result_child == True:
                        result = True
                        break

        return result


    def create_states(self, list_pattern, list_terminals):
        state0 = RegExState()
        for pattern in list_pattern:
            rule = RegExRule()
            rule.set_pattern(pattern)
            state0.list_rules.append(rule)

        list_states = [state0]

        for state in list_states:
            for t in list_terminals:
                str_t = RegExUtils.symbol_to_str(t)
                new_state = RegExState()
                new_state.prev_state = state.id
                
                rule:RegExRule
                for rule in state.list_rules:
                    mark_symbol = rule.mark_symbol()
                    if mark_symbol is not None:
                                        
                        str_mark = RegExUtils.symbol_to_str(mark_symbol)

                        if str_t == str_mark:
                            rule_copy = rule.copy()
                            rule_copy.mark += 1
                            new_state.list_rules.append(rule_copy)

                            # Forward Transition
                            ext = False
                            for key in state.shift_forward:
                                str_key = RegExUtils.symbol_to_str(key)
                                if str_key == str_mark:
                                    ext = True
                                    break
                            if ext == False:
                                state.shift_forward[mark_symbol] = new_state.id

                            # Backward Transition
                            if rule.mark >= 1:
                                
                                # print('backward test')
                                # print(rule)

                                if state.prev_state >= 0:
                                    for prev_rule in list_states[state.prev_state].list_rules:
                                        if prev_rule.mark >= 2:

                                            count_max = prev_symbol = rule.symbols[rule.mark-2].count_max

                                            if count_max > 1 or count_max == -1:
                                                # check if the mark symbol can be included in the previous symbol
                                                prev_symbol = rule.symbols[rule.mark-2]
                                                cur_symbol = rule.symbols[rule.mark-1]

                                                # print('prev. symbol : ' + RegExUtils.symbol_to_str(prev_symbol))
                                                # print('cur. symbol : ' + RegExUtils.symbol_to_str(cur_symbol))

                                                included = self.check_inclusion(prev_symbol, cur_symbol)

                                                if included:
                                                    state.shift_backward[prev_symbol] = state.prev_state
                    else:
                        # Reduce
                        if state.accept == -1:
                            state.accept = rule.id
                        else:
                            if state.accept != rule.id:
                                print('ERROR: ACCEPT - ACCEPT Conflict!')

                if len(new_state.list_rules) > 0:
                    list_states.append(new_state)
                else:
                    RegExState.STATE_ID -= 1

        for state in list_states:
            print(state)

        return list_states


    def match_dfa(self, str):
        
        list_matched = []
        list_states = self.list_states

        for state in list_states:
            for rule in state.list_rules:
                rule.matched_count = 0

        cur_state_id = 0
        idx_begin = 0
        cur_state = list_states[cur_state_id]

        idx_char = 0
        while idx_char < len(str):
            c = str[idx_char]

            if cur_state_id == 0:
                idx_begin = idx_char

            next_matched = False
            cur_matched = False

        
            for sym in cur_state.shift_forward:

                if self.match_char(sym, c):
                    cur_state_id = cur_state.shift_forward[sym]
                    cur_state = list_states[cur_state_id]
                    cur_state.count += 1

                    next_matched = True
                    break

            if next_matched == False:
                for rule in cur_state.list_rules:
                    if rule.mark >= 1:
                        cur_symbol = rule.symbols[rule.mark-1]

                        if (cur_symbol.count_max == -1 or cur_symbol.matched_count < cur_symbol.count_max) and self.match_char(cur_symbol, c):
                            cur_symbol.matched_count += 1
                            cur_matched = True
                            break

            if next_matched == False and cur_matched == False:

                # handle cases in which minimum count=0 (?, {0}, {0,M})
                if next_matched == False:
                    for rule in cur_state.list_rules:
                        mark_symbol = rule.mark_symbol()

                        if mark_symbol is not None and mark_symbol.count_min == 0:
                            cur_state_id = cur_state.shift_forward[mark_symbol]
                            cur_state = list_states[cur_state_id]
                            mark_symbol.matched_count += 1
                            idx_char -= 1
                            next_matched = True
                            break

                if next_matched == False:
                    backward = False
                    if len(cur_state.shift_backward) > 0:                
                        for s in cur_state.shift_backward:
                            if self.match_char(s, c):
                                cur_state_id = cur_state.shift_backward[s]
                                cur_state = list_states[cur_state_id]
                                s.matched_count += 1
                                idx_char -= 1
                                backward = True

                    if backward == False:
                        if cur_state.accept != -1:
                            idx_char -= 1
                            idx_end = idx_char

                            str_matched = str[idx_begin:idx_end+1]
                            list_matched.append(str_matched)

                        # return to state 0
                        cur_state_id = 0
                        cur_state = list_states[cur_state_id]
            
            idx_char += 1
        
        if cur_state.accept != -1:
            idx_char -= 1
            idx_end = idx_char
            str_matched = str[idx_begin:idx_end+1]
            list_matched.append(str_matched)

        return list_matched
