from examples.regex.regex_parser_table import *


class StackElem:
    def __init__(self):
        self.node = None
        self.state = 0        

    def __str__(self):
        s = ''
        if self.node is not None:
            s += str(self.node)
        s += str(self.state)
        return s

class Parser:
    def __init__(self):
        pass

    def parse(self, list_nodes):
        result = None

        elem = StackElem()
        stack = [elem]
        state = 0

        while True:
            if len(list_nodes) > 0:
                node = list_nodes[0]

                # Call Embedded Action Function

            else:
                node = TreeNode()
                node.type = END__RESERVED

            shift = tbl_shift[state][node.type]
            reduce = tbl_reduce[state][node.type]

            # if action = shift / goto
            if shift >= 0:
                state = shift
                # print('SHIFT {}'.format(s))
                list_nodes.pop(0)

                elem = StackElem()
                elem.node = node
                elem.state = state
                stack.append(elem)

            elif reduce >= 0 and reduce < NUM_RULES:

                params = []
                for i in range(len(tbl_rule[reduce])-1):
                    p = stack.pop()
                    params.insert(0, p.node)

                state = stack[-1].state

                # Call Reduce Function
                if reduce==1:
                    node = reduce_rule_1(params[0])
                elif reduce==2:
                    node = reduce_rule_2(params[0], params[1])
                elif reduce==3:
                    node = reduce_rule_3(params[0])
                elif reduce==4:
                    node = reduce_rule_4(params[0], params[1], params[2])
                elif reduce==5:
                    node = reduce_rule_5(params[0])
                elif reduce==6:
                    node = reduce_rule_6(params[0])
                elif reduce==7:
                    node = reduce_rule_7(params[0])
                elif reduce==8:
                    node = reduce_rule_8(params[0], params[1])
                elif reduce==9:
                    node = reduce_rule_9(params[0])
                elif reduce==10:
                    node = reduce_rule_10(params[0], params[1], params[2])
                elif reduce==11:
                    node = reduce_rule_11(params[0], params[1], params[2])
                elif reduce==12:
                    node = reduce_rule_12(params[0], params[1])
                elif reduce==13:
                    node = reduce_rule_13(params[0])
                elif reduce==14:
                    node = reduce_rule_14(params[0], params[1])
                elif reduce==15:
                    node = reduce_rule_15(params[0])
                elif reduce==16:
                    node = reduce_rule_16(params[0], params[1], params[2])
                elif reduce==17:
                    node = reduce_rule_17(params[0])
                elif reduce==18:
                    node = reduce_rule_18(params[0])
                elif reduce==19:
                    node = reduce_rule_19(params[0])
                elif reduce==20:
                    node = reduce_rule_20(params[0])
                elif reduce==21:
                    node = reduce_rule_21(params[0])
                elif reduce==22:
                    node = reduce_rule_22(params[0], params[1])
                elif reduce==23:
                    node = reduce_rule_23(params[0])
                elif reduce==24:
                    node = reduce_rule_24(params[0])
                elif reduce==25:
                    node = reduce_rule_25(params[0])
                elif reduce==26:
                    node = reduce_rule_26(params[0])
                elif reduce==27:
                    node = reduce_rule_27(params[0], params[1], params[2])
                elif reduce==28:
                    node = reduce_rule_28(params[0], params[1], params[2], params[3], params[4])

                else:
                    node = None
                    print('reduction error')
                    break

                # Call Embedded Action Function


                elem = StackElem()
                elem.node = node

                # GOTO
                left_node = tbl_rule[reduce][0]
                elem.state = tbl_shift[state][left_node]

                # print('GOTO {}'.format(elem.state))
                state = elem.state

                stack.append(elem)

            elif reduce == NUM_RULES:
                # print('ACCEPT')
                elem = stack.pop()
                result = elem.node
                break
            else:
                # Error
                # Enter panic mode for error recovery.
                print('Syntax Error:')
                while shift == -1 and reduce == -1:
                    elem:StackElem
                    elem = stack.pop()

                    if elem.node is not None:
                        print(elem.node.value)

                        state = stack[-1].state
                        shift = tbl_shift[state][node.type]
                        reduce = tbl_reduce[state][node.type]

        return result
