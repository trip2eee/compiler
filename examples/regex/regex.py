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
        matched = False
        matched_string = ''
        self.string = str

        for idx_begin in range(len(str)):

            # match
            substr_matched, matched_string = self.__match_substring(str, idx_begin)
            if substr_matched:
                matched = substr_matched
                break

        return matched, matched_string
    
    def __match_substring(self, str, idx_begin):
        pattern: Pattern
        pattern = self.pattern

        matched_str = ''

        idx_char = idx_begin
        matched = True
        while pattern is not None and idx_char < len(str) and matched == True:
            matched = False            

            matched, matched_c = self.__match_pattern(pattern, str, idx_char)

            if matched == False:
                break
            else:
                pattern = pattern.next
                matched_str += matched_c
                idx_char += 1
        
        return matched, matched_str
    
    def __match_pattern(self, pattern, str, idx_begin):
        final_pattern = pattern
        idx_char = idx_begin

        stack = []
        stack_parent = []

        class StackElem:
            def __init__(self):
                self.pattern = None
                self.idx_begin = 0

        # 1st path. matching child patterns
        elem = StackElem()
        elem.pattern = pattern
        elem.idx_begin = idx_begin
        stack.append(elem)

        if pattern.child is not None:
            stack_parent.append(elem)

        while len(stack) > 0:
            elem: StackElem
            elem = stack.pop()
            pattern = elem.pattern
            idx_char = elem.idx_begin
            
            pattern.matched = False
            pattern.matched_str = ''

            if pattern.child is None:
                c = str[idx_char]

                pattern.matched = False
                pattern.matched_str = c
                
                if pattern.type == Pattern.VALUE:
                    if pattern.value == c:
                        pattern.matched = True                        

                elif pattern.type == Pattern.RANGE:
                    if pattern.range_min <= c <= pattern.range_max:
                        pattern.matched = True
            else:                
                child = pattern.child

                while child is not None:
                    elem = StackElem()
                    elem.pattern = child
                    elem.idx_begin = idx_char
                    stack.append(elem)
                    child = child.sibling

                elem = StackElem()
                elem.pattern = pattern
                elem.idx_begin = idx_char
                stack_parent.append(elem)

        # 2nd path. merging child patterns
        while len(stack_parent) > 0:
            elem: StackElem
            elem = stack_parent.pop()

            pattern : Pattern
            pattern = elem.pattern

            if pattern.type == Pattern.CLASS:
                pattern.matched = False
                child = pattern.child
                while child is not None:
                    if child.matched == True:
                        pattern.matched = True
                        pattern.matched_str = child.matched_str
                    child = child.sibling
            
            if len(stack_parent) == 0:
                final_pattern = pattern

        return final_pattern.matched, final_pattern.matched_str

