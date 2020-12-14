import sys

LDI= 0b10000010
PRN = 0b01000111
HLT=  0b00000001
POP = 0b01000110
CALL = 0b01010000
RET =  0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
# Flag Values
ltf = 0b100
gtf = 0b010
etf = 0b001


class CPU:

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[7] = 0xF4
        self.flags = 0b00000001 
        self.hault = False
        self.SP = 7
        
         
    def load(self):
        address = 0
        file = sys.argv[1]

        if len(sys.argv) < 2:
             print('Wrong number of arguments passed in')   
            
        with open(file) as my_file:
            for line in my_file:
                comment_split = line.split('#')
                possible_binary_num = comment_split[0]
                try:
                    x = int(possible_binary_num, 2)
                    self.ram[address] = x
                    address += 1
                except:
                    continue
            
    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[value] = address
        
    def alu(self, op, reg_a, reg_b):
        if op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flags = ltf
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flags = gtf
            else:
                self.flags = etf     
        else:
            raise Exception("Unsupported ALU operation")

    def run(self):
        while self.hault == False:
            command = self.ram[self.pc]
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            alu = (command >> 5) & 0b001
            
            if command == PRN:
                print(self.reg[op_a])
            elif command == LDI:
                self.reg[op_a] = op_b         
            elif command == HLT:
                self.hault = True
            elif command == CMP:
                self.alu("CMP", op_a, op_b)  
            elif command == JMP:
                self.pc = self.reg[op_a]  
            elif command == JEQ:
                if self.flags & etf:
                    self.pc = self.reg[op_a]
                else:
                    self.pc +=2   
            elif command == JNE:
                if not self.flags & etf:
                    self.pc = self.reg[op_a]
                else:
                    self.pc +=2
            else:   
                self.hault = True
            
            if command >> 4 & 0b0001:
                continue
            else:
                self.pc += (command >> 6)  + 1