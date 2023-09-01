%IMPORT%

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
%EMBEDDED_ACTIONS%
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
%REDUCE_ACTIONS%
                else:
                    symbol = None
                    print('reduction error')
                    break

                # Call Embedded Action Function
%EMBEDDED_ACTIONS%

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
                print('Syntax Error:')
                while shift == -1 and reduce == -1:
                    elem:StackElem
                    elem = stack.pop()

                    if elem.symbol is not None:
                        print(elem.symbol.value)

                        state = stack[-1].state
                        shift = tbl_shift[state][symbol.type]
                        reduce = tbl_reduce[state][symbol.type]

        return result
