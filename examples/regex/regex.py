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
        self.reduce = -1
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
        if self.reduce != -1:
            str_state += '  {}'.format(self.reduce)

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

                        else:    
                            root1 = self.copy_pattern(root)
                            prev = root1
                            while prev.next.type != PatternType.GROUP:
                                prev = prev.next

                            if prev is not None:
                                prev.next = elem

                                # if elem.next is None:
                                #     elem.count_min = next.count_min
                                #     elem.count_max = next.count_max

                            while elem.next is not None:
                                elem = elem.next

                            elem.next = next.next
                            if elem.next == elem:
                                elem.next = None
                            
                            print('push -> {}'.format(RegExUtils.symbols_to_str(root1)))
                            stack.append(root1)

                    # if next.count_min == 0:
                    #     if root != next:
                    #         root1 = self.copy_pattern(root)
                    #         prev = root1
                    #         while prev.next.type != PatternType.GROUP:
                    #             prev = prev.next
                    #         prev.next = prev.next.next
                    #         print('push -> {}'.format(RegExUtils.symbols_to_str(root1)))
                    #         stack.append(root1)
                
                # else:

                # if next.count_min == 0:
                #     # if next.type == PatternType.CLASS:
                #     if next == root:
                #         root1 = self.copy_pattern(root)
                #         root1 = root1.next

                #         if root1 is not None:
                #             print('node -> {}'.format(RegExUtils.symbols_to_str(next)))
                #             print('push -> {}'.format(RegExUtils.symbols_to_str(root1)))
                #             stack.append(root1)
                        
                #     else:
                #         root1 = self.copy_pattern(root)
                #         prev = root1

                #         while True:
                #             print('  compare : {}'.format(RegExUtils.symbol_to_str(prev.next)))
                #             print('  compare : {}'.format(RegExUtils.symbol_to_str(next)))

                #             if RegExUtils.symbol_to_str(prev.next) == RegExUtils.symbol_to_str(next):
                #                 break
                #             else:
                #                 prev = prev.next
                            
                #         prev.next = prev.next.next

                #         print('node -> {}'.format(RegExUtils.symbols_to_str(next)))
                #         print('push -> {}'.format(RegExUtils.symbols_to_str(root1)))
                #         stack.append(root1)

                next = next.next

            
            if no_split and no_group:

                str_root = RegExUtils.symbols_to_str(root)
                exists = False
                print('check existence')
                print('*   {}'.format(str_root))
                for p in list_patterns:
                    str_p = RegExUtils.symbols_to_str(p)
                    print('    {}'.format(str_p))

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
