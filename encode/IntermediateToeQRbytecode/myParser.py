from .myScanner import *
import ply.yacc as yacc
import struct

class Parser:

    def __init__(self,lexer, fileName, debug=False):
        self.parser = yacc.yacc(module=self, debug=debug)
        self.lexer = lexer
        self.output = open(f"{fileName}.bin", "w")
        self.endCharAscii = '0000011'
        self.endCharUtf = '00000011'


    # Encodes the strings in ascii-7 or UTF-8 based on the most suitable and most compact encoding for the specified string
    def stringEncoding(self,string):
        res = ''
        if(string.isascii()):
            res = '00' + ''.join(format(i, '07b') for i in bytearray(string, encoding ='ascii')) + self.endCharAscii
        else:
            res = '01' + ''.join(format(i, '08b') for i in bytearray(string, encoding ='utf-8')) + self.endCharUtf
        return res

    # Functions to encode references using the exponential encoding defined in the paper
    def _exponential_ones_value(self, ones: int) -> int:
        if ones == 0:
            return 0
        if ones == 4:
            return 2**ones - 1
        return self._exponential_ones_value(ones // 2) + 2**(ones // 2) - 1

    def referenceEncoding(self, value) -> str:
        '''
        Exponential format for unsigned ints 
        Lengths: 4, 8, 16
        '''

        if(not str(value).isdigit()):
            raise Exception("The provided reference " + str(value) + " is not a valid one")

        value = int(value)
        length = 4

        while True:
            ones = 0 if length == 4 else length // 2
            max_value = 2**(length - ones) - 1
            cur_value = value - self._exponential_ones_value(ones)
            if cur_value < max_value:
                return "1" * ones + format(cur_value, f'0{4 if length == 4 else length // 2}b')
            length = length * 2

    # Encodes the integers that are not references using two's complement
    def twos_complement_binary(self, n, bits):
        if n < 0:
            n = (1 << bits) + n

        return bin(n)[2:].zfill(bits)

    tokens = Scanner.tokens


    # A program is a list of operations (instructions from the definition of the QRtree dialect)
    def p_prog(self,p):
        '''
        prog : op_list
        '''
        self.output.close()

    def p_op_list(self,p):
        '''
        op_list : op_list op
                | op
        '''

    def p_op(self,p):
        '''
        op : RO INTEGER RC input
            | RO INTEGER RC inputs
            | RO INTEGER RC print
            | RO INTEGER RC printex
            | RO INTEGER RC goto
            | RO INTEGER RC if
            | RO INTEGER RC ifc
        '''

    # Each instruction has its own code, and then it encodes its other parameters 
    # using the appropriate function among the ones listed above

    def p_input(self,p):
        '''
        input : INPUT constant
        '''

        if isinstance(p[2], int):
            p[0] = '0001' + self.referenceEncoding(p[2])
        else:
            p[0] = '0000' + self.stringEncoding(p[2])
        self.output.write(p[0])

    def p_inputs(self,p):
        '''
        inputs : INPUTS constant
        '''

        if isinstance(p[2], int):
            p[0] = '0011' + self.referenceEncoding(p[2])
        else:
            p[0] = '0010' + self.stringEncoding(p[2])
        self.output.write(p[0])

    def p_print(self,p):
        '''
        print : PRINT constant
        '''

        if isinstance(p[2], int):
            p[0] = '0101' + self.referenceEncoding(p[2])
        else:
            p[0] = '0100' + self.stringEncoding(p[2])
        self.output.write(p[0])

    def p_printex(self,p):
        '''
        printex : PRINTEX constant
        '''

        if isinstance(p[2], int):
            p[0] = '0111' + self.referenceEncoding(p[2])
        else:
            p[0] = '0110' + self.stringEncoding(p[2])
        self.output.write(p[0])

    def p_goto(self,p):
        '''
        goto : GOTO RO INTEGER RC
        '''

        p[0] = '100' + self.referenceEncoding(int(p[3]) - int(p[-2]) - 1)
        self.output.write(p[0])

    def p_if(self,p):
        '''
        if : IF constant RO INTEGER RC
        '''

        if isinstance(p[2], int):
            p[0] = '1011' + self.referenceEncoding(p[2])
        else:
            p[0] = '1010' + self.stringEncoding(p[2])
        p[0] = p[0] + self.referenceEncoding(int(p[4]) - int(p[-2]) - 1)
        self.output.write(p[0])

    def p_ifc(self,p):
        '''
        ifc : IFC rel_op operand RO INTEGER RC
        '''

        if isinstance(p[3], int):
            p[0] = '110' + p[2] 
            # Decides how to encode the integer
            if(-32768 <= p[3] <= 32767):
                p[0] = p[0] + '00' + self.twos_complement_binary(p[3], 16)
            else:
                p[0] = p[0] + '01' + self.twos_complement_binary(p[3], 32)
        else:
            # Decides how to encode the floating point
            f = str(p[3]).lower().split("f")
            if(f[1] == "16"):
                p[0] = '110' + p[2] + '10' + format(struct.unpack('!H', struct.pack('!e', float(f[0])))[0], '016b')
            else:
                p[0] = '110' + p[2] + '11' + format(struct.unpack('!I', struct.pack('!f', float(f[0])))[0], '032b')
        p[0] = p[0] + self.referenceEncoding(int(p[5]) - int(p[-2]) - 1)
        self.output.write(p[0])

    def p_constant(self,p):
        '''
        constant : STRING 
                | INTEGER
        '''
    
        p[0] = p[1]

    # Each relational operator has its own code
    def p_rel_op(self,p):
        '''
        rel_op : EQ 
                | NEQ
                | MAJ_EQ 
                | MIN_EQ
                | MAJ 
                | MIN
        '''

        if(p[1] == '=='):
            p[0] = '000'
        elif(p[1] == '!='):
            p[0] = '001'
        elif(p[1] == '<='):
            p[0] = '010'
        elif(p[1] == '>='):
            p[0] = '011'
        elif(p[1] == '<'):
            p[0] = '100'
        elif(p[1] == '>'):
            p[0] = '101'

    def p_operand(self,p):
        '''
        operand : INTEGER
                | REAL
        '''

        p[0] = p[1]

    def p_error(self,p):
        '''
        '''