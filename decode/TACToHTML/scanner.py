import re
import ply.lex as lex
import ply.yacc as yacc

class Scanner():

    tokens = [
        "INPUT", 
        "INPUTS", 
        "INT", 
        "FLOAT16",
        "FLOAT32",
        "STRING", 
        "IF", 
        "IFC", 
        "PRINT", 
        "PRINTEX", 
        "GOTO", 
        "LT", 
        "LTEQ",
        "GT", 
        "GTEQ",
        "EQ", 
        "NE",
        "OPEN_ROUND",
        "CLOSE_ROUND"
    ]

    def __init__(self, debug=False):
        self.lexer = lex.lex(module=self, debug=debug)
    
    t_INPUT = r'input'
    t_INPUTS = r'inputs'
    t_IF = r'if'
    t_IFC = r'ifc'
    t_PRINT = r'print'
    t_PRINTEX = r'printex'
    t_GOTO = r'goto'
    t_LT = r'\<'
    t_LTEQ = r'\<\='
    t_GT = r'\>'
    t_GTEQ = r'\>\='
    t_EQ = r'\=\='
    t_NE = r'\!\='
    t_OPEN_ROUND = r'\('
    t_CLOSE_ROUND = r'\)'
    t_FLOAT16 = r'[+-]?([1-9][0-9]*\.[0-9]+|0\.[0-9]+|\.[0-9]+)([eE][+-]?[0-9]+)?f16'
    t_FLOAT32 = r'[+-]?([1-9][0-9]*\.[0-9]+|0\.[0-9]+|\.[0-9]+)([eE][+-]?[0-9]+)?f32'
    t_INT = r'[1-9][0-9]*|0'

    def t_STRING(self, t):
        r'"(?:[^"\\]|\\.)*"'
        t.value = t.value.replace('"', '')
        return t

    def t_comment(self, t):
        r'[\ ]*\#[^\n]*'
        t.lexer.lineno += 1
        pass

    def t_space(self, t):
        r'\ |\n|\r|\r\n'
        pass

    # every symbol that doesn't match with almost one of the previous tokens is considered an error
    def t_error(self, t):
        r'.'
        print("SCANNER ERROR (line", t.lineno, "):", t.value)
        pass

    def input(self, s):
        self.lexer.input(s)

    def token(self):
        return self.lexer.token()