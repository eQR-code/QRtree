import qrcode
#import numpy as np

def encode(file): 

    with open("binary.txt", 'r') as f:

        data = f.read()

        data = int("1" + data, 2)

        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)     #Options for the QRCode

        qr.add_data(data)       #Adds the data to the QRCode

        qr.make(fit=True)       #Generates the QRCode making sure that the dimension is compliant with the size of the data

        img = qr.make_image(fill_color="black", back_color="white")     #Creates the real QRCode

        img.save(f"{file}")      #Saves the QRCode in a file