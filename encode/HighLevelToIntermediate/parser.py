from .three_address_code import Instruction, ThreeAddressCode, ComparativeOperand
from .scanner import Scanner
import ply.yacc as yacc

class Parser:

    tokens = Scanner.tokens

    precedence = (
        ('nonassoc', 'ELSE'),
        ('left', 'LT', 'LTEQ', 'GT', 'GTEQ')
    )

    def __init__(self, lexer, debug=False):
        self.parser = yacc.yacc(module=self, debug=debug)
        self.lexer = lexer
    
    def p_progr(self, p):
        '''
        progr : statement_list
        '''
        p[0] = p[1]

    def p_statement_list(self, p):
        '''
        statement_list : statement_list statement
        '''
        if len(p[1]) > 0 and len(p[2]) == 1:
            if p[1][-1].instruction == Instruction.PRINT and p[2][0].instruction == Instruction.PRINTEX and p[2][0].par1 is None:
                p[1][-1].instruction = Instruction.PRINTEX
                p[0] = p[1]
                return
            elif p[1][-1].instruction == Instruction.PRINTEX: # Se ho un'istruzione che fa terminare il programma, le successive sono irraggiungibili
                p[0] = p[1]
                return
        p[0] = p[1] + p[2]
    
    def p_statement_list_statement(self, p):
        '''
        statement_list : statement
        '''
        p[0] = p[1]
    
    def p_statement(self, p):
        '''
        statement : input_statement
                | inputs_statement
                | print_statement
                | exit_statement
        '''
        p[0] = [p[1]]
    
    def p_statement_compound(self, p):
        '''
        statement : if_statement
                | ifc_statement
        '''
        p[0] = p[1]
    
    def p_statement_empty(self, p):
        '''
        statement : empty
        '''
        p[0] = []
            
    def p_input_statement_string(self, p):
        '''
        input_statement : INPUT STRING
        '''
        p[0] = ThreeAddressCode(Instruction.INPUT, p[2], None)
    
    def p_inputs_statement_string(self, p):
        '''
        inputs_statement : INPUTS STRING
        '''
        p[0] = ThreeAddressCode(Instruction.INPUTS, p[2], None)
    
    def p_input_statement_reference(self, p):
        '''
        input_statement : INPUT INT
        '''
        p[0] = ThreeAddressCode(Instruction.INPUT, p[2], None)
    
    def p_inputs_statement_reference(self, p):
        '''
        inputs_statement : INPUTS INT
        '''
        p[0] = ThreeAddressCode(Instruction.INPUTS, p[2], None)
    
    def p_print_statement_string(self, p):
        '''
        print_statement : PRINT STRING
        '''
        p[0] = ThreeAddressCode(Instruction.PRINT, p[2], None)
    
    def p_print_statement_reference(self, p):
        '''
        print_statement : PRINT INT
        '''
        p[0] = ThreeAddressCode(Instruction.PRINT, p[2], None)

    def p_exit_statement(self, p):
        '''
        exit_statement : EXIT
        '''
        p[0] = ThreeAddressCode(Instruction.PRINTEX, None, None)
    
    def p_block(self, p):
        '''
        block : INDENT statement_list DEDENT
        '''
        p[0] = p[2]
    
    def p_if_statement(self, p):
        '''
        if_statement : IF STRING COLUMN block else_if_list
        '''
        if_conditions = [ThreeAddressCode(Instruction.IF, p[2], len(p[5]))]
        if_blocks = [p[4]]
        if len(p[5]) != 0:
            if_blocks[-1].append(ThreeAddressCode(Instruction.GOTO, None, None))
        for i, else_if in enumerate(p[5]):
            if_conditions.append(else_if[0])
            block = else_if[1]
            if i < len(p[5]) - 1:
                block.append(ThreeAddressCode(Instruction.GOTO, None, None))
            if_blocks.append(block)

        for i, (if_condition, if_block) in enumerate(zip(if_conditions, if_blocks)):
            if_condition.par2 = len(if_conditions[i + 1:]) + sum(map(len, if_blocks[:i])) + 1
            if if_block[-1].instruction == Instruction.GOTO:
                if_block[-1].par1 = sum(map(len, if_blocks[i + 1:]))
        
        p[0] = if_conditions + [ThreeAddressCode(Instruction.GOTO, sum(map(len, if_blocks)), None)] + [instruction for block in if_blocks for instruction in block]

    def p_if_statement_else(self, p):
        '''
        if_statement : IF STRING COLUMN block else_if_list ELSE COLUMN block
        '''
        if_conditions = [ThreeAddressCode(Instruction.IF, p[2], len(p[5]))]
        if_blocks = [p[8] + [ThreeAddressCode(Instruction.GOTO, None, None)], p[4]]
        if len(p[5]) != 0:
            if_blocks[-1].append(ThreeAddressCode(Instruction.GOTO, None, None))
        for i, else_if in enumerate(p[5]):
            if_conditions.append(else_if[0])
            block = else_if[1]
            if i < len(p[5]) - 1:
                block.append(ThreeAddressCode(Instruction.GOTO, None, None))
            if_blocks.append(block)
        
        for i, (if_condition, if_block) in enumerate(zip(if_conditions, if_blocks)):
            if_condition.par2 = len(if_conditions[i + 1:]) + sum(map(len, if_blocks[:i + 1]))
            if if_block[-1].instruction == Instruction.GOTO:
                if_block[-1].par1 = sum(map(len, if_blocks[i + 1:]))
        
        p[0] = if_conditions + [instruction for block in if_blocks for instruction in block]

    def p_else_if_list(self, p):
        '''
        else_if_list : else_if_list ELSE IF STRING COLUMN block
        '''
        p[0] = p[1] + [(ThreeAddressCode(Instruction.IF, p[4], None), p[6])]

    def p_else_if_list_empty(self, p):
        '''
        else_if_list : empty
        '''
        p[0] = []
    
    def p_ifc_statement(self, p):
        '''
        ifc_statement : IFC comp_expr COLUMN block else_ifc_list
        '''
        if_conditions = [ThreeAddressCode(Instruction.IFC, p[2], len(p[5]))]
        if_blocks = [p[4]]
        for i, else_if in enumerate(p[5]):
            if_conditions.append(else_if[0])
            block = else_if[1]
            if i < len(p[5]) - 1 and block[-1].instruction != Instruction.PRINTEX:
                block.append(ThreeAddressCode(Instruction.GOTO, None, None))
            if_blocks.append(block)
                
        if_conditions.append(ThreeAddressCode(Instruction.GOTO, sum(map(len, if_blocks)) - 1, None))

        for i, (if_condition, if_block) in enumerate(zip(if_conditions, if_blocks)):
            if_condition.par2 = len(if_conditions[i + 1:]) + sum(map(len, if_blocks[:i + 1]))
            if if_block[-1].instruction == Instruction.GOTO:
                if_block[-1].par1 = sum(map(len, if_blocks[i + 1:]))
        
        p[0] = if_conditions + [instruction for block in if_blocks for instruction in block]
    
    def p_ifc_statement_else(self, p):
        '''
        ifc_statement : IFC comp_expr COLUMN block else_ifc_list ELSE COLUMN block
        '''
        if p[8][-1].instruction != Instruction.PRINTEX:
            p[8].append(ThreeAddressCode(Instruction.GOTO, None, None))
        if_conditions = [ThreeAddressCode(Instruction.IFC, p[2], len(p[5]))]
        if_blocks = [p[8], p[4]]
        for i, else_if in enumerate(p[5]):
            if_conditions.append(else_if[0])
            block = else_if[1]
            if i < len(p[5]) - 1 and block[-1].instruction != Instruction.PRINTEX:
                block.append(ThreeAddressCode(Instruction.GOTO, None, None))
            if_blocks.append(block)
        
        for i, (if_condition, if_block) in enumerate(zip(if_conditions, if_blocks)):
            if_condition.par2 = len(if_conditions[i + 1:]) + sum(map(len, if_blocks[:i + 1]))
            if if_block[-1].instruction == Instruction.GOTO:
                if_block[-1].par1 = sum(map(len, if_blocks[i + 1:]))
        
        p[0] = if_conditions + [instruction for block in if_blocks for instruction in block]

    def p_else_ifc_list(self, p):
        '''
        else_ifc_list : else_ifc_list ELSE IFC comp_expr COLUMN block
        '''
        p[0] = p[1] + [(ThreeAddressCode(Instruction.IFC, p[4], None), p[6])]

    def p_else_ifc_list_empty(self, p):
        '''
        else_ifc_list : empty
        '''
        p[0] = []
    
    def p_comp_expr_lt(self, p):
        '''
        comp_expr : LT INT
                | LT FLOAT16
                | LT FLOAT32
        '''
        p[0] = (ComparativeOperand.LT, p[2])
    
    def p_comp_expr_lteq(self, p):
        '''
        comp_expr : LTEQ INT
                | LTEQ FLOAT16
                | LTEQ FLOAT32
        '''
        p[0] = (ComparativeOperand.LTEQ, p[2])
    
    def p_comp_expr_gt(self, p):
        '''
        comp_expr : GT INT
                | GT FLOAT16
                | GT FLOAT32
        '''
        p[0] = (ComparativeOperand.GT, p[2])
    
    def p_comp_expr_gteq(self, p):
        '''
        comp_expr : GTEQ INT
                | GTEQ FLOAT16
                | GTEQ FLOAT32
        '''
        p[0] = (ComparativeOperand.GTEQ, p[2])
    
    def p_comp_expr_eq(self, p):
        '''
        comp_expr : EQ INT
                | EQ FLOAT16
                | EQ FLOAT32
        '''
        p[0] = (ComparativeOperand.EQ, p[2])
    
    def p_comp_expr_ne(self, p):
        '''
        comp_expr : NE INT
                | NE FLOAT16
                | NE FLOAT32
        '''
        p[0] = (ComparativeOperand.NE, p[2])

    def p_empty(self, p):
        '''
        empty :
        '''
        pass

    def p_error(self, p):
        if p:
            print("Line", p.lineno, ": Syntax error at token", p.type)
            self.parser.errok()
        else:
            print("Syntax error at EOF")
        
    def parse(self, code):
        self.lexer.input(code)
        return self.parser.parse(lexer=self.lexer)
