# QRtree compiler

The QRtree compiler is the first compiler that allows the generation of a QR code containing an executable program (which is named eQR code) and executed it.
This repository contains all the tool chain needed to compile the QRscript dialect named **QRtree** into QRtreebytecode, and then to insert the QRtreebytecode into a QR code. It also contains the tools for the inverse process to translate the QR code into QRtreebytecode and create an HTML page for the execution of the program.

# Acknowledgment
Please, cite this software (even if you just use a part of it) as:
- S. Scanzio, M. Rosani, and M. Scamuzzi, “QRtree software,” GitHub. [Online]. Available: [https://github.com/eQR-code/QRtree](https://github.com/eQR-code/QRtree)


## Dependencies

This project is written for Python 3.8 or above and is based on the following packages:
- `qrcode`, for encoding the QR code
- `ply`, for parsing the language
- `opencv-python`, for manipulating and loading the image of the QR code
- `pyzbar`, for decoding the QR code
- `argparse`, for the CLI

## Usage

The `QRtree.py` file is the main access point for both compilation and decompilation.

It requires two positional arguments:
- **action**, that can be `encode` or `decode`
- **input**, that is the path to the file to process

Other optional arguments are:
- **-d**, **--debug**, if it is present the compiler prints debug information
- **-o OUTPUT**, **--output OUTPUT**, the optional output file name, if missing the input file name is used
- **--no-cleanup**, if present the temporary files created during the compilation are kept
- **-h**, **--help**, prints help informations

## Example

### Compile a QRtree script

For example, you write a simple test code and save it in `test.txt`.
```
print "hello world!"
```

To compile it and obtain the QR code you have to use the `encode` action.
```bash
python QRtree.py encode test.txt
```

This produces a file called `test.png` containing the QR code.

### Execute a QRtree QR code

For example you have taken a picture of a QR code and saved it as `photo.png`.

To execute it you have to use the `decode` action.
```bash
python QRtree.py decode photo.png
```

This produces a file called `photo.html` and automatically opens it in the default browser of your machine starting the execution.

# QRtree
QRtree is project aim at embedding a program that implements a decision three into a QR code. QRtree is one of the possibile dialects that can be embedded in a QR code, and all the possible dialects are named QR script.

The QR tree dialect was first defined in the following specifications [[2]](https://doi.org/10.48550/arXiv.2403.04708) and [[3]](https://doi.org/10.48550/arXiv.2403.04716).

# Release history
- 2024/03/13: Version v1.0 released. Contributors that worked on this edition are Stefano Scanzio, Matteo Rosani, and Mattia Scamuzzi [[3]](https://github.com/eQR-code/QRtree).

# Notes
- The eQR code was generated using the ``binary'' mode.
- In the implementation it was privilaged the maximum possible ``correction level`` at the cost of having a higher ``version``, in order to improve reliability of QR code read operations.

# Limitations
If compared with the specifications defined in [[2]](https://doi.org/10.48550/arXiv.2403.04708) and [[3]](https://doi.org/10.48550/arXiv.2403.04716).
The version v1.0 has the following limitations:
- References are encoded with an extensible format limited to the following cases 4 bits, 8 bits, 16 bits and 32 bits
- Jumps are encoded with an extensible format limited to the following cases 4 bits, 8 bits, 16 bits and 32 bits
- The DICT type is not handled
- Header parts (not QRscript and QRtree headers) are not implemented
- When the ``--no-cleanup`` option is used, the generated file with extension .bin containing the QRbytecode binary representation of the code does not have either the QRscript or the QRtree headers. Both headers are encoded in the generated eQR code, and in particular, the following sequence of bits are included: the needed padding to have the QRbytecode multiple of 8 bits, 0 for the continuation, 0000 for security, 0 for URL, 0000 for dialect, 0001 for version, 0 to indicate the absence of the QRtree header.
 
# References
- [1] S. Scanzio, G. Cena and A. Valenzano, “QRscript: Embedding a Programming Language in QR codes to support Decision and Management,” 27th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA 2022), 2022, pp. 1-8. doi: [10.1109/ETFA52439.2022.9921530](https://doi.org/10.1109/ETFA52439.2022.9921530) (**First paper about QRscript and QRtree**)
- [2] S. Scanzio, M. Rosani, M. Scamuzzi, and G. Cena, “QRscript specification,” arXiv, pp. 1–13, Mar. 2024. doi: [10.48550/arXiv.2403.04708](https://doi.org/10.48550/arXiv.2403.04708) (**Specification document of QRscript**)
- [3] S. Scanzio, M. Rosani, M. Scamuzzi, and G. Cena, “QRtree - Decision Tree dialect specification of QRscript,” arXiv, pp. 1–32, Mar. 2024. doi: [10.48550/arXiv.2403.04716](https://doi.org/10.48550/arXiv.2403.04716) (**Specification document of QRtree**)
- [4] S. Scanzio, M. Rosani, and M. Scamuzzi, “QRtree software,” GitHub. [Online]. Available: [https://github.com/eQR-code/QRtree](https://github.com/eQR-code/QRtree) (**This software**)


# Contributors
- [Stefano Scanzio](https://www.skenz.it/ss): was the first to propose the possibility to embed a program in a QR code, he proposed most of the programming language, and he coordinates this project
- [Matteo Rosani]: implemented the high-level language to intermediate language compiler ad the intermediate language to HTML page converter and jointly worked on the creation/reading of the QRCode
- [Mattia Scamuzzi]: implemented all the encoding and decoding part from intermediate representation to binary representation and jointly worked on the creation/reading of the QRCode

