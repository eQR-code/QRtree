from .myScanner import *
import ply.yacc as yacc
import struct

class Parser:

    def __init__(self,lexer, fileName, debug=False):
        self.parser = yacc.yacc(module=self, debug=debug)
        self.lexer = lexer
        self.output = open(f"{fileName}.qr", "w")
        self.curline = 0
        self.endChar = ""

    def binStrToStrAscii(self,string):
        res = ""
        s = [string[idx:idx + 7] for idx in range(0, len(string), 7)]
        for char in s:
            i = int(char,2)
            c = chr(i)
            res += c
        return res

    def binStrToStrUtf(self,string):
        res = ""
        s = [string[idx:idx + 8] for idx in range(0, len(string), 8)]
        for char in s:
            i = int(char,2)
            c = chr(i)
            res += c
        return res

    def binRefToIntRef(self, string):
        l = len(string)
        if(l == 4):
            return int(string, 2)
        elif(l == 12):
            return int(string[4:], 2) + 15
        elif(l == 24):
            return int(string[12:], 2) + 270

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
        op : input
            | inputs
            | print
            | printex
            | goto
            | if
            | ifc
        '''
    
    def p_input(self,p):
        '''
        input : ZERO ZERO ZERO ZERO constant
                | ZERO ZERO ZERO ONE number
        '''

        if(p[4] == '0'):
            if(p[5][0] == "00"):
                self.output.write("(" + str(self.curline) + ") input " + '"' + self.binStrToStrAscii(p[5][1]) + '"' + '\n')
            else:
                self.output.write("(" + str(self.curline) + ") input " + '"' + self.binStrToStrUtf(p[5][1]) + '"' + '\n')
        else:
            self.output.write("(" + str(self.curline) + ") input " + str(self.binRefToIntRef(p[5])) + '\n')
        self.curline += 1

    def p_inputs(self,p):
        '''
        inputs : ZERO ZERO ONE ZERO constant
                | ZERO ZERO ONE ONE number
        '''

        if(p[4] == '0'):
            if(p[5][0] == "00"):
                self.output.write("(" + str(self.curline) + ") inputs " + '"' + self.binStrToStrAscii(p[5][1]) + '"' + '\n')
            else:
                self.output.write("(" + str(self.curline) + ") inputs " + '"' + self.binStrToStrUtf(p[5][1]) + '"' + '\n')
        else:
            self.output.write("(" + str(self.curline) + ") inputs " + str(self.binRefToIntRef(p[5])) + '\n')
        self.curline += 1

    def p_print(self,p):
        '''
        print : ZERO ONE ZERO ZERO constant
                | ZERO ONE ZERO ONE number
        '''

        if(p[4] == '0'):
            if(p[5][0] == "00"):
                self.output.write("(" + str(self.curline) + ") print " + '"' + self.binStrToStrAscii(p[5][1]) + '"' + '\n')
            else:
                self.output.write("(" + str(self.curline) + ") print " + '"' + self.binStrToStrUtf(p[5][1]) + '"' + '\n')
        else:
            self.output.write("(" + str(self.curline) + ") print " + str(self.binRefToIntRef(p[5])) + '\n')
        self.curline += 1

    def p_printex(self,p):
        '''
        printex : ZERO ONE ONE ZERO constant
                | ZERO ONE ONE ONE number
        '''

        if(p[4] == '0'):
            if(p[5][0] == "00"):
                self.output.write("(" + str(self.curline) + ") printex " + '"' + self.binStrToStrAscii(p[5][1]) + '"' + '\n')
            else:
                self.output.write("(" + str(self.curline) + ") printex " + '"' + self.binStrToStrUtf(p[5][1]) + '"' + '\n')
        else:
            self.output.write("(" + str(self.curline) + ") printex " + str(self.binRefToIntRef(p[5])) + '\n')
        self.curline += 1

    def p_goto(self,p):
        '''
        goto : ONE ZERO ZERO number
        '''
        
        self.output.write("(" + str(self.curline) + ") goto (" + str(self.binRefToIntRef(p[4]) + self.curline + 1) + ")" + '\n')
        self.curline += 1

    def p_if(self,p):
        '''
        if : ONE ZERO ONE ZERO constant number
                | ONE ZERO ONE ONE number number
        '''

        if(p[4] == '0'):
            if(p[5][0] == "00"):
                self.output.write("(" + str(self.curline) + ") if " + '"' + self.binStrToStrAscii(p[5][1]) + '"' + " (" + str(self.binRefToIntRef(p[6]) + self.curline + 1) + ")" + '\n')
            else:
                self.output.write("(" + str(self.curline) + ") if " + '"' + self.binStrToStrUtf(p[5][1]) + '"' + " (" + str(self.binRefToIntRef(p[6]) + self.curline + 1) + ")" + '\n')
        else:
            self.output.write("(" + str(self.curline) + ") if " + str(self.binRefToIntRef(p[5])) + " (" + str(self.binRefToIntRef(p[6]) + self.curline + 1) + ")" + '\n')
        self.curline += 1

    def p_ifc(self,p):
        '''
        ifc : ONE ONE ZERO rel_op ZERO operand number
                | ONE ONE ZERO rel_op ONE operand number
        '''

        if(p[5] == '0'):
            self.output.write("(" + str(self.curline) + ") ifc " + p[4] + " " + str(int(p[6][1], 2)) + " (" + str(self.binRefToIntRef(p[7]) + self.curline + 1) + ")" + '\n')
        else:
            if(p[6][0] == '0'):
                self.output.write("(" + str(self.curline) + ") ifc " + p[4] + " " + str(struct.unpack('!e',struct.pack('!H', int(p[6][1], 2)))[0]) + "f16 (" + str(self.binRefToIntRef(p[7]) + self.curline + 1) + ")" + '\n')
            else:
                self.output.write("(" + str(self.curline) + ") ifc " + p[4] + " " + str(struct.unpack('!f',struct.pack('!I', int(p[6][1], 2)))[0]) + "f32 (" + str(self.binRefToIntRef(p[7]) + self.curline + 1) + ")" + '\n')
        self.curline += 1

    def p_operand(self,p):
        '''
        operand : optype NUMBER
        '''

        p[0] = [ p[1], p[2] ]

    def p_optype(self,p):
        '''
        optype : ZERO
                | ONE
        '''

        p[0] = p[1]
        if(p[1] == '0'):
            self.lexer.lexer.begin('n16')
        else:
            self.lexer.lexer.begin('n32')

    def p_constant(self,p):
        '''
        constant : stype byte_list eot
                | stype eot
        '''

        if(len(p) == 4):
            p[0] = [ p[1], p[2] ]
        else:
            p[0] = [ p[1], "" ]

    def p_stype(self,p):
        '''
        stype : ZERO marker2 ZERO
            | ZERO marker3 ONE
        '''

        p[0] = p[1] + p[3]

    def p_marker2(self,p):
        '''
        marker2 :
        '''

        self.lexer.lexer.begin('ascii7')

    def p_marker3(self,p):
        '''
        marker3 :
        '''

        self.lexer.lexer.begin('utf8')
            
    def p_byte_list(self,p):
        '''
        byte_list : byte_list BYTE
                    | BYTE
        '''

        if(len(p) == 3):
            p[0] = p[1] + p[2]
        else:
            p[0] = p[1]

    def p_number(self,p):
        '''
        number : marker ref
        '''

        p[0] = p[2]

    def p_marker(self,p):
        '''
        marker :
        '''
        
        self.lexer.lexer.begin('ref')

    def p_ref(self,p):
        '''
        ref : ZERO REF4
            | ONE REF4
            | ONE REF8
            | ONE REF12
        '''

        p[0] = p[1] + p[2]

    def p_rel_op(self,p):
        '''
        rel_op : ZERO ZERO ZERO 
                | ZERO ZERO ONE
                | ZERO ONE ZERO 
                | ZERO ONE ONE
                | ONE ZERO ZERO 
                | ONE ZERO ONE
        '''

        rel_op = "" + p[1] + p[2] + p[3]
        if(rel_op == '000'):
            p[0] = '=='
        elif(rel_op == '001'):
            p[0] = '!='
        elif(rel_op == '010'):
            p[0] = '<='
        elif(rel_op == '011'):
            p[0] = '>='
        elif(rel_op == '100'):
            p[0] = '<'
        elif(rel_op == '101'):
            p[0] = '>'

    def p_eot(self,p):
        '''
        eot : ZERO ZERO ZERO ZERO ZERO ONE ONE
            | ZERO ZERO ZERO ZERO ZERO ZERO ONE ONE
        '''

    def p_error(self,p):
        '''
        '''
