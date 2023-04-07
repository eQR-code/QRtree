import enum

class Instruction(enum.Enum):
                    # | Par1                        | Par2
    INPUT = 1       # | ref or string               |
    INPUTS = 2      # | ref or string               |
    GOTO = 3        # | instructions to jump        |
    IF = 4          # | string to compare           | jump if true
    IFC = 5         # | value to compare and relop  | jump if true
    PRINT = 6       # | ref or string               |
    PRINTEX = 7     # | ref or string               |

class ComparativeOperand(enum.Enum):

    LT = 1
    LTEQ = 2
    GT = 3
    GTEQ = 4
    EQ = 5
    NE = 6

class ThreeAddressCode:

    COLUMN_WIDTH = 30

    def __init__(self, instruction: Instruction, par1, par2):
        self.instruction = instruction
        self.par1 = par1
        self.par2 = par2

    def to_asm(self):
        if self.instruction == Instruction.INPUT:
            if isinstance(self.par1, str):
                return f"input \"{self.par1}\""
            return f"input {self.par1}"
        elif self.instruction == Instruction.INPUTS:
            if isinstance(self.par1, str):
                return f"inputs \"{self.par1}\""
            return f"inputs {self.par1}"
        elif self.instruction == Instruction.GOTO:
            return f"goto ({self.par1})"
        elif self.instruction == Instruction.IF:
            return f"if \"{self.par1}\" ({self.par2})"
        elif self.instruction == Instruction.IFC:
            if (self.par1[0] == ComparativeOperand.LT):
                return f"ifc < {self.par1[1]} ({self.par2})"
            elif (self.par1[0] == ComparativeOperand.LTEQ):
                return f"ifc <= {self.par1[1]} ({self.par2})"
            elif (self.par1[0] == ComparativeOperand.GT):
                return f"ifc > {self.par1[1]} ({self.par2})"
            elif (self.par1[0] == ComparativeOperand.GTEQ):
                return f"ifc >= {self.par1[1]} ({self.par2})"
            elif (self.par1[0] == ComparativeOperand.EQ):
                return f"ifc == {self.par1[1]} ({self.par2})"
            else:
                return f"ifc != {self.par1[1]} ({self.par2})"
        elif self.instruction == Instruction.PRINT:
            if isinstance(self.par1, str):
                return f"print \"{self.par1}\""
            return f"print {self.par1}"
        else:
            if isinstance(self.par1, str):
                return f"printex \"{self.par1}\""
            elif self.par1 is None:
                return f"printex \"\""
            return f"printex {self.par1}"
    
    def __str__(self):
        if self.instruction == Instruction.IFC:
            return f"{str(self.instruction): <{ThreeAddressCode.COLUMN_WIDTH}}|  {str(self.par1[0]): <23}{str(self.par1[1]): <{ThreeAddressCode.COLUMN_WIDTH - 23}}|  {str(self.par2): <{ThreeAddressCode.COLUMN_WIDTH}}"
        return f"{str(self.instruction): <{ThreeAddressCode.COLUMN_WIDTH}}|  {str(self.par1): <{ThreeAddressCode.COLUMN_WIDTH}}|  {str(self.par2): <{ThreeAddressCode.COLUMN_WIDTH}}"