"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        # program that saves and prints numbers from registers
        self.reg = [0] * 8  
        self.pc = 0 
        self.ram = [0] * 256  
        self.SP = 7 # register location that holds top of stack address
        self.LDI =  int('10000010',2) 
        self.PRN =  int('01000111',2)
        self.HLT =  int('00000001',2)
        self.MUL =  int('10100010',2)
        self.PUSH =  int('01000101',2)
        self.POP =  int('01000110',2) 
        
    def load(self):
        """Load a program into memory."""

        address = 0
        print('see how many args passed', sys.argv)
        if len(sys.argv) != 2:
            print("Need file name with the extention .ls8 passed")
            sys.exit(1)

        # For now, we've just hardcoded a program:
        program = []
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        filename = sys.argv[1]
        filepath = "examples/" + filename
        with open(filepath) as f:
            for line in f:
                if line == '\n' or line[0]== '#':
                    continue
                comment_split = line.split('#')
                bi_num = int(comment_split[0].strip(), 2)
                program.append(bi_num)
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, address):
        return self.ram[address]
    def ram_write(self, address, instruction):
        self.ram[address] = instruction
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        # store the top of memory into Register 7
        self.reg[self.SP] = len(self.ram) - 1 #255
        while running:
            # lets receive some instructions, and execute them
            command = self.ram[self.pc]
            # if command is LDI
            if command == self.LDI:
                Rg = self.ram[self.pc+1]
                num_LDI = self.ram[self.pc+2]
                self.reg[Rg] = num_LDI
                self.pc += 3
            #if comad is push
            elif command == self.PUSH:
                Rg = self.ram[self.pc+1]
                # decrement the Stack Pointer (SP)
                self.reg[self.SP] -= 1
                # read the next value for register location
                Rg_val = self.reg[Rg]
                # take the value in that register and add to stack
                self.ram[self.reg[self.SP]] = Rg_val
                self.pc += 2
            elif command == self.POP:
                # POP value of stack at location SP
                val = self.ram[self.reg[self.SP]]
                Rg = self.ram[self.pc+1]
                # store the value into register given
                self.reg[Rg] = val
                # increment the Stack Pointer (SP)
                self.reg[self.SP] += 1
                self.pc += 2
            # if command is MUL
            elif command == self.MUL:
                num_LDI1 = self.reg[self.ram[self.pc + 1]]
                num_LDI2 = self.reg[self.ram[self.pc + 2]]
                print(num_LDI1 * num_LDI2)
                self.pc += 3
            # if command is PRN
            elif command == self.PRN:
                num_LDI = self.reg[self.ram[self.pc + 1]]
                print(num_LDI)
                self.pc += 2
            # if command is HLT
            elif command == self.HLT:
                running = False
                self.pc = 0
                # shutdown
            else:
                # if command is non recognizable
                print(f"Unknown instruction {command}")
                sys.exit(1)
        