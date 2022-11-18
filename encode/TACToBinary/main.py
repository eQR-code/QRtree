from .myScanner import Scanner
from .myParser import Parser

def encode(file, debug):
    scanner = Scanner(debug)
    parser = Parser(scanner, debug)

    parser = parser.parser

    with open(f"{file}.qr", 'r', encoding='utf-8') as input:
        parser.parse(input.read())