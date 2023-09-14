"""
@brief C-- Runtime Environment
@author Jongmin Park (trip2eee@gmail.com)
@date September 10, 2023
"""

ENDIAN = 'little'

class Code:
    def __init__(self):
        self.inst = ''
        self.op = 0
        self.base = 0

class RunEnv:
    """ C-- Runtime environment
    """
    def __init__(self):
                
        self.list_code = [] # code memory
        self.list_data = None

        self.global_size = 0    # The size of gobal/static is determined by .global directive.
        self.stack_size = 1024  # reserved stack size

        # special purpose registers
        self.pc = 0 # program counter
        self.bp = 0 # base pointer
        self.sp = 0 # stack pointer

        self.stdout = ''   # output stream for test

    def exec(self, code_path):
        """This method executes pcode file.
        @param code_path [in] Input pcode file path
        """
        self.load_code(code_path)

        self.pc = 0
        self.bp = 0
        self.bp_marked = 0
        self.sp = self.global_size

        while True:
            # fetch
            code = self.list_code[self.pc]
            self.pc += 1

            # decode & execute
            if 'ldc_i32' == code.inst:
                self.ldc_i32(code)
            elif 'lda_i32' == code.inst:
                self.lda_i32(code)
            elif 'sto_i32' == code.inst:
                self.sto_i32(code)
            elif 'add_i32' == code.inst:
                self.add_i32(code)
            elif 'sub_i32' == code.inst:
                self.sub_i32(code)
            elif 'mul_i32' == code.inst:
                self.mul_i32(code)
            elif 'inc_i32' == code.inst:
                self.inc_i32(code)
            elif 'dec_i32' == code.inst:
                self.dec_i32(code)
            elif 'mst' == code.inst:
                self.mst()
            elif 'cup' == code.inst:
                self.cup(code)
            elif 'ret' == code.inst:
                self.ret()
            elif 'equ' == code.inst:
                self.equ()
            elif 'lte' == code.inst:
                self.lte()
            elif 'gte' == code.inst:
                self.gte()
            elif 'lst' == code.inst:
                self.lst()
            elif 'grt' == code.inst:
                self.grt()
            elif 'jmp' == code.inst:
                self.jmp(code)
            elif 'jpf' == code.inst:
                self.jpf(code)
            elif 'csp' == code.inst:
                self.csp(code)
            elif 'stp' == code.inst:
                break
            else:
                print('undefined instruction:', code.inst, self.pc-1)
                assert(0)
    
    def push_i32(self, i32):
        b = self.i32_to_bytes(i32)
        self.list_data[self.sp:self.sp+4] = b
        self.sp += 4

    def pop_i32(self):
        self.sp -= 4
        b = self.list_data[self.sp:self.sp+4]
        return self.bytes_to_i32(b)

    def push_u32(self, i32):
        b = self.u32_to_bytes(i32)
        self.list_data[self.sp:self.sp+4] = b
        self.sp += 4

    def pop_u32(self):
        self.sp -= 4
        b = self.list_data[self.sp:self.sp+4]
        return self.bytes_to_u32(b)

    def print_string(self, str):
        print(str, end='')

    def i32_to_bytes(self, i32):
        return int.to_bytes(i32, 4, byteorder=ENDIAN, signed=True)

    def bytes_to_i32(self, bytes):
        return int.from_bytes(bytes, byteorder=ENDIAN, signed=True)
    
    def u32_to_bytes(self, u32):
        return int.to_bytes(u32, 4, byteorder=ENDIAN, signed=False)

    def bytes_to_u32(self, bytes):
        return int.from_bytes(bytes, byteorder=ENDIAN, signed=False)
    
    def printf(self):
        # string pointer
        ptr_arg0 = self.bp+0
        ptr_arg = ptr_arg0
        ptr_format = self.list_data[ptr_arg0]

        str_out = ''
        c = self.list_data[ptr_format:ptr_format+1].decode()
        ptr_format += 1
        while c != '\0':
            if c == '\\':
                # if escape character
                c = self.list_data[ptr_format:ptr_format+1].decode()
                ptr_format += 1
                if c == '\0':
                    break
                elif c == 'n':
                    self.print_string('\n')
                    str_out += '\n'
                elif c == 't':
                    self.print_string('\t')
                    str_out += '\t'
                else:
                    self.print_string('\\')
                    self.print_string(c)
                    str_out += '\\'
                    str_out += c
            elif c == '%':
                # if specifier character
                c = self.list_data[ptr_format:ptr_format+1].decode()
                ptr_format += 1
                if c == 'd':
                    ptr_arg += 4
                    data = self.list_data[ptr_arg:ptr_arg+4]
                    value = self.bytes_to_i32(data)
                    self.print_string(str(value))
                    str_out += str(value)
                else:
                    self.print_string('%')
                    self.print_string(c)
                    str_out += '%'
                    str_out += c
            else:                
                self.print_string(c)
                str_out += c
            
            c = self.list_data[ptr_format:ptr_format+1].decode()
            ptr_format += 1

        self.stdout += str_out

    def cup(self, code):
        self.bp = self.bp_marked    # set new base pointer
        addr = self.bp - 8
        self.list_data[addr:addr+4] = self.u32_to_bytes(self.pc)

        self.pc = code.op

    def csp(self, code):
        self.bp = self.bp_marked    # set new base pointer
        addr = self.bp - 8
        self.list_data[addr:addr+4] = self.u32_to_bytes(self.pc)

        if code.op == 0:
            # printf
            self.printf()
        
        self.ret()  # return

    def jmp(self, code): 
        # unconditional branch       
        self.pc = code.op        

    def jpf(self, code):
        a = self.pop_i32()
        if a == 0:
            # if false
            self.pc = code.op
        else:
            pass    # no operation        

    def equ(self):
        a = self.pop_i32()
        b = self.pop_i32()
        if a==b:
            # equal
            self.push_i32(1)
        else:
            # not equal
            self.push_i32(0)

    def lte(self):
        # pushed in order of a, b
        # pop in reverse order
        b = self.pop_i32()
        a = self.pop_i32()
        if a<=b:
            # less than or equal to
            self.push_i32(1)
        else:
            self.push_i32(0)

    def gte(self):
        # pushed in order of a, b
        # pop in reverse order
        b = self.pop_i32()
        a = self.pop_i32()
        if a>=b:
            # greater than or equal to
            self.push_i32(1)
        else:
            self.push_i32(0)

    def lst(self):
        # pushed in order of a, b
        # pop in reverse order
        b = self.pop_i32()
        a = self.pop_i32()
        if a<b:
            # less than
            self.push_i32(1)
        else:
            self.push_i32(0)

    def grt(self):
        # pushed in order of a, b
        # pop in reverse order
        b = self.pop_i32()
        a = self.pop_i32()
        if a>b:
            # greater than
            self.push_i32(1)
        else:
            self.push_i32(0)

    def mst(self):
        self.push_u32(0)        # reserve memory for pc
        self.push_u32(self.bp)
        self.bp_marked = self.sp
        # sp: not changed

    def ret(self):
        # read pc
        addr = self.bp - 8
        self.pc = self.bytes_to_u32(self.list_data[addr:addr+4])

        # restore sp
        self.sp = self.bp - 8 # for bp and pc

        # read bp
        addr = self.bp - 4
        self.bp = self.bytes_to_u32(self.list_data[addr:addr+4])
        

    def ldc_i32(self, code):
        self.push_i32(code.op)

    def lda_i32(self, code):
        if code.base == 0:
            addr = code.op
        else:
            addr = self.bp + code.op
        value = self.bytes_to_i32(self.list_data[addr:addr+4])
        self.push_i32(value)

    def sto_i32(self, code):
        a = self.pop_i32()

        if code.base == 0:
            addr = code.op
        else:
            addr = self.bp + code.op

        self.list_data[addr:addr+4] = self.i32_to_bytes(a)
    
    def add_i32(self, code):
        b = self.pop_i32()
        a = self.pop_i32()
        self.push_i32(a + b)
    
    def sub_i32(self, code):
        b = self.pop_i32()
        a = self.pop_i32()
        self.push_i32(a - b)

    def mul_i32(self, code):
        b = self.pop_i32()
        a = self.pop_i32()
        self.push_i32(a * b)
    
    def inc_i32(self, code):
        if code.base == 0:
            addr = code.op
        else:
            addr = self.bp + code.op
        value = self.bytes_to_i32(self.list_data[addr:addr+4])
        self.list_data[addr:addr+4] = self.i32_to_bytes(value+1)

    def dec_i32(self, code):
        if code.base == 0:
            addr = code.op
        else:
            addr = self.bp + code.op
        value = self.bytes_to_i32(self.list_data[addr:addr+4])
        self.list_data[addr:addr+4] = self.i32_to_bytes(value-1)

    def load_code(self, code_path):
        """This method loads pcode file and performs the follwing jobs.
           - initialize global memory
           - store pcodes in self.list_code.
        """
        with open(code_path, 'r') as f:
            while True:
                l = f.readline().strip()

                if l == '':
                    break                

                if l.startswith('.global'):
                    # initialize data memory
                    tokens = l.split(' ')
                    self.global_size = int(tokens[1])
                    self.list_data = bytearray(self.global_size + self.stack_size)
                
                elif l.startswith('.data'):
                    pass
                
                elif l.startswith('db'):
                    # addr = int(tokens[1])

                    addr = 0
                    data = l[3:]
                    i = 0
                    while '0' <= data[i] <= '9':
                        addr *= 10
                        addr += int(data[i])
                        i += 1

                    i += 1
                    if data[i] == '"':
                        i += 1
                        while data[i] != '"':
                            self.list_data[addr] = ord(data[i])
                            addr += 1
                            i += 1
                        idx_start = i+2

                    for i in range(idx_start, len(data)):
                        value = 0
                        if '0' <= data[i] <= '0':
                            value *= 10
                            value += int(data[i])
                        else:
                            self.list_data[addr] = value
                            addr += 1


                elif l.startswith('.code'):
                    pass

                else:
                    tokens = l.split(' ')

                    code = Code()
                    code.inst = tokens[0]
                    if len(tokens) >= 2 and tokens[1] != '':                        
                        if tokens[1].startswith('bp'):
                            code.op = int(tokens[1][2:])
                            code.base = 'bp'
                        else:
                            code.op = int(tokens[1])
                            code.base = 0
                    self.list_code.append(code)





