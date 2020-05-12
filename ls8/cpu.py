"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        # program that saves and prints numbers from registers
        self.reg = [0] * 8  
        self.pc = 0 
        self.ram = [0] * 256  
        
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
        while running:
            # lets receive some instructions, and execute them
            command = self.ram[self.pc]
            print('comand', command)
            # if command is LDI
            if command == 0b10000010:
                R0 = self.ram[self.pc+1]
                num_LDI = self.ram[self.pc+2]
                self.reg[R0] = num_LDI
                self.pc += 3
            # if command is MUL
            elif command == 0b10100010:
                num_LDI1 = self.reg[self.ram[self.pc + 1]]
                num_LDI2 = self.reg[self.ram[self.pc + 2]]
                print(num_LDI1 * num_LDI2)
                self.pc += 3
            # if command is PRN
            elif command == 0b01000111:
                num_LDI = self.reg[self.ram[self.pc + 1]]
                print(num_LDI)
                self.pc += 2
            # if command is HLT
            elif command == 0b00000001:
                running = False
                self.pc = 0
                # shutdown
            else:
                # if command is non recognizable
                print(f"Unknown instruction {command}")
                sys.exit(1)
        