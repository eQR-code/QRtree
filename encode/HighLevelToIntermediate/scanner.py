import re
import ply.lex as lex
import ply.yacc as yacc

class IndentScanner:

    tokens = [
        "INPUT", 
        "INPUTS", 
        "FLOAT16",
        "FLOAT32",
        "INT", 
        "STRING", 
        "IF", 
        "IFC", 
        "ELSE", 
        "COLUMN", 
        "INDENT", 
        "DEDENT",
        "PRINT", 
        "EXIT", 
        "LT", 
        "LTEQ",
        "GT", 
        "GTEQ",
        "EQ", 
        "NE", 
        "NL",
        "WS",
        "TAB",
    ]

    def __init__(self, debug=False):
        self.lexer = lex.lex(module=self, debug=debug)
        self.line_start = True
    
    t_INPUT = r'input'
    t_INPUTS = r'inputs'
    t_IF = r'if'
    t_IFC = r'ifc'
    t_ELSE = r'else'
    t_COLUMN = r':'
    t_PRINT = r'print'
    t_EXIT = r'exit'
    t_LT = r'\<'
    t_LTEQ = r'\<\='
    t_GT = r'\>'
    t_GTEQ = r'\>\='
    t_EQ = r'\=\='
    t_NE = r'\!\='
    t_FLOAT16 = r'[+-]?([1-9][0-9]*\.[0-9]+|0\.[0-9]+|\.[0-9]+)([eE][+-]?[0-9]+)?f16'
    t_FLOAT32 = r'[+-]?([1-9][0-9]*\.[0-9]+|0\.[0-9]+|\.[0-9]+)([eE][+-]?[0-9]+)?f32'
    t_INT = r'[+-]?[1-9][0-9]*|0'

    def t_STRING(self, t):
        r'"(?:[^"\\]|\\.)*"'
        t.value = t.value.replace('"', '')
        return t

    def t_NL(self, t):
        r'\r|\n|\r\n'
        t.lexer.lineno += 1
        return t

    def t_WS(self, t):
        r'\ '
        if self.line_start:
            return t

    def t_TAB(self, t):
        r'\t'
        if self.line_start:
            return t

    def t_comment(self, t):
        r'[\ ]*\#[^\n]*'
        t.lexer.lineno += 1
        pass

    def t_space(self, t):
        r'\ '
        pass

    # every symbol that doesn't match with almost one of the previous tokens is considered an error
    def t_error(self, t):
        r'.'
        print("SCANNER ERROR (line", t.lineno, "):", t.value)
        pass

    def _new_token(type, lineno):
        t = lex.LexToken()
        t.type = type
        t.value = None
        t.lineno = lineno
        return t

    def ws_filter(self):
        ws_counter = 0
        indent_stack = [0]
        indent_spaces = None
        indent_type = None
        indend_count = 0
        for token in iter(self.lexer.token, None):
            if self.line_start and token.type in [ "WS", "TAB" ]:
                if indent_type is None:
                    indent_type = token.type
                if token.type != indent_type:
                    if token.type == "WS":
                        raise Exception(f"SCANNER ERROR (line {self.lexer.lineno}): Wrong indentation type, tabs are used but space was found")
                    else:
                        raise Exception(f"SCANNER ERROR (line {self.lexer.lineno}): Wrong indentation type, spaces are used but tab was found")
                ws_counter += 1
            elif token.type == 'NL':
                self.line_start = True
                ws_counter = 0
            else:
                self.line_start = False
                if indent_type == "WS":
                    if indent_spaces is None:
                        indent_spaces = ws_counter
                    if ws_counter % indent_spaces != 0:
                        raise Exception(f"SCANNER ERROR (line {self.lexer.lineno}): Wrong indentation level {ws_counter} spaces, the indentation levels are of {indent_spaces} spaces")
                    indend_count = ws_counter // indent_spaces
                else:
                    indend_count = ws_counter
                if indent_stack[-1] < indend_count:
                    indent_stack.append(indend_count)
                    yield IndentScanner._new_token("INDENT", self.lexer.lineno)
                elif indent_stack[-1] > indend_count:
                    while indent_stack[-1] > indend_count:
                        yield IndentScanner._new_token("DEDENT", self.lexer.lineno)
                        indent_stack.pop()
                yield token
        #At EOF
        while indent_stack[-1] > 0:
            yield IndentScanner._new_token("DEDENT", self.lexer.lineno)
            indent_stack.pop()
    
    def input(self, s):
        self.lexer.input(s)
        self.token_stream = self.ws_filter()

    def token(self):
        try:
            return next(self.token_stream)
        except StopIteration:
            return None

class Scanner():

    tokens = [ token for token in IndentScanner.tokens if token not in [ "WS", "NL", "TAB" ] ]

    def __init__(self, debug=False):
        self.lexer = IndentScanner(debug=debug)
        self.debug = debug
        self.token_stream = None
    
    def input(self, s):
        self.lexer.input(s)
        self.token_stream = iter(self.lexer.token, None)
    
    def token(self):
        try:
            token = next(self.token_stream)
            if self.debug:
                print(f"Line {token.lineno}: {token.type}")
            return token
        except StopIteration:
            return None
    