import qrcode
import os

def encode(inputFileName, outputFileName): 

    with open(f"{os.path.splitext(inputFileName)[0]}.bin", 'rb') as f:

        data = f.read()

        continuation = "0"
        security_profile = "0000"
        url = "0"
        dialect = "0000"
        version = "0001"
        padding = "0" * ((8 - (len(continuation) + len(security_profile) + len(url) + len(dialect) + len(version) + len(data) + 1)) % 8) + "1"

        header_data = bytes(f"{padding}{continuation}{security_profile}{url}{dialect}{version}", 'utf-8')

        data = header_data + data

        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)     #Options for the QRCode
        
        qr.add_data(data, optimize=0)       #Adds the data to the QRCode

        qr.make(fit=True)       #Generates the QRCode making sure that the dimension is compliant with the size of the data

        img = qr.make_image(fill_color="black", back_color="white")     #Creates the real QRCode

        img.save(f"{outputFileName}")      #Saves the QRCode in a file