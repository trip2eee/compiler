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
            matched_pattern = self.__match_substring(str, idx_begin)
            if matched_pattern is not None:
                self.matched.append(matched_pattern.matched_str)
                idx_begin = matched_pattern.idx_end + 1
            else:
                idx_begin += 1
        
        return self.matched
    
    def __match_substring(self, str, idx_begin):
        pattern: Pattern
        pattern = self.pattern
        pattern.matched_str = ''
        matched_pattern = None

        idx_char = idx_begin

        while pattern is not None and idx_char < len(str):
            pattern.idx_begin = idx_char
            self.__match_pattern(pattern, str, pattern.next)

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
    
    
    def __match_pattern(self, pattern: Pattern, str, next_pattern=None):
        
        pattern.matched_count = 0
        pattern.matched = False
        pattern.matched_str = ''
        idx_char = pattern.idx_begin
        matched = False

        while (pattern.matched_count < pattern.count_max or pattern.count_max == -1) and idx_char < len(str):
            matched = False
            c = str[idx_char]

            if pattern.type == Pattern.VALUE and pattern.value == c:
                matched = True
                pattern.idx_end = idx_char
                pattern.matched_str += c
            elif pattern.type == Pattern.NOT_VALUE and pattern.value != c:
                matched = True
                pattern.idx_end = idx_char
                pattern.matched_str += c
            elif pattern.type == Pattern.RANGE and pattern.range_min <= c <= pattern.range_max:
                matched = True
                pattern.idx_end = idx_char
                pattern.matched_str += c
            elif pattern.type == Pattern.CLASS:
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
            elif pattern.type == Pattern.GROUP:
                child: Pattern
                child = pattern.child
                idx_child_begin = idx_char
                while child is not None:

                    child.idx_begin = idx_child_begin
                    self.__match_pattern(child, str, child.next)

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

            elif pattern.type == Pattern.OR:
                
                child1 = pattern.child
                child2 = child1.next
                child1.idx_begin = idx_char
                self.__match_pattern(child1, str, next_pattern)

                child2.idx_begin = idx_char
                self.__match_pattern(child2, str, next_pattern)

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

                if next_pattern is not None:
                    npattern = next_pattern
                    npattern.idx_begin = pattern.idx_end+1
                    while npattern is not None:
                        self.__match_pattern(npattern, str)
                        if npattern.matched:
                            if npattern.next is not None:
                                npattern.next.idx_begin = npattern.idx_end+1
                            npattern = npattern.next
                        else:
                            break
                    if npattern is None:
                        break
            else:
                break

        if pattern.matched_count >= max(1, pattern.count_min):
            pattern.matched = True
