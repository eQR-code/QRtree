from .myScanner import Scanner
from .myParser import Parser
import os

def encode(file, debug):
    fileName = os.path.splitext(file)[0]
    scanner = Scanner(debug)
    parser = Parser(scanner, fileName, debug)

    parser = parser.parser

    with open(f"{fileName}.qr", 'r', encoding='utf-8') as input:
        parser.parse(input.read())