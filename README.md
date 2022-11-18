# Punti vari (TB DELETED)
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
