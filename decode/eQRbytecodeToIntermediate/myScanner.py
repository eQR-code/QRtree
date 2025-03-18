import ply.lex as lex
from ply.lex import TOKEN

class Scanner:

    def __init__(self, debug=False):
        self.lexer = lex.lex(module=self, debug=debug)

    tokens = [
        'ZERO', 'ONE', 'BYTE', 'NUMBER', 'REF4', 'REF8', 'REF16', 'REF32',
    ]

    states = (
        ('ascii7', 'exclusive'),
        ('utf8', 'exclusive'), 
        ('n16', 'exclusive'),
        ('n32', 'exclusive'),
        ('ref', 'exclusive'),
    )

    def t_ZERO(self,t):
        r'0'
        return t

    def t_ONE(self,t):
        r'1'
        return t

    def t_ANY_eof(self,t):
        t.lexer.skip(1)

    def t_ANY_error(self,t):
        r'.'
        print("ERROR (Character not recognized): ", t.value)
        return t

    def t_ascii7_BYTE(self,t):
        r'(?!0000011)(0|1){7}'
        return t

    def t_ascii7_LOOKAHEAD(self,t):
        r'(?=0000011)'
        self.lexer.begin('INITIAL')

    def t_utf8_BYTE(self,t):
        r'(?!00000011)(0|1){8}'
        return t

    def t_utf8_LOOKAHEAD(self,t):
        r'(?=00000011)'
        self.lexer.begin('INITIAL')

    def t_n16_NUMBER(self,t):
        r'(0|1){16}'
        self.lexer.begin('INITIAL')
        return t

    def t_n32_NUMBER(self,t):
        r'(0|1){32}'
        self.lexer.begin('INITIAL')
        return t
    
    def t_ref_REF32(self,t):
        r'111111111111111(?!1111111111111111)(0|1){16}'
        self.lexer.begin('INITIAL')
        return t

    def t_ref_REF16(self,t):
        r'1111111(?!11111111)(0|1){8}'
        self.lexer.begin('INITIAL')
        return t

    def t_ref_REF8(self,t):
        r'(?<=1)111(?!1111)(0|1){4}'
        self.lexer.begin('INITIAL')
        return t

    def t_ref_REF4(self,t):
        r'(0|1){3}'
        self.lexer.begin('INITIAL')
        return t

    
