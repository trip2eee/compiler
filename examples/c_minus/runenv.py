"""
@brief C-- Runtime Environment
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

        self.global_size = 0
        self.stack_size = 1024

        # special purpose registers
        self.pc = 0 # program counter
        self.bp = 0 # base pointer
        self.sp = 0 # stack pointer

    def exec(self, code_path):
        self.load_code(code_path)

        self.pc = 0
        self.bp = 0
        self.sp = self.global_size

        while True:
            # featch
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
            elif 'stp' == code.inst:
                print('End program')
                break
            else:
                print('undefined instruction')
    
    def push_i32(self, i32):
        b = int.to_bytes(i32, 4, byteorder=ENDIAN)
        self.list_data[self.sp:self.sp+4] = b
        self.sp += 4

    def pop_i32(self):
        self.sp -= 4
        b = self.list_data[self.sp:self.sp+4]
        
        return int.from_bytes(b, byteorder=ENDIAN)

    def mst(self):        
        self.push_i32(self.bp)
        self.bp = self.sp
        self.sp = self.bp

    def cup(self, code):
        self.push_i32(self.pc)
        self.pc = code.op

    def ret(self):
        self.pc = self.pop_i32()
        self.sp = self.bp
        self.bp = self.pop_i32()        

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
        b = self.pop_i32()

        if code.base == 0:
            addr = code.op
        else:
            addr = self.bp + code.op

        self.list_data[addr:addr+4] = int.to_bytes(b, 4, byteorder=ENDIAN)
    
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
                    print('initialize data')
                
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
                    print('read codes')
                
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





