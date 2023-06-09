from examples.calc.calc_parser_table import *


class StackElem:
    def __init__(self):
        self.symbol = None
        self.state = 0        

    def __str__(self):
        s = ''
        if self.symbol is not None:
            s += str(self.symbol)
        s += str(self.state)
        return s

def parse(list_symbols):
    result = None

    elem = StackElem()
    stack = [elem]
    state = 0

    while True:
        if len(list_symbols) > 0:
            symbol = list_symbols[0]
        else:
            symbol = Symbol()
            symbol.type = END

        shift = tbl_shift[state][symbol.type]
        reduce = tbl_reduce[state][symbol.type]

        # if action = shift / goto
        if shift >= 0:
            state = shift
            # print('SHIFT {}'.format(s))
            list_symbols.pop(0)

            elem = StackElem()
            elem.symbol = symbol
            elem.state = state
            stack.append(elem)

        elif reduce >= 0 and reduce < NUM_RULES:

            params = []
            for i in range(len(tbl_rule[reduce])-1):
                p = stack.pop()
                params.insert(0, p.symbol)

            state = stack[-1].state

            elem = StackElem()
            elem.symbol = None

            # Call reduce function
            if reduce==1:
                elem.symbol = reduce_rule_1(params[0], params[1], params[2])
            elif reduce==2:
                elem.symbol = reduce_rule_2(params[0])
            elif reduce==3:
                elem.symbol = reduce_rule_3(params[0])
            elif reduce==4:
                elem.symbol = reduce_rule_4(params[0])
            elif reduce==5:
                elem.symbol = reduce_rule_5(params[0], params[1], params[2])
            elif reduce==6:
                elem.symbol = reduce_rule_6(params[0], params[1])
            elif reduce==7:
                elem.symbol = reduce_rule_7(params[0])
            elif reduce==8:
                elem.symbol = reduce_rule_8(params[0])
            elif reduce==9:
                elem.symbol = reduce_rule_9(params[0])
            elif reduce==10:
                elem.symbol = reduce_rule_10(params[0], params[1], params[2])
            elif reduce==11:
                elem.symbol = reduce_rule_11(params[0])

            else:
                print('reduction error')

            # GOTO
            left_symbol = tbl_rule[reduce][0]
            elem.state = tbl_shift[state][left_symbol]

            # print('GOTO {}'.format(elem.state))
            state = elem.state

            stack.append(elem)

        elif reduce == NUM_RULES:
            # print('ACCEPT')
            elem = stack.pop()
            result = elem.symbol
            break
        else:
            print('ERROR')

    return result
