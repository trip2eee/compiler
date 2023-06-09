from examples.c_minus.cmm_parser_table import *


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

class Parser:
    def __init__(self):
        pass

    def parse(self, list_symbols):
        result = None

        elem = StackElem()
        stack = [elem]
        state = 0

        while True:
            if len(list_symbols) > 0:
                symbol = list_symbols[0]

                # Call Embedded Action Function

            else:
                symbol = Symbol()
                symbol.type = END__RESERVED

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

                # Call Reduce Function
                if reduce==1:
                    symbol = reduce_rule_1(params[0])
                elif reduce==2:
                    symbol = reduce_rule_2(params[0])
                elif reduce==3:
                    symbol = reduce_rule_3(params[0], params[1])
                elif reduce==4:
                    symbol = reduce_rule_4(params[0])
                elif reduce==5:
                    symbol = reduce_rule_5(params[0])
                elif reduce==6:
                    symbol = reduce_rule_6(params[0], params[1])
                elif reduce==7:
                    symbol = reduce_rule_7(params[0])
                elif reduce==8:
                    symbol = reduce_rule_8(params[0])
                elif reduce==9:
                    symbol = reduce_rule_9(params[0])
                elif reduce==10:
                    symbol = reduce_rule_10(params[0], params[1], params[2], params[3], params[4], params[5], params[6])
                elif reduce==11:
                    symbol = reduce_rule_11(params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], params[9], params[10])
                elif reduce==12:
                    symbol = reduce_rule_12(params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], params[9], params[10])
                elif reduce==13:
                    symbol = reduce_rule_13(params[0])
                elif reduce==14:
                    symbol = reduce_rule_14(params[0], params[1], params[2])
                elif reduce==15:
                    symbol = reduce_rule_15(params[0])
                elif reduce==16:
                    symbol = reduce_rule_16(params[0])
                elif reduce==17:
                    symbol = reduce_rule_17(params[0])
                elif reduce==18:
                    symbol = reduce_rule_18(params[0])
                elif reduce==19:
                    symbol = reduce_rule_19(params[0])
                elif reduce==20:
                    symbol = reduce_rule_20(params[0])
                elif reduce==21:
                    symbol = reduce_rule_21(params[0], params[1], params[2])
                elif reduce==22:
                    symbol = reduce_rule_22(params[0])
                elif reduce==23:
                    symbol = reduce_rule_23(params[0], params[1], params[2])
                elif reduce==24:
                    symbol = reduce_rule_24(params[0])
                elif reduce==25:
                    symbol = reduce_rule_25(params[0])
                elif reduce==26:
                    symbol = reduce_rule_26(params[0], params[1], params[2])
                elif reduce==27:
                    symbol = reduce_rule_27(params[0])
                elif reduce==28:
                    symbol = reduce_rule_28(params[0])
                elif reduce==29:
                    symbol = reduce_rule_29(params[0])
                elif reduce==30:
                    symbol = reduce_rule_30(params[0])
                elif reduce==31:
                    symbol = reduce_rule_31(params[0])
                elif reduce==32:
                    symbol = reduce_rule_32(params[0], params[1], params[2])

                else:
                    symbol = None
                    print('reduction error')
                    break

                # Call Embedded Action Function


                elem = StackElem()
                elem.symbol = symbol

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
                # Error
                # Enter panic mode for error recovery.
                while shift == -1 and reduce == -1:
                    elem:StackElem
                    elem = stack.pop()
                    print(elem.symbol.value)

                    state = stack[-1].state
                    shift = tbl_shift[state][symbol.type]
                    reduce = tbl_reduce[state][symbol.type]

        return result
