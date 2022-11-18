from .myScanner import Scanner
from .myParser import Parser

def decode(file, debug):
    scanner = Scanner(debug)
    parser = Parser(scanner, debug)

    parser = parser.parser

    with open(f"{file}.txt") as input:
        parser.parse(input.read())
