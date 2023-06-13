from examples.regex.regex_parser_table import *
from examples.regex.regex_parser import parse
from examples.regex.regex_lexer import RegExLexer

class RegEx:
    def __init__(self):
        self.list_symbol = []
        self.lexer = RegExLexer()
        self.pattern = None

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
                child = pattern.child

                while child is not None:
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
                    child = child.next
            elif pattern.type == PatternType.GROUP:
                child: Pattern
                child = pattern.child
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
                
                child1 = pattern.child
                child2 = child1.next
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
