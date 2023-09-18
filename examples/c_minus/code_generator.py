"""
@brief C-- p-code generator
@author Jongmin Park (trip2eee@gmail.com)
@date September 4, 2023
"""

from examples.c_minus.cmm_parser_table import *

VAL_UNINIT = -858993460 # 0xCCCCCCCC

class SymbolType(enum.IntEnum):
    VARIABLE = 0
    ARRAY = 1
    FUNCTION = 2
    TYPE = 3
    STD_FUNCTION = 4

class SymbolInfo:
    def __init__(self, type:TreeNode, name:TreeNode, value:TreeNode=None, args:TreeNode=None, symtype=SymbolType.VARIABLE, const=False, local_flag=True, num_elem=1):
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
        elem_size = self.get_size(self.type)
        self.elem_size = elem_size          # size of data type
        self.num_elements = num_elem        # number of elements (array)

        if elem_size >= 0:
            self.size = elem_size * self.num_elements        # total size
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
        """ This method finds symbol with the input name
            @param name [in] input name
            @return symbol, from_parent
                    symbol: symbol class instance
                    from_cur_symtab: True if from current symbol table. Otherwise, the symbol is from parent symbol table.
        """
        tab = self
        symbol = None
        from_cur_symtab = True

        while tab is not None:
            if name in tab.symbols:
                symbol = tab.symbols[name]    
                break
            else:
                tab = tab.parent
                from_cur_symtab = False

        return symbol, from_cur_symtab

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
                    inst = self.inst[:3]
                    if inst == 'lod' or inst == 'lda' or inst == 'sto' or inst == 'inc' or inst == 'dec':
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
        label_printf = self.new_named_label('printf')
        label_printf.addr = 0

    def select_global_var_code(self):
        self.list_code = self.global_var_code

    def select_function_def_code(self):
        self.list_code = self.function_def_code

    def add_code(self, code:PCode):        
        self.list_code.append(code)

    def new_label(self):
        """ This method create a new label with name L@<id>
        """
        label = Label()
        label.name = "L@{:08d}".format(len(self.labels))
        self.labels[label.name] = label
        return label
    
    def new_named_label(self, name):
        """ This method create a new named label.
        """
        if name not in self.labels:
            # if there is label with the name
            label = Label()
            label.name = name
            self.labels[label.name] = label
        
        return self.labels[name]

    def get_label(self, name):
        if name in self.labels:
            return self.labels[name]
        else:
            return None

    def generate_var_decl(self, node, local_flag=True):
        var_type = node.childs[0]
        var_name = node.childs[1]
        var_value = node.childs[2]

        symbol, from_cur_symtab = self.cur_symtab.find_symbol(var_name.text)
        if symbol is None or from_cur_symtab == False:
            sinfo = SymbolInfo(var_type, var_name, var_value, local_flag=local_flag)
            self.cur_symtab.add_symbol(sinfo)
            
            if var_value is not None:
                # declaration with initial value
                code = PCode()
                code.inst = 'ldc_i32'
                code.op = VAL_UNINIT
                code.comment = 'declare variable ' + var_name.text
                self.add_code(code)

                code = PCode()
                code.inst = 'lda'
                code.op = sinfo
                self.add_code(code)

                # if terminal value
                self.generate_exp(var_value)

                code = PCode()
                code.inst = 'sto_i32'
                symbol = self.cur_symtab.symbols[var_name.text]
                code.op = symbol
                code.comment = 'store to ' + var_name.text
                self.add_code(code)
            else:
                # declaration with no initial value
                code = PCode()
                code.inst = 'ldc_i32'
                code.op = VAL_UNINIT
                code.comment = 'uninitialized variable ' + var_name.text
                self.add_code(code)
                
        else:
            print('Error [Line:{}, Col:{}] variable {} is already declared.'.format(node.childs[1].idx_line, node.childs[1].idx_col, var_name.text))        

    def generate_var_array_decl(self, node, local_flag=True):
        array_type  = node.childs[0]
        array_name  = node.childs[1]
        array_size  = node.childs[2]
        array_value = node.childs[3]

        array_size = int(array_size.text)

        symbol, from_cur_symtab = self.cur_symtab.find_symbol(array_name.text)
        if symbol is None or from_cur_symtab == False:
            sinfo = SymbolInfo(array_type, array_name, symtype=SymbolType.ARRAY, local_flag=local_flag, num_elem=array_size)
            sinfo.num_elements = array_size
            self.cur_symtab.add_symbol(sinfo)

            if array_value is not None:
                # not implemented.
                assert(0)
            else:
                # declaration with no initial value
                for i in range(array_size):
                    code = PCode()
                    code.inst = 'ldc_i32'
                    code.op = VAL_UNINIT
                    if i == 0:
                        code.comment = 'uninitialized variable ' + array_name.text
                    self.add_code(code)
        else:
            print('Error [Line:{}, Col:{}] variable {} is already declared.'.format(node.childs[1].idx_line, node.childs[1].idx_col, array_name.text))

    def generate_number(self, num_node:TreeNode):
        code = PCode()
        code.inst = 'ldc_i32'
        code.op = num_node.value
        self.add_code(code)

    def generate_id(self, id_node:TreeNode):
        symbol, _ = self.cur_symtab.find_symbol(id_node.text)
        
        if id_node.childs[2] is None:
            # if ID
            code = PCode()
            code.inst = 'lod_i32'
            code.op = symbol
            code.comment = 'load ' + id_node.text
            self.add_code(code)
        else:
            # if ID[EXP] (array)
            code = PCode()
            code.inst = 'lda'
            code.op = symbol
            code.comment = 'load ' + id_node.text
            self.add_code(code)

            # compute index
            self.generate_exp(id_node.childs[2])

            code = PCode()
            code.inst = 'ixa'   # indexed address
            code.op = 4         # TODO: To use symbol.elem_size
            self.add_code(code)

            code = PCode()
            code.inst = 'ind_i32'   # indexed address
            code.op = 0
            self.add_code(code)

            # TODO: To make flag to compute address or value

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


        # TODO: To implement in recursive call??
        while exp is not None:
            if exp.childs[0] is not None and exp.childs[0].visited == False:
                stack.append(exp)
                exp = exp.childs[0]
                exp.visited = True

            elif exp.childs[1] is not None and exp.childs[1].visited == False:
                stack.append(exp)
                exp = exp.childs[1]
                exp.visited = True

            else:
                # if terminal nodes
                if OpType.ID == exp.op_type:
                    self.generate_id(exp)
                elif OpType.NUMBER == exp.op_type:
                    self.generate_number(exp)
                elif OpType.STRING == exp.op_type:
                    self.generate_string(exp)
                elif OpType.FUNC_CALL == exp.op_type:
                    self.generate_call(exp)
                else:
                    # if both the left and the right children are visited.
                    code = PCode()
                    if exp.text == '+':
                        code.inst = 'add_i32'
                    elif exp.text == '-':
                        code.inst = 'sub_i32'
                    elif exp.text == '*':
                        code.inst = 'mul_i32'
                    elif exp.text == '==':
                        code.inst = 'equ'
                    elif exp.text == '!=':
                        code.inst = 'neq'
                    elif exp.text == '<=':
                        code.inst = 'lte'
                    elif exp.text == '>=':
                        code.inst = 'gte'
                    elif exp.text == '<':
                        code.inst = 'lst'
                    elif exp.text == '>':
                        code.inst = 'grt'
                    else:
                        print('Error: Undefined operator ' + exp.text)
                        assert(0)

                    self.add_code(code)

                if len(stack) > 0:
                    exp = stack.pop()
                else:
                    exp = None


    def generate_assign_exp(self, assign_node:TreeNode):

        # lda <addr>
        # lod <value>
        # sto  ; *(<addr>) = value

        # compute L-value
        # ID
        # ID[exp]
        # call()[exp]
        # *(exp)
        code = PCode()
        if OpType.TERMINAL != assign_node.childs[0].op_type:
            print('Error: L-Value is not ID')
            assert(0)

        code.inst = 'lda'   # load address of a variable
        symbol, _ = self.cur_symtab.find_symbol(assign_node.childs[0].text)
        code.op = symbol
        self.add_code(code)

        offset_node = assign_node.childs[1]
        if offset_node is not None:
            # compute offset (index)
            self.generate_exp(offset_node)

            # scale index. addr + op*index
            code = PCode()
            code.inst = 'ixa'
            code.op = 4
            self.add_code(code)
            
        # compute R-value
        self.generate_exp(assign_node.childs[2])

        code = PCode()
        code.inst = 'sto_i32'
        self.add_code(code)
        

    def generate_call(self, call_node:TreeNode):

        # get function name
        func_name = call_node.text

        sinfo:SymbolInfo
        sinfo, _ = self.cur_symtab.find_symbol(func_name)
        if SymbolType.FUNCTION != sinfo.symtype and SymbolType.STD_FUNCTION != sinfo.symtype:
            print("ERROR: " + func_name + ' is not a function')

        if sinfo.size > 0:
            code = PCode()
            code.inst = 'ldc_i32'
            code.op = VAL_UNINIT
            code.comment = 'reserve for return value'
            self.add_code(code)

        code = PCode()
        code.inst = 'mst'
        code.comment = 'mark stack'
        self.add_code(code)

        # function arguments
        arg = call_node.childs[2]
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
            label_end = self.new_label()

            code = PCode()
            code.inst = 'jpf'
            code.label = label_end
            self.add_code(code)

            self.generate_stmt(block_true)

            code = PCode()
            code.label = label_end
            self.add_code(code)
            
        else:
            # if-else statement
            label_false = self.new_label()
            label_end = self.new_label()

            code = PCode()
            code.inst = 'jpf'
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

    def generate_for_stmt(self, for_node:TreeNode):
        node_init   = for_node.childs[0]
        node_test   = for_node.childs[1]
        node_update = for_node.childs[2]
        node_body   = for_node.childs[3]

        # new symbol table for for-statement
        symtab = SymbolTable()
        symtab.parent = self.cur_symtab
        symtab.last_addr = self.cur_symtab.last_addr    # for scope, base pointer is preserved.
        self.cur_symtab = symtab

        # initialization statement
        self.generate_stmt(node_init)

        label_begin = self.new_label()
        label_end = self.new_label()

        code = PCode()
        code.label = label_begin
        self.add_code(code)
        
        # test statement
        self.generate_stmt(node_test)

        code = PCode()
        code.inst = 'jpf'
        code.label = label_end
        code.comment = 'if false, jump to the end of for-loop'
        self.add_code(code)

        # loop body
        if OpType.COMPOUND_STMT == node_body.op_type:
            self.generate_stmt(node_body.childs[0])
        else:
            self.generate_stmt(node_body)

        # update
        self.generate_stmt(node_update)

        code = PCode()
        code.inst = 'jmp'
        code.label = label_begin
        self.add_code(code)
        
        code = PCode()
        code.label = label_end
        self.add_code(code)

        self.cur_symtab = self.cur_symtab.parent

    def generate_while_stmt(self, for_node:TreeNode):
        node_test   = for_node.childs[0]
        node_body   = for_node.childs[1]

        label_begin = self.new_label()
        label_end = self.new_label()

        code = PCode()
        code.label = label_begin
        self.add_code(code)

        # test statement
        self.generate_stmt(node_test)        

        code = PCode()
        code.inst = 'jpf'
        code.label = label_end
        code.comment = 'if false, jump to the end of while-loop'
        self.add_code(code)

        # loop body
        self.generate_stmt(node_body)

        code = PCode()
        code.inst = 'jmp'
        code.label = label_begin
        self.add_code(code)
        
        code = PCode()
        code.label = label_end
        self.add_code(code)

    def generate_compound_stmt(self, comp_node:TreeNode):
        # new symbol table for compound statement
        symtab = SymbolTable()
        symtab.parent = self.cur_symtab
        symtab.last_addr = self.cur_symtab.last_addr    # for scope, base pointer is preserved.
        self.cur_symtab = symtab

        self.generate_stmt(comp_node.childs[0])

        self.cur_symtab = self.cur_symtab.parent

    def generate_dec_stmt(self, exp:TreeNode):        
        if OpType.TERMINAL != exp.childs[0].op_type:
            print('Error: LVALUE is not ID')
            assert(0)

        code = PCode()
        code.inst = 'dec_i32'
        symbol, _ = self.cur_symtab.find_symbol(exp.childs[0].text)
        code.op = symbol
        code.comment = 'decrease ' + exp.childs[0].text
        self.add_code(code)
    
    def generate_inc_stmt(self, exp:TreeNode):
        if OpType.TERMINAL != exp.childs[0].op_type:
            print('Error: LVALUE is not ID')
            assert(0)

        code = PCode()
        code.inst = 'inc_i32'
        symbol, _ = self.cur_symtab.find_symbol(exp.childs[0].text)
        code.op = symbol
        code.comment = 'increase ' + exp.childs[0].text
        self.add_code(code)

    def generate_stmt(self, stmt_node:TreeNode):
        node = stmt_node

        while node is not None:
            if OpType.VAR_DECL == node.op_type:
                self.generate_var_decl(node)
            elif OpType.VAR_ARRAY_DECL == node.op_type:
                self.generate_var_array_decl(node)
            elif OpType.IF_STMT == node.op_type:
                self.generate_if_stmt(node)
            elif OpType.EXP == node.op_type:
                self.generate_exp(node)
            elif OpType.ASSIGN_EXP == node.op_type:
                self.generate_assign_exp(node)
            elif OpType.RETURN == node.op_type:
                self.generate_return(node)
            elif OpType.ID == node.op_type:
                self.generate_id(node)
            elif OpType.NUMBER == node.op_type:
                self.generate_number(node)
            elif OpType.FUNC_CALL == node.op_type:
                self.generate_call(node)
            elif OpType.FOR_STMT == node.op_type:
                self.generate_for_stmt(node)
            elif OpType.WHILE_STMT == node.op_type:
                self.generate_while_stmt(node)
            elif OpType.COMPOUND_STMT == node.op_type:
                self.generate_compound_stmt(node)
            elif OpType.DECREMENT == node.op_type:
                self.generate_dec_stmt(node)
            elif OpType.INCREMENT == node.op_type:
                self.generate_inc_stmt(node)
            elif OpType.COMMENT == node.op_type:
                pass # skip comment
            else:
                print('ERROR: Undefined operation type', node.op_type)
                assert(0)

            node = node.next

    def generate_return(self, ret_node:TreeNode):
        
        code = PCode()
        code.inst = 'lda'
        code.comment = 'return value'
        sinfo = SymbolInfo(type=None, name=None)
        sinfo.local = True
        sinfo.addr = -12
        code.op = sinfo
        self.add_code(code)

        op = ret_node.childs[0]
        self.generate_exp(op)        

        code = PCode()
        code.inst = 'sto_i32'        
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

        label = self.new_named_label(func_name.text)

        code = PCode()
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

        label_main = self.new_named_label('main')

        code = PCode()
        code.inst = 'mst'
        code.comment = 'mark stack'
        self.add_code(code)
        
        # To handle main function with return type int
        code = PCode()
        code.inst = 'ldc_i32'
        code.op = VAL_UNINIT
        code.comment = 'reserve for return value of int main()'
        self.add_code(code)
    
        code = PCode()
        code.inst = 'cup'
        code.label = label_main
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

                sinfo = SymbolInfo(func_type, func_name, args=func_args, symtype=SymbolType.FUNCTION)
                self.cur_symtab.add_symbol(sinfo)

                self.generate_function(node)

            node = node.next

        debug_mode = False

        # find address
        if debug_mode == False:
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
                if code.inst != None or debug_mode == True:
                    f.write(str(code) + '\n')

