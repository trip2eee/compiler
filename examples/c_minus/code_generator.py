"""
@brief C-- p-code generator
@author Jongmin Park (trip2eee@gmail.com)
@date September 4, 2023
"""

from examples.c_minus.cmm_parser_table import *

class SymbolType(enum.IntEnum):
    VARIABLE = 0
    ARRAY = 1
    FUNCTION = 2
    TYPE = 3
    STD_FUNCTION = 4

class SymbolInfo:
    def __init__(self, type:TreeNode, name:TreeNode, value:TreeNode=None, args:TreeNode=None, symtype=SymbolType.VARIABLE, const=False, local_flag=True):
        """ Symbol Information
            type [in] symbol type node
            name [in] symbol name node
            value [in] symbol value node
        """
        if type is not None:
            if isinstance(type, str):
                self.type = type
            else:
                self.type = type.text
        else:
            self.type = 'void'

        if name is not None:
            if isinstance(name, str):
                self.name = name
            else:
                self.name = name.text
        else:
            self.name = ''

        if value is not None:
            if isinstance(value, str):
                self.value = value
            else:
                self.value = value.value
            self.init = True
        else:
            self.value = None
            self.init = False

        self.args = args
        self.symtype = symtype
        
        # determine size based on type
        size = self.get_size(self.type)
        if size >= 0:
            self.size = size        # variable/return type size
        else:
            print('ERROR: undefined type ' + str(type.text))
            self.size = 0

        self.const = const
        self.addr = 0                # address assigned in add_symbol of SymbolTable.
        self.local = local_flag      # local variable flag

    def get_size(self, type):
        if type == 'char':
            size = 1
        elif type == 'int':
            size = 4
        elif type == 'float':
            size = 4
        elif type == 'void':
            size = 0
        else:
            size = -1

        return size

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None
        self.last_addr = 0
    
    def add_symbol(self, sinfo:SymbolInfo):
        if sinfo.name not in self.symbols:
            sinfo.addr = self.last_addr
            self.symbols[sinfo.name] = sinfo

            if sinfo.symtype == SymbolType.VARIABLE or sinfo.symtype == SymbolType.ARRAY:
                self.last_addr += sinfo.size

    def find_symbol(self, name):
        tab = self
        symbol = None

        while tab is not None:
            if name in tab.symbols:
                symbol = tab.symbols[name]    
                break
            else:
                tab = tab.parent        

        return symbol

class Data:
    def __init__(self, name, value, dtype):
        self.name = name
        self.addr = 0
        self.value = value
        self.dtype = dtype

    def __str__(self):
        s = ''

        if 'char' == self.dtype:
            s = 'db ' + str(self.addr) + ' ' + self.value
        else:
            print('ERROR: undefined data type')
            assert(0)
        return s

INDENT = ''
class Label:
    def __init__(self):
        self.name = ''
        self.addr = -1

    def __str__(self):
        if self.addr > -1:
            return str(self.addr)
        else:
            return self.name
        
class PCode:
    def __init__(self):
        self.inst = None  # instruction. If inst is None, it's a label
        self.op = None
        self.label = None   # label to branch
        self.comment = ''
        self.addr = -1

    def __str__(self):
        
        if self.inst is not None:

            col_op = 10

            s = INDENT
            s += self.inst  # instruction

            if self.op is not None:
                s += ' '
                # If operand exists
                if isinstance(self.op, SymbolInfo):
                    self.op : SymbolInfo

                    # if load and store instructions
                    if self.inst[:3] == 'lda' or self.inst[:3] == 'sto':
                        if self.op.local:
                            if self.op.addr >= 0:
                                s += 'bp+' + str(self.op.addr)
                            else:
                                s += 'bp' + str(self.op.addr)
                        else:
                            s += str(self.op.addr)
                    else:
                        s += str(self.op)
                else:
                    s += str(self.op)

            elif self.label is not None:
                s += ' '
                s += str(self.label)

            if self.comment is not '':
                while len(s) < 25:
                    s += ' '
                s += '; ' + self.comment
        else:
            s = str(self.label) + ':'

        return s

class CodeGenerator:
    """ Code generator class
        This class generates p-code that can be executed by runtime environment.
    """
    def __init__(self):
        self.verbose = False
        self.global_symtab = SymbolTable() # Global Symbol Table

        self.cur_symtab = self.global_symtab

        self.global_var_code = []
        self.function_def_code = []        
        self.labels = {}

        self.list_code = None # instruction list
        self.list_data = []

        sinfo = SymbolInfo('void', 'printf', symtype=SymbolType.STD_FUNCTION)
        self.cur_symtab.add_symbol(sinfo)
        label = Label()
        label.name = 'printf'
        label.addr = 0
        self.add_label(label)

    def select_global_var_code(self):
        self.list_code = self.global_var_code

    def select_function_def_code(self):
        self.list_code = self.function_def_code

    def add_code(self, code:PCode):        
        self.list_code.append(code)

    def add_label(self, label):
        if label.name not in self.labels:
            self.labels[label.name] = label

    def get_label(self, name):
        if name in self.labels:
            return self.labels[name]
        else:
            return None

    def generate_var_decl(self, node, local_flag=True):
        var_type = node.childs[0]
        var_name = node.childs[1]

        if node.childs[2] is not None:
            # declaration with initial value

            var_value = node.childs[2]
            sinfo = SymbolInfo(var_type, var_name, var_value, local_flag=local_flag)
            self.cur_symtab.add_symbol(sinfo)

            # if terminal value
            if OpType.NUMBER == var_value.op_type:
                self.generate_number(var_value)
            elif OpType.ID == var_value.op_type:
                self.generate_id(var_value)
            elif OpType.EXP == var_value.op_type:
                self.generate_exp(var_value)
            elif OpType.FUNC_CALL == var_value.op_type:
                self.generate_call(var_value)
            else:
                print('unknown operation')
                assert(0)

            code = PCode()
            code.inst = 'sto_i32'
            symbol = self.cur_symtab.symbols[var_name.text]
            code.op = symbol
            code.comment = 'store to ' + var_name.text            
            self.add_code(code)
        else:
            # declaration with no initial value

            sinfo = SymbolInfo(var_type, var_name, local_flag=local_flag)
            self.cur_symtab.add_symbol(sinfo)
    
    def generate_number(self, num_node:TreeNode):
        code = PCode()
        code.inst = 'ldc_i32'
        code.op = num_node.value
        self.add_code(code)

    def generate_id(self, id_node:TreeNode):
        symbol = self.cur_symtab.find_symbol(id_node.text)
        code = PCode()
        code.inst = 'lda_i32'
        code.op = symbol
        code.comment = 'load ' + id_node.text
        self.add_code(code)

    def generate_string(self, str_node:TreeNode):        
        
        value = str_node.text + ' 0'
        len_str = len(str_node.text) - 2 + 1 # -2 for " ", +1 for 0
        if len_str % 4 != 0:
            for i in range(4 - len_str % 4):
                value += ' 0'
            len_str += 4 - (len_str % 4)        

        data = Data(name='$'+str(len(self.list_code)), value=value, dtype='char')
        data.addr = self.global_symtab.last_addr
        self.list_data.append(data)

        self.global_symtab.last_addr += len_str

        code = PCode()
        code.inst = 'ldc_i32'
        code.op = data.addr
        self.add_code(code)
        
    
    def generate_exp(self, exp_node:TreeNode):
        exp = exp_node
        stack = []

        if OpType.ID == exp.op_type:
            self.generate_id(exp)
        elif OpType.NUMBER == exp.op_type:
            self.generate_number(exp)
        elif OpType.STRING == exp.op_type:
            self.generate_string(exp)
        else:
            # TODO: To implement in recursive call??
            while exp is not None:
                if exp.childs[0] is not None and exp.childs[0].visited == False:
                    stack.append(exp)
                    exp = exp.childs[0]
                    exp.visited = True

                    # in left leaf node
                    if exp.childs[0] is None and exp.childs[1] is None:
                        if OpType.NUMBER == exp.op_type:
                            self.generate_number(exp)
                        elif OpType.ID == exp.op_type:
                            self.generate_id(exp)

                        if len(stack) > 0:
                            exp = stack.pop()
                        else:
                            exp = None

                elif exp.childs[1] is not None and exp.childs[1].visited == False:
                    stack.append(exp)
                    exp = exp.childs[1]
                    exp.visited = True

                    # in right leaf node
                    if exp.childs[0] is None and exp.childs[1] is None:

                        if OpType.NUMBER == exp.op_type:
                            self.generate_number(exp)
                        elif OpType.ID == exp.op_type:
                            self.generate_id(exp)

                        if len(stack) > 0:
                            exp = stack.pop()
                        else:
                            exp = None

                else:
                    # if both the left and the right children are visited.

                    code = PCode()
                    if exp.text == '+':
                        code.inst = 'add_i32'
                    elif exp.text == '*':
                        code.inst = 'mul_i32'
                    elif exp.text == '=':

                        if OpType.TERMINAL != exp.childs[0].op_type:
                            print('Error: LVALUE is not ID')
                            assert(0)

                        code.inst = 'sto_i32'
                        symbol = self.cur_symtab.find_symbol(exp.childs[0].text)
                        code.op = symbol
                        code.comment = 'store to ' + exp.childs[0].text
                    elif exp.text == '==':
                        code.inst = 'cmp'                
                    else:
                        print('Error: Undefined operator')
                        assert(0)

                    self.add_code(code)

                    if len(stack) > 0:
                        exp = stack.pop()
                    else:
                        exp = None

    def generate_call(self, call_node:TreeNode):

        # get function name
        func_name = call_node.text

        sinfo:SymbolInfo
        sinfo = self.cur_symtab.find_symbol(func_name)
        if SymbolType.FUNCTION != sinfo.symtype and SymbolType.STD_FUNCTION != sinfo.symtype:
            print("ERROR: " + func_name + ' is not a function')

        if sinfo.size > 0:
            code = PCode()
            code.inst = 'ldc_i32'
            code.op = 0
            code.comment = 'reserve for return value'
            self.add_code(code)

        code = PCode()
        code.inst = 'mst'
        code.comment = 'mark stack'
        self.add_code(code)

        # function arguments
        arg = call_node.childs[0]
        while arg is not None:
            self.generate_exp(arg)
            arg = arg.next

        label = self.get_label(call_node.text)
        if label is None:
            label = Label()
            label.name = call_node.text
            self.add_label(label)

        code = PCode()
        if SymbolType.FUNCTION == sinfo.symtype:
            code.inst = 'cup'
            code.op = label
            code.comment = 'call user procedure ' + call_node.text
        else:
            code.inst = 'csp'
            code.op = label
            code.comment = 'call standard procedure ' + call_node.text
        
        self.add_code(code)

    def generate_if_stmt(self, if_node:TreeNode):
        cond = if_node.childs[0]
        block_true  = if_node.childs[1]
        block_false = if_node.childs[2]

        self.generate_exp(cond)

        if block_false == None:
            # if-statement
            label_end = Label()
            label_end = 'LE' + str(len(self.list_code))
            self.add_label(label_end)

            code = PCode()
            code.inst = 'jne'
            code.label = label_end
            self.add_code(code)

            self.generate_stmt(block_true)
        
        else:
            # if-else statement
            label_false = Label()
            label_false.name = 'LF' + str(len(self.list_code))
            self.add_label(label_false)

            label_end = Label()
            label_end.name = 'LE' + str(len(self.list_code))
            self.add_label(label_end)

            code = PCode()
            code.inst = 'jne'
            code.label = label_false
            self.add_code(code)

            self.generate_stmt(block_true)

            code = PCode()
            code.inst = 'jmp'
            code.label = label_end
            self.add_code(code)

            code = PCode()
            code.label = label_false
            self.add_code(code)

            self.generate_stmt(block_false)
        
            code = PCode()
            code.label = label_end
            self.add_code(code)

    def generate_stmt(self, stmt_node:TreeNode):
        node = stmt_node

        while node is not None:
            if OpType.VAR_DECL == node.op_type:
                self.generate_var_decl(node)
            elif OpType.IF_STMT == node.op_type:
                self.generate_if_stmt(node)
            elif OpType.EXP == node.op_type:
                self.generate_exp(node)
            elif OpType.RETURN == node.op_type:
                self.generate_return(node)
            elif OpType.ID == node.op_type:
                self.generate_id(node)
            elif OpType.NUMBER == node.op_type:
                self.generate_number(node)
            elif OpType.FUNC_CALL == node.op_type:
                self.generate_call(node)
            else:
                print('ERROR: Undefined operation type')
                assert(0)

            node = node.next

    def generate_return(self, ret_node:TreeNode):
        
        op = ret_node.childs[0]
        self.generate_exp(op)

        code = PCode()
        code.inst = 'sto_i32'
        code.comment = 'return value'
        sinfo = SymbolInfo(type=None, name=None)
        sinfo.local = True
        sinfo.addr = -12
        code.op = sinfo
        self.add_code(code)

    def generate_function(self, func_node):

        symtab = SymbolTable()
        symtab.parent = self.cur_symtab
        self.cur_symtab = symtab

        func_args: TreeNode
        func_body: TreeNode
        
        func_type = func_node.childs[0]
        func_name = func_node.childs[1]
        func_args = func_node.childs[2]
        func_body = func_node.childs[3]

        comment = ''
        arg = func_args
        while arg is not None:
            comment += arg.childs[1].text
            comment += ':'
            comment += arg.childs[0].text
            comment += " "            

            arg_type = arg.childs[0]
            arg_name = arg.childs[1]
            sinfo = SymbolInfo(arg_type, arg_name)
            sinfo.init = True   # function arguments are initialized
            self.cur_symtab.add_symbol(sinfo)

            arg = arg.next

        label = self.get_label(func_name.text)
        if label is None:
            label = Label()
            label.name = func_name.text
            self.add_label(label)

        code = PCode()
        code.inst = None
        code.label = label
        self.add_code(code)

        self.generate_stmt(func_body)

        code = PCode()
        code.inst = 'ret'
        self.add_code(code)
        
        self.cur_symtab = self.cur_symtab.parent


    def generate(self, program:TreeNode, path, verbose=False):
        """ This method generates code from abstract syntax tree (AST)
            @param program [in] The root of AST
        """
        self.verbose = verbose

        self.select_function_def_code()

        label = Label()
        label.name = 'main'
        self.add_label(label)

        code = PCode()
        code.inst = 'mst'
        code.comment = 'mark stack'
        self.add_code(code)

        code = PCode()
        code.inst = 'cup'
        code.label = label
        code.comment = 'call main() function'
        self.add_code(code)

        code = PCode()
        code.inst = 'stp'
        code.comment = 'end program'
        self.add_code(code)

        # traverse abstracted syntax tree
        node = program
        while node is not None:
            if node.op_type == OpType.VAR_DECL:
                self.select_global_var_code()
                self.generate_var_decl(node, local_flag=False)

            elif node.op_type == OpType.FUNC_DECL:
                self.select_function_def_code()
                func_type = node.childs[0]
                func_name = node.childs[1]
                func_args = node.childs[2]
                func_body = node.childs[3]

                sinfo = SymbolInfo(func_type, func_name, args=func_args, symtype=SymbolType.FUNCTION)
                self.cur_symtab.add_symbol(sinfo)

                self.generate_function(node)

            node = node.next

        # find address
        if True:
            addr = len(self.global_var_code)

            for i in range(len(self.function_def_code)):
                code = self.function_def_code[i]
                if code.inst is not None:
                    addr += 1
                else:
                    code.label.addr = addr

        # write code
        with open(path, 'w') as f:

            # summary
            # global memory size
            f.write('.global {}'.format(self.global_symtab.last_addr) + '\n')

            f.write('.data\n')
            for data in self.list_data:
                f.write(str(data) + '\n')

            f.write('.code\n')

            for code in self.global_var_code:
                f.write(str(code) + '\n')
            
            for code in self.function_def_code:
                if code.inst != None:
                    f.write(str(code) + '\n')

