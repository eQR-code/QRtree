from .three_address_code import ThreeAddressCode, Instruction
from .scanner import Scanner
from .parser import Parser
import argparse
import os

def encode(file, debug):
    s = Scanner(debug=debug)
    p = Parser(s, debug=debug)
    file_content = None

    with open(file, mode='r') as f:
        file_content = f.read()

    code = p.parse(file_content)
    # Porto i jump a assoluti
    for i, line in enumerate(code):
        if line.instruction == Instruction.IF or line.instruction == Instruction.IFC:
            line.par2 = line.par2 + i + 1
        elif line.instruction == Instruction.GOTO:
            line.par1 = line.par1 + i + 1

    # Scrivo il file in formato testuale
    with open(f"{os.path.splitext(file)[0]}.qr", mode='w') as f:
        for i, line in enumerate(code):
            print(f"({i}) {line.to_asm()}", file=f)
    
    return code

def main(args):
    for file in args.files:
        code = encode(file, args.debug)

        if args.verbose:
            print(f"Line  |  {'Instruction': <{ThreeAddressCode.COLUMN_WIDTH}}|  {'Arg1': <{ThreeAddressCode.COLUMN_WIDTH}}|  {'Arg2': <{ThreeAddressCode.COLUMN_WIDTH}}")
            print("-" * (7 + (ThreeAddressCode.COLUMN_WIDTH + 3) * 3))
            for (i, line) in enumerate(code):
                print(f"({i:03}) |  {line}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="QRscript compiler to three-address code")
    parser.add_argument("files", metavar="file", type=str, nargs='+')
    parser.add_argument("-d", "--debug", action='store_true', help="Prints the debug output of parser and scanner")
    parser.add_argument("-v", "--verbose", action='store_true', help="Prints the output three-address code")
    args = parser.parse_args()
    main(args)