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
    def __init__(self):
                
        self.list_code = [] # code memory
        self.list_data = None

        self.global_size = 0    # The size of gobal/static is determined by .global directive.
        self.stack_size = 1024  # reserved stack size

        # special purpose registers
        self.pc = 0 # program counter
        self.bp = 0 # base pointer
        self.sp = 0 # stack pointer

        self.ostream = []   # output stream for test

    def exec(self, code_path):
        self.load_code(code_path)

        self.pc = 0
        self.bp = 0
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
            elif 'mul_i32' == code.inst:
                self.mul_i32(code)
            elif 'mst' == code.inst:
                self.mst()
            elif 'cup' == code.inst:
                self.cup(code)
            elif 'ret' == code.inst:
                self.ret()
            elif 'cmp' == code.inst:
                self.cmp()
            elif 'jmp' == code.inst:
                self.jmp(code)
            elif 'jne' == code.inst:
                self.jne(code)
            elif 'csp' == code.inst:
                self.csp(code)
            elif 'stp' == code.inst:
                break
            else:
                print('undefined instruction:', code.inst, self.pc-1)
                assert(0)
    
    def push_i32(self, i32):
        b = int.to_bytes(i32, 4, byteorder=ENDIAN)
        self.list_data[self.sp:self.sp+4] = b
        self.sp += 4

    def pop_i32(self):
        self.sp -= 4
        b = self.list_data[self.sp:self.sp+4]
        
        return int.from_bytes(b, byteorder=ENDIAN)

    def printf(self):
        # string pointer
        addr = self.bp+0
        pstr = self.list_data[addr]

        str_out = ''
        c = self.list_data[pstr:pstr+1].decode()        
        while c != '\0':
            str_out += c
            print(c, end='')
            pstr += 1
            c = self.list_data[pstr:pstr+1].decode()

        self.ostream.append(str_out)

    def cup(self, code):        
        addr = self.bp - 8
        self.list_data[addr:addr+4] = int.to_bytes(self.pc, 4, byteorder=ENDIAN)

        self.pc = code.op

    def csp(self, code):
        addr = self.bp - 8
        self.list_data[addr:addr+4] = int.to_bytes(self.pc, 4, byteorder=ENDIAN)

        if code.op == 0:
            # printf
            self.printf()
        
        self.ret()  # return

    def jmp(self, code): 
        # unconditional branch       
        self.pc = code.op        

    def jne(self, code):
        a = self.pop_i32()
        if a == 0:
            self.pc = code.op
        else:
            pass    # no operation        

    def cmp(self):
        a = self.pop_i32()
        b = self.pop_i32()
        if a==b:
            # equal
            self.push_i32(1)
        else:
            # not equal
            self.push_i32(0)


    def mst(self):
        self.push_i32(0)        # reserve memory for pc
        self.push_i32(self.bp)
        self.bp = self.sp       # set new base pointer
        self.sp = self.bp       # set new stack pointer

    def ret(self):
        # read pc
        addr = self.bp - 8
        self.pc = int.from_bytes(self.list_data[addr:addr+4], byteorder=ENDIAN)

        # restore sp
        self.sp = self.bp - 8 # for bp and pc

        # read bp
        addr = self.bp - 4
        self.bp = int.from_bytes(self.list_data[addr:addr+4], byteorder=ENDIAN)        
        

    def ldc_i32(self, code):
        self.push_i32(code.op)

    def lda_i32(self, code):
        if code.base == 0:
            addr = code.op
        else:
            addr = self.bp + code.op

        value = int.from_bytes(self.list_data[addr:addr+4], byteorder=ENDIAN)
        self.push_i32(value)

    def sto_i32(self, code):
        a = self.pop_i32()

        if code.base == 0:
            addr = code.op
        else:
            addr = self.bp + code.op

        self.list_data[addr:addr+4] = int.to_bytes(a, 4, byteorder=ENDIAN)
    
    def add_i32(self, code):
        b = self.pop_i32()
        a = self.pop_i32()
        self.push_i32(a + b)

    def mul_i32(self, code):
        b = self.pop_i32()
        a = self.pop_i32()
        self.push_i32(a * b)

    def load_code(self, code_path):
        with open(code_path, 'r') as f:
            while True:
                l = f.readline().strip()

                if l == '':
                    break

                tokens = l.split(' ')

                if '.global' == tokens[0]:
                    # initialize data memory
                    self.global_size = int(tokens[1])
                    self.list_data = bytearray(self.global_size + self.stack_size)
                
                elif '.data' == tokens[0]:
                    pass
                
                elif 'db' == tokens[0]:
                    addr = int(tokens[1])

                    for i in range(2, len(tokens)):
                        d = tokens[i]

                        # if string
                        if d[0] == '"':
                            j = 1
                            while d[j] != '"':
                                self.list_data[addr] = ord(d[j])
                                addr += 1
                                j += 1
                        else:
                            self.list_data[addr] = int(d)
                            addr += 1

                elif '.code' == tokens[0]:
                    pass

                else:
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





