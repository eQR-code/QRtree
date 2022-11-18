from .three_address_code import ThreeAddressCode, ComparativeOperand, Instruction
from .scanner import Scanner
import ply.yacc as yacc

class Parser:

    tokens = Scanner.tokens

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
                | printex_statement
                | if_statement
                | ifc_statement
                | goto_statement
        '''
        p[0] = [p[1]]

    def p_lineno(self, p):
        '''
        lineno : OPEN_ROUND INT CLOSE_ROUND
        '''
        p[0] = p[2]
            
    def p_input_statement_string(self, p):
        '''
        input_statement : lineno INPUT STRING
        '''
        p[0] = ThreeAddressCode(Instruction.INPUT, p[3], None)
    
    def p_inputs_statement_string(self, p):
        '''
        inputs_statement : lineno INPUTS STRING
        '''
        p[0] = ThreeAddressCode(Instruction.INPUTS, p[3], None)
    
    def p_input_statement_reference(self, p):
        '''
        input_statement : lineno INPUT INT
        '''
        p[0] = ThreeAddressCode(Instruction.INPUT, p[3], None)
    
    def p_inputs_statement_reference(self, p):
        '''
        inputs_statement : lineno INPUTS INT
        '''
        p[0] = ThreeAddressCode(Instruction.INPUTS, p[3], None)
    
    def p_print_statement_string(self, p):
        '''
        print_statement : lineno PRINT STRING
        '''
        p[0] = ThreeAddressCode(Instruction.PRINT, p[3], None)
    
    def p_print_statement_reference(self, p):
        '''
        print_statement : lineno PRINT INT
        '''
        p[0] = ThreeAddressCode(Instruction.PRINT, p[3], None)

    def p_printex_statement_string(self, p):
        '''
        printex_statement : lineno PRINTEX STRING
        '''
        p[0] = ThreeAddressCode(Instruction.PRINTEX, p[3], None)

    def p_printex_statement_reference(self, p):
        '''
        printex_statement : lineno PRINTEX INT
        '''
        p[0] = ThreeAddressCode(Instruction.PRINTEX, p[3], None)
    
    def p_if_statement(self, p):
        '''
        if_statement : lineno IF STRING lineno
        '''
        p[0] = ThreeAddressCode(Instruction.IF, p[3], p[4])
    
    def p_ifc_statement(self, p):
        '''
        ifc_statement : lineno IFC comp_expr lineno
        '''
        p[0] = ThreeAddressCode(Instruction.IFC, p[3], p[4])
    
    def p_comp_expr_lt(self, p):
        '''
        comp_expr : LT INT
        '''
        p[0] = (ComparativeOperand.LT, p[2])
    
    def p_comp_expr_lteq(self, p):
        '''
        comp_expr : LTEQ INT
        '''
        p[0] = (ComparativeOperand.LTEQ, p[2])
    
    def p_comp_expr_gt(self, p):
        '''
        comp_expr : GT INT
        '''
        p[0] = (ComparativeOperand.GT, p[2])
    
    def p_comp_expr_gteq(self, p):
        '''
        comp_expr : GTEQ INT
        '''
        p[0] = (ComparativeOperand.GTEQ, p[2])
    
    def p_comp_expr_eq(self, p):
        '''
        comp_expr : EQ INT
        '''
        p[0] = (ComparativeOperand.EQ, p[2])
    
    def p_comp_expr_ne(self, p):
        '''
        comp_expr : NE INT
        '''
        p[0] = (ComparativeOperand.NE, p[2])
    
    def p_comp_expr_lt_float(self, p):
        '''
        comp_expr : LT FLOAT16
            | LT FLOAT32
        '''
        p[0] = (ComparativeOperand.LT, p[2][:-3])
    
    def p_comp_expr_lteq_float(self, p):
        '''
        comp_expr : LTEQ FLOAT16
            | LTEQ FLOAT32
        '''
        p[0] = (ComparativeOperand.LTEQ, p[2][:-3])
    
    def p_comp_expr_gt_float(self, p):
        '''
        comp_expr : GT FLOAT16
            | GT FLOAT32
        '''
        p[0] = (ComparativeOperand.GT, p[2][:-3])
    
    def p_comp_expr_gteq_float(self, p):
        '''
        comp_expr : GTEQ FLOAT16
            | GTEQ FLOAT32
        '''
        p[0] = (ComparativeOperand.GTEQ, p[2][:-3])
    
    def p_comp_expr_eq_float(self, p):
        '''
        comp_expr : EQ FLOAT16
            | EQ FLOAT32
        '''
        p[0] = (ComparativeOperand.EQ, p[2][:-3])
    
    def p_comp_expr_ne_float(self, p):
        '''
        comp_expr : NE FLOAT16
            | NE FLOAT32
        '''
        p[0] = (ComparativeOperand.NE, p[2][:-3])
    
    def p_goto_statement(self, p):
        '''
        goto_statement : lineno GOTO lineno 
        '''
        p[0] = ThreeAddressCode(Instruction.GOTO, p[3], None)

    def p_error(self, p):
        if p:
            print("Line", p.lineno, ": Syntax error at token", p.type)
            self.parser.errok()
        else:
            print("Syntax error at EOF")
        
    def parse(self, code):
        self.lexer.input(code)
        return self.parser.parse(lexer=self.lexer)