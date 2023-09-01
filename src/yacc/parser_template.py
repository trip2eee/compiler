%IMPORT%

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
%EMBEDDED_ACTIONS%
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
%REDUCE_ACTIONS%
                else:
                    node = None
                    print('reduction error')
                    break

                # Call Embedded Action Function
%EMBEDDED_ACTIONS%

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
