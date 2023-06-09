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

    e = StackElem()
    stack = [e]
    s = 0

    while True:
        if len(list_symbols) > 0:
            symbol = list_symbols[0]
        else:
            symbol = Symbol()
            symbol.type = END

        shift = tbl_shift[s][symbol.type]
        reduce = tbl_reduce[s][symbol.type]

        # if action = shift / goto
        if shift >= 0:
            s = shift
            # print('SHIFT {}'.format(s))
            list_symbols.pop(0)

            e = StackElem()
            e.symbol = symbol
            e.state = s
            stack.append(e)

        elif reduce >= 0 and reduce < NUM_RULES:

            # print('REDUCE {}'.format(reduce))

            params = []
            for i in range(len(tbl_rule[reduce])-1):
                p = stack.pop()
                params.insert(0, p.symbol)

            s = stack[-1].state

            e = StackElem()
            e.symbol = None

            # call reduce function
            p = params
            if reduce==1:
                e.symbol = reduce_rule_1(p[0], p[1], p[2])
            elif reduce==2:
                e.symbol = reduce_rule_2(p[0])
            elif reduce==3:
                e.symbol = reduce_rule_3(p[0])
            elif reduce==4:
                e.symbol = reduce_rule_4(p[0])
            elif reduce==5:
                e.symbol = reduce_rule_5(p[0], p[1], p[2])
            elif reduce==6:
                e.symbol = reduce_rule_6(p[0])
            elif reduce==7:
                e.symbol = reduce_rule_7(p[0])
            elif reduce==8:
                e.symbol = reduce_rule_8(p[0])
            elif reduce==9:
                e.symbol = reduce_rule_9(p[0], p[1], p[2])
            elif reduce==10:
                e.symbol = reduce_rule_10(p[0])
            else:
                print('ERROR!')

            # GOTO
            left_symbol = tbl_rule[reduce][0]
            e.state = tbl_shift[s][left_symbol]

            # print('GOTO {}'.format(e.state))
            s = e.state

            stack.append(e)

        elif reduce == NUM_RULES:
            # print('ACCEPT')
            e = stack.pop()
            result = e.symbol
            break
        else:
            print('ERROR')

        # for e in stack:
        #     print(str(e), end='')
        # print('')

    return result
