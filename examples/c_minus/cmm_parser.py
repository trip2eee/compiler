from examples.c_minus.cmm_parser_table import *


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
                    node = reduce_rule_4(params[0])
                elif reduce==5:
                    node = reduce_rule_5(params[0])
                elif reduce==6:
                    node = reduce_rule_6(params[0])
                elif reduce==7:
                    node = reduce_rule_7(params[0], params[1], params[2])
                elif reduce==8:
                    node = reduce_rule_8(params[0], params[1], params[2], params[3], params[4])
                elif reduce==9:
                    node = reduce_rule_9(params[0], params[1], params[2], params[3], params[4], params[5])
                elif reduce==10:
                    node = reduce_rule_10(params[0], params[1], params[2], params[3], params[4], params[5])
                elif reduce==11:
                    node = reduce_rule_11(params[0], params[1], params[2], params[3], params[4])
                elif reduce==12:
                    node = reduce_rule_12(params[0])
                elif reduce==13:
                    node = reduce_rule_13(params[0])
                elif reduce==14:
                    node = reduce_rule_14(params[0])
                elif reduce==15:
                    node = reduce_rule_15(params[0])
                elif reduce==16:
                    node = reduce_rule_16(params[0])
                elif reduce==17:
                    node = reduce_rule_17(params[0])
                elif reduce==18:
                    node = reduce_rule_18(params[0], params[1], params[2])
                elif reduce==19:
                    node = reduce_rule_19(params[0])
                elif reduce==20:
                    node = reduce_rule_20(params[0], params[1])
                elif reduce==21:
                    node = reduce_rule_21(params[0], params[1], params[2], params[3], params[4])
                elif reduce==22:
                    node = reduce_rule_22(params[0], params[1], params[2])
                elif reduce==23:
                    node = reduce_rule_23(params[0], params[1])
                elif reduce==24:
                    node = reduce_rule_24(params[0])
                elif reduce==25:
                    node = reduce_rule_25(params[0])
                elif reduce==26:
                    node = reduce_rule_26(params[0])
                elif reduce==27:
                    node = reduce_rule_27(params[0])
                elif reduce==28:
                    node = reduce_rule_28(params[0])
                elif reduce==29:
                    node = reduce_rule_29(params[0])
                elif reduce==30:
                    node = reduce_rule_30(params[0])
                elif reduce==31:
                    node = reduce_rule_31(params[0])
                elif reduce==32:
                    node = reduce_rule_32(params[0], params[1])
                elif reduce==33:
                    node = reduce_rule_33(params[0])
                elif reduce==34:
                    node = reduce_rule_34(params[0], params[1], params[2], params[3], params[4])
                elif reduce==35:
                    node = reduce_rule_35(params[0], params[1], params[2], params[3], params[4], params[5], params[6])
                elif reduce==36:
                    node = reduce_rule_36(params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8])
                elif reduce==37:
                    node = reduce_rule_37(params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7])
                elif reduce==38:
                    node = reduce_rule_38(params[0], params[1], params[2], params[3], params[4])
                elif reduce==39:
                    node = reduce_rule_39(params[0], params[1], params[2])
                elif reduce==40:
                    node = reduce_rule_40(params[0])
                elif reduce==41:
                    node = reduce_rule_41(params[0], params[1], params[2])
                elif reduce==42:
                    node = reduce_rule_42(params[0])
                elif reduce==43:
                    node = reduce_rule_43(params[0])
                elif reduce==44:
                    node = reduce_rule_44(params[0])
                elif reduce==45:
                    node = reduce_rule_45(params[0])
                elif reduce==46:
                    node = reduce_rule_46(params[0])
                elif reduce==47:
                    node = reduce_rule_47(params[0])
                elif reduce==48:
                    node = reduce_rule_48(params[0])
                elif reduce==49:
                    node = reduce_rule_49(params[0], params[1], params[2])
                elif reduce==50:
                    node = reduce_rule_50(params[0])
                elif reduce==51:
                    node = reduce_rule_51(params[0], params[1], params[2])
                elif reduce==52:
                    node = reduce_rule_52(params[0], params[1], params[2], params[3], params[4], params[5])
                elif reduce==53:
                    node = reduce_rule_53(params[0])
                elif reduce==54:
                    node = reduce_rule_54(params[0])
                elif reduce==55:
                    node = reduce_rule_55(params[0], params[1], params[2])
                elif reduce==56:
                    node = reduce_rule_56(params[0])
                elif reduce==57:
                    node = reduce_rule_57(params[0])
                elif reduce==58:
                    node = reduce_rule_58(params[0])
                elif reduce==59:
                    node = reduce_rule_59(params[0])
                elif reduce==60:
                    node = reduce_rule_60(params[0], params[1])
                elif reduce==61:
                    node = reduce_rule_61(params[0], params[1])
                elif reduce==62:
                    node = reduce_rule_62(params[0])
                elif reduce==63:
                    node = reduce_rule_63(params[0], params[1], params[2], params[3])
                elif reduce==64:
                    node = reduce_rule_64(params[0], params[1])
                elif reduce==65:
                    node = reduce_rule_65(params[0], params[1])
                elif reduce==66:
                    node = reduce_rule_66(params[0], params[1], params[2])
                elif reduce==67:
                    node = reduce_rule_67(params[0])
                elif reduce==68:
                    node = reduce_rule_68(params[0])
                elif reduce==69:
                    node = reduce_rule_69(params[0], params[1], params[2])
                elif reduce==70:
                    node = reduce_rule_70(params[0], params[1], params[2], params[3])
                elif reduce==71:
                    node = reduce_rule_71(params[0])
                elif reduce==72:
                    node = reduce_rule_72(params[0], params[1], params[2])

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
                first_node = None
                error_code = ''
                while shift == -1 and reduce == -1 and len(stack) > 0:
                    elem:StackElem
                    elem = stack.pop()

                    if elem.node is not None:
                        error_code = elem.node.text + ' ' + error_code
                        first_node = elem.node

                        state = stack[-1].state
                        shift = tbl_shift[state][node.type]
                        reduce = tbl_reduce[state][node.type]
                
                print('Syntax Error [Line:{}, Col:{}] '.format(first_node.idx_line, first_node.idx_col), end='')
                print(error_code)

                if len(stack) == 0:
                    break

        return result
