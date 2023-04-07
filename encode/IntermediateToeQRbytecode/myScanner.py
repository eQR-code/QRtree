import ply.lex as lex
from ply.lex import TOKEN

class Scanner:

    def __init__(self, debug=False):
        self.lexer = lex.lex(module=self, debug=debug)

    tokens = [
        'ws', 'nl',
        'INTEGER', 'REAL', 'STRING',
        'INPUT', 'INPUTS', 'PRINT', 'PRINTEX', 'GOTO', 'IF', 'IFC',
        'RO', 'RC', 'EQ', 'NEQ', 'MAJ_EQ', 'MIN_EQ', 'MAJ', 'MIN'
    ]

    t_ignore = r' '

    t_ws = r'([ \t])'

    def t_nl(self,t):
        r'(\r|\n|\r\n)'
        pass

    def t_REAL(self,t):
        r'[+-]?(([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+)|([0-9]+))([eE][-+]?[0-9]+)?(f|F)(16|32)'
        return t

    def t_INTEGER(self,t):
        r'[+-]?[1-9][0-9]*|0'
        return t

    def t_STRING(self,t):
        r'\"(.)*\"'
        return t

    def t_INPUTS(self,t):
        r'inputs'
        return t

    def t_INPUT(self,t):
        r'input'
        return t

    def t_PRINTEX(self,t):
        r'printex'
        return t

    def t_PRINT(self,t):
        r'print'
        return t

    def t_GOTO(self,t):
        r'goto'
        return t

    def t_IFC(self,t):
        r'ifc'
        return t

    def t_IF(self,t):
        r'if'
        return t

    def t_RO(self, t): 
        r'\('
        return t

    def t_RC(self, t):
        r'\)'
        return t

    def t_EQ(self, t):
        r'\=\='
        return t

    def t_NEQ(self, t):
        r'\!\='
        return t

    def t_MAJ_EQ(self, t):
        r'\>\='
        return t

    def t_MIN_EQ(self, t):
        r'\<\='
        return t

    def t_MAJ(self, t):
        r'\>'
        return t

    def t_MIN(self, t):
        r'\<'
        return t

    def t_eof(self,t):
        t.lexer.skip(1)

    def t_error(self,t):
        r'.'
        print("ERROR (Character not recognized): ", t.value)
        return t
