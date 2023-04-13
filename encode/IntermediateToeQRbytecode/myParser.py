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

    def stringEncoding(self,string):
        res = ''
        if(string.isascii()):
            res = '00' + ''.join(format(i, '07b') for i in bytearray(string, encoding ='ascii')) + self.endCharAscii
        else:
            res = '01' + ''.join(format(i, '08b') for i in bytearray(string, encoding ='utf-8')) + self.endCharUtf
        return res

    # def referenceEncoding(self, n):
    #     if(n >= 0 and n <= 14):
    #         return format(n, '04b')
    #     elif (n >= 15 and n <= 269):
    #         return '1111' + format(n-15, '08b')
    #     elif (n >= 270 and n <= 65535):
    #         return '111111111111' + format(n-270, '016b')

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
        value = int(value)
        length = 4

        while True:
            ones = 0 if length == 4 else length // 2
            max_value = 2**(length - ones) - 1
            cur_value = value - self._exponential_ones_value(ones)
            if cur_value < max_value:
                return "1" * ones + format(cur_value, f'0{4 if length == 4 else length // 2}b')
            length = length * 2

    tokens = Scanner.tokens

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
            p[0] = '1010'
            p[0] = '1010' + self.stringEncoding(p[2])
        p[0] = p[0] + self.referenceEncoding(int(p[4]) - int(p[-2]) - 1)
        self.output.write(p[0])

    def p_ifc(self,p):
        '''
        ifc : IFC rel_op operand RO INTEGER RC
        '''

        if isinstance(p[3], int):
            p[0] = '110' + p[2] 
            if(p[3] <= 65536):
                p[0] = p[0] + '00' + format(p[3], '016b')
            else:
                p[0] = p[0] + '01' + format(p[3], '032b')
        else:
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