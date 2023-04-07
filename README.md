# QRtree compiler

This repository contains the tools used to compile the QRscript dialect QRtree into QRtree bytecode, then into a QR code. It also contains the tools for the inverse process to decompile the QR code into QRtree bytecode and create an HTML page to execute the program.

## Dependencies

This project is written for Python 3.8 or above and is based on the following packages:
- `qrcode`, for encoding the QR code
- `ply`, for parsing the language
- `opencv-python`, for manipulating and loading the image of the QR code
- `pyzbar`, for decoding the QR code
- `argparse`, for the CLI

## Usage

The `main.py` file is the main access point for both compilation and decompilation.

It requires two positional arguments:
- **action**, that can be `encode` or `decode`
- **input**, that is the path to the file to process

Other optional arguments are:
- **-d**, **--debug**, if it is present the compiler prints debug information
- **-o OUTPUT**, **--output OUTPUT**, the optional output file name, a default name is used if missing
- **--no-cleanup**, if present the temporary files created during the compilation are kept
- **-h**, **--help**, prints help informations

## Example

### Compile a QRtree script

For example you write a simple test code and save it in `test.txt`.
```
print "hello world!"
```

To compile it and obtain the QR code you have to use the `encode` action.
```bash
python main.py encode test.txt
```

This produces a file called `out.png` containing the QR code.

### Execute a QRtree QR code

For example you have taken a picture of a QR code and saved it as `photo.png`.

To execute it you have to use the `decode` action.
```bash
python main.py decode photo.png
```

This produces a file called `out.html` and automatically opens it in the default browser of your machine starting the execution.





# Punti vari (TB DELETED)
- [ ] I primi bit del IQR code devono essere 1000000000000000000001 cioè un 1 seguito da 16 zeri
- [ ] Rinominare il file main.py nella radice in QRtree.py
- [ ] Occorre capire quali sono le varie mancanze rispetto alle specifiche (forse perché non ci sono ancora le specifiche scritte) 
  - Estensibilita' 4 8 12 per i salti
  - Per gli interi 16 32 con segno CA2 (Verificare?)
  - f16 f32 per i float
- [X] Non ho capito come si fa a selezionare la rappresentazione delle stringhe e se effettivamente è stata gestita la possibilità di uscare sia stringhe di tipo ASCII-7 che UTF8. Quando si riceve la stringa da three addesss code capisco se posso codificarla su ASCII-7. Metto 00 su ASCII-7, 01 su UTF-8. Verificare? 10 DICT    !! ESTENSIONE
<ntype> 00 INT16  01 INT32  10 FLOAT16    11 FLOAT32

NOTA: header non implementato

# QRtree
QRtree is project aim at embedding a program that implements a decision three into a QR code. QRtree is one of the possibile dialects that can be embedded in a QR code, and all the possible dialects are named QR script.

The QR tree dialect was firtly defined in the following specifications: LINK AL DOCUMENTO CHE STIAMO REALIZZANDO SU OVERLEAF

# Release history
- 2023/01/15: Version v1.0 released. Contributors that worked on this edition are Stefano Scanzio, Matteo Rosani, and Mattia Scamuzzi

# Installation

# Short description

# Usage


# Limitations
If compared with the specifications defined in LINK AL DOCUMENTO CHE STIAMO REALIZZANDO SU OVERLEAF
The version v1.0 has the following limitation:
- I riferimenti sono condificati con codifica estensibile 4 8 12
- Non è implementato l'header
- I jump sono codificati con codifica estensibile 4 8 12



# Contributors
- [Stefano Scanzio](https://www.skenz.it/ss): was the first to propose the possibility to embed a program in a QR code, he proposed most of the programming language, and he coordinates this project
- [Matteo Rosani]: METTETE COSA AVETE FATTO
- [Mattia Scamuzzi]:

