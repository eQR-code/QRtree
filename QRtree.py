import argparse
import os
import webbrowser
import encode.HighLevelToIntermediate.main as HighLevelToIntermediate
import encode.IntermediateToeQRbytecode.main as IntermediateToeQRbytecode
import encode.eQRbytecodeToeQRcode.main as eQRbytecodeToeQRcode

import decode.eQRcodeToeQRbytecode.main as eQRcodeToeQRbytecode
import decode.eQRbytecodeToIntermediate.main as eQRbytecodeToIntermediate
import decode.IntermediateToHTML.main as IntermediateToHTML

def main(args):
    if args.type == "encode":
        main_encode(args)
    elif args.type == "decode":
        main_decode(args)
    else:
        print("Error")
    
def main_encode(args):
    HighLevelToIntermediate.encode(args.input, args.debug)
    IntermediateToeQRbytecode.encode(args.input, args.debug)
    if args.output is None:
        args.output = f"{os.path.splitext(args.input)[0]}.png"
    eQRbytecodeToeQRcode.encode(args.input, args.output)

    if not args.no_cleanup:
        os.remove(f"{os.path.splitext(args.input)[0]}.qr")
        os.remove(f"{os.path.splitext(args.input)[0]}.bin")

def main_decode(args):
    eQRcodeToeQRbytecode.decode(args.input)
    eQRbytecodeToIntermediate.decode(args.input, args.debug)
    if args.output is None:
        args.output = f"{os.path.splitext(args.input)[0]}.html"
    IntermediateToHTML.decode(args.input, args.output, args.debug)

    if not args.no_cleanup:
        os.remove(f"{os.path.splitext(args.input)[0]}.bin")
        os.remove(f"{os.path.splitext(args.input)[0]}.qr")

    # HTML page automatically opens on browser
    webbrowser.open_new(f"file://{os.path.realpath(args.output)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("type", choices=["encode", "decode"], help="Indicates the type of action")
    parser.add_argument("input", type=str, help="The input file to process")
    parser.add_argument("-o", "--output", type=str, nargs='?', help="The optional output file")
    parser.add_argument("-d", "--debug", action='store_true', help="Prints the debug output of parser and scanner")
    parser.add_argument("--no-cleanup", action='store_true', help="Specifies that the temporary files are not to be deleted")
    main(parser.parse_args())