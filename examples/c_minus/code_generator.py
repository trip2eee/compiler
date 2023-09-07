"""
@brief C-- p-code generator
"""

from examples.c_minus.cmm_parser_table import *

class SymbolType(enum.IntEnum):
    VARIABLE = 0
    ARRAY = 1
    FUNCTION = 2
    TYPE = 3

class SymbolInfo:
    def __init__(self, type:TreeNode, name:TreeNode, value:TreeNode, symtype=SymbolType.VARIABLE, const=False):
        """ Symbol Information
            type [in] symbol type node
            name [in] symbol name node
            value [in] symbol value node
        """
        self.type = type.text
        self.name = name.text

        self.value = value.value
        if value is not None:
            self.init = True
        else:
            self.init = False
        self.symtype = symtype
        
        # determine size based on type
        if type.text == 'char':
            self.size = 1
        elif type.text == 'int':
            self.size = 4
        elif type.text == 'float':
            self.size = 8
        else:
            print('ERROR: undefined type ' + str(type.text))
        
        self.const = const

        self.addr = 0   # address assigned in add_symbol of SymbolTable.


class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None
        self.last_addr = 0
    
    def add_symbol(self, info:SymbolInfo):
        if info.name not in self.symbols:
            info.addr = self.last_addr
            self.symbols[info.name] = info            
            self.last_addr += info.size

def merge_symtab(dst, src):
    # This function merges symbol tables
    
    # find the last node of src
    while src.next is not None:
        src = src.next

    if dst.symtab is None:
        dst.symtab = src.symtab
    elif dst.symtab is not None and src.symtab is not None:
        for key in src.symtab.symbols:
            if key not in dst.symtab.symbols:
                dst.symtab.symbols[key] = src.symtab.symbols[key]

INDENT = '    '

class CodeGenerator:
    def __init__(self):
        self.verbose = False
        self.global_symtab = SymbolTable() # Global Symbol Table
        
        self.cur_symtab = self.global_symtab

        self.global_var_code = []
        self.function_def_code = []

        self.list_code = None # instruction list

    def select_global_var_code(self):
        self.list_code = self.global_var_code

    def select_function_def_code(self):
        self.list_code = self.function_def_code

    def add_code(self, code, comment = '', indent=INDENT):
        
        if comment != '':
            line = indent + '{0:<20}'.format(code)
            line += '; ' + comment
        else:
            line = indent + '{0}'.format(code)

        self.list_code.append(line)

    def add_label(self, label):
        self.list_code.append(label + ':')

    def generate(self, program:TreeNode, path, verbose=False):
        """ This method generates code from abstract syntax tree (AST)
            @param program [in] The root of AST
        """
        self.verbose = verbose

        self.select_function_def_code()
        self.add_code('ujp main', 'jump to main() function')

        # traverse abstracted syntax tree
        node = program
        while node is not None:
            if node.op_type == OpType.VAR_DECL:
                self.select_global_var_code()

                var_type = node.childs[0]
                var_name = node.childs[1]

                if node.childs[2] is not None:
                    var_value = node.childs[2]
                    info = SymbolInfo(var_type, var_name, var_value)
                    self.cur_symtab.add_symbol(info)

                    # if terminal value
                    if OpType.TERMINAL == var_value.op_type:
                        code = 'ldc_i32 ' + str(node.childs[2].value)
                        self.add_code(code)

                    elif OpType.EXP == var_value.op_type:
                        # generate code recursively
                        
                        #        +
                        #     /     \
                        #    *       *
                        #   / \     / \
                        #  1  10   2   +
                        #             / \
                        #            5   5

                        stack = []
                        exp = var_value
                        while exp is not None:                          

                            if exp.childs[0] is not None and exp.childs[0].visited == False:
                                stack.append(exp)
                                exp = exp.childs[0]
                                exp.visited = True

                                # in left leaf node
                                if OpType.TERMINAL == exp.op_type:
                                    code = 'ldc_i32 ' + str(exp.value)
                                    self.add_code(code)

                                    if len(stack) > 0:
                                        exp = stack.pop()
                                    else:
                                        exp = None

                            elif exp.childs[1].visited == False:
                                stack.append(exp)
                                exp = exp.childs[1]
                                exp.visited = True

                                # in right leaf node
                                if OpType.TERMINAL == exp.op_type:
                                    code = 'ldc_i32 ' + str(exp.value)
                                    self.add_code(code)

                                    if len(stack) > 0:
                                        exp = stack.pop()
                                    else:
                                        exp = None

                            else:
                                # if both the left and the right children are visited.

                                if exp.text == '+':
                                    code = 'add_i32'
                                elif exp.text == '*':
                                    code = 'mul_i32'
                            
                                self.add_code(code)

                                if len(stack) > 0:
                                    exp = stack.pop()
                                else:
                                    exp = None

                        while len(stack) > 0:
                            exp:TreeNode
                            exp = stack.pop()

                            if OpType.TERMINAL == exp.op_type:
                                code = 'ldc_i32 ' + str(exp.value)
                                self.add_code(code)

                        code = ''


                    else:
                        # compute expression
                        print('ERROR: undefined value')

                    code = 'sto_i32 ' + str(self.cur_symtab.symbols[var_name.text].addr)
                    comment = 'store to ' + var_name.text
                    self.add_code(code, comment)
                else:
                    print(var_type + ' ' + var_name.text)

                    info = SymbolInfo(var_type, var_name, None)
                    self.cur_symtab.add_symbol(info)


            elif node.op_type == OpType.FUNC_DECL:
                self.select_function_def_code()

                print(node.childs[0].text + ' ' + node.childs[1].text)
                self.add_label(node.childs[1].text)

            node = node.next

        with open(path, 'w') as f:
            for code in self.global_var_code:
                f.write(code + '\n')

            for code in self.function_def_code:
                f.write(code + '\n')
        
