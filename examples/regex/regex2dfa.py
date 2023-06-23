import sys

sys.path += '../../'
from examples.regex.regex import *
utils = RegExUtils()

# regular expression to DFA

regex = RegEx()
# regex.set_pattern('[_a-zA-Z][_a-zA-Z0-9]*')
# code = '    f32Value;    1234;    abcd'

regex.set_pattern('[+-]?((\d+([.]\d{0,10})?)|([.]\d{1,10}))[fF]{0,1}')
code = '-10. 10.321  -.123, +3.141592F, +1.234f -.321F'

# regex.set_pattern('W{1}o(r|R|k)l*d')
# code = 'Hello, World, Hello WoRld, Hello Word, Wokd'

regex.set_pattern('\/(\*(.|\n)*\*\/)|(\/.*\n)')
code = ''
code += "#include <stdio.h>\n   "
code += "/* This is a C style Comment\n *with a line change. Currently searching this pattern is not efficient. **/\n"
code += " // This is C++ style comment\n"
code += " /* comment2 */\n"
code += " /***/\n"


# regex.set_pattern('(([a-z]*)|(if))')
# code = 'ifstd11'
# code += "if(ifst == aadd)"

# TODO: To implement backward shift for /**./

print(utils.symbols_to_str(regex.pattern))
list_pattern, _ = regex.augment_rules(regex.pattern)

regex.find_terminals()
list_terminals = regex.list_terminals

print('Terminals')
for t in list_terminals:
    print(utils.symbol_to_str(t))


print('Augmented Rules')

for rule in list_pattern:
    print(utils.symbols_to_str(rule))

print('create states')

def check_inclusion(set_pattern:Pattern, elem_pattern:Pattern):
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
                result_child = check_inclusion(set_pattern, c)
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
            result_child = check_inclusion(child, elem_pattern)
            if result_child == True:
                result = True
                break


    return result

def match_char(pattern:Pattern, char):

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
                result_child = match_char(child, char)
                if result_child == True:
                    result = True
                    break

    return result


def create_states(list_pattern):
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

                                            included = check_inclusion(prev_symbol, cur_symbol)

                                            if included:
                                                state.shift_backward[prev_symbol] = state.prev_state
                else:
                    # Reduce
                    if state.reduce == -1:
                        state.reduce = rule.id
                    else:
                        if state.reduce != rule.id:
                            print('ERROR: REDUCE - REDUCE Conflict!')

            if len(new_state.list_rules) > 0:
                list_states.append(new_state)
            else:
                RegExState.STATE_ID -= 1

    for state in list_states:
        print(state)

    return list_states

print(code)

def match(list_states, str):
    list_matched = []

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

            if match_char(sym, c):
                cur_state_id = cur_state.shift_forward[sym]
                cur_state = list_states[cur_state_id]
                cur_state.count += 1

                next_matched = True
                break

        if next_matched == False:
            for rule in cur_state.list_rules:
                if rule.mark >= 1:
                    cur_symbol = rule.symbols[rule.mark-1]

                    if (cur_symbol.count_max == -1 or cur_symbol.matched_count < cur_symbol.count_max) and match_char(cur_symbol, c):
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
                        if match_char(s, c):
                            cur_state_id = cur_state.shift_backward[s]
                            cur_state = list_states[cur_state_id]
                            s.matched_count += 1
                            idx_char -= 1
                            backward = True

                if backward == False:
                    if cur_state.reduce != -1:
                        idx_char -= 1
                        idx_end = idx_char

                        str_matched = str[idx_begin:idx_end+1]
                        list_matched.append(str_matched)

                    # return to state 0
                    cur_state_id = 0
                    cur_state = list_states[cur_state_id]
        
        idx_char += 1
    
    if cur_state.reduce != -1:
        idx_char -= 1
        idx_end = idx_char
        str_matched = str[idx_begin:idx_end+1]
        list_matched.append(str_matched)

    return list_matched

list_states = create_states(list_pattern)
list_matched = match(list_states, code)

for s in list_matched:
    print(s)

