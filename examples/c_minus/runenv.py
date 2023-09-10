"""
@brief C-- Runtime Environment
"""

class RunEnv:
    def __init__(self):
                
        self.list_code = [] # code memory
        self.list_data = [] # data memory

        # special purpose registers
        self.pc = 0 # program counter
        self.bp = 0 # base pointer
        self.sp = 0 # stack pointer

    def exec(self, code_path):
        