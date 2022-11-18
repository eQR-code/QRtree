import argparse
import os
import webbrowser
import encode.QRscriptToTAC.main as QrScriptToTac
import encode.TACToBinary.main as TacToBin
import encode.BinaryToQRCode.main as BinToQrCode

import decode.QRCodeToBinary.main as QrCodeToBin
import decode.BinaryToTAC.main as BinToTac
import decode.TACToHTML.main as TacToHtml

def main(args):
    if args.type == "encode":
        main_encode(args)
    elif args.type == "decode":
        main_decode(args)
    else:
        print("Error")
    
def main_encode(args):
    QrScriptToTac.encode(args.input, args.debug)
    TacToBin.encode(args.input, args.debug)
    if args.output is None:
        args.output = "out.png"
    BinToQrCode.encode(args.output)

    if not args.no_cleanup:
        os.remove(f"{args.input}.qr")
        os.remove("binary.txt")

def main_decode(args):
    QrCodeToBin.decode(args.input)
    BinToTac.decode(args.input, args.debug)
    if args.output is None:
        args.output = "out.html"
    TacToHtml.decode(args.output, args.debug)

    if not args.no_cleanup:
        os.remove(f"{args.input}.txt")
        os.remove("output.txt")

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