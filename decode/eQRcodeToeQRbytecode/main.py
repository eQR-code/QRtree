import pyzbar.pyzbar as pyzbar
from PIL import Image
import os

def decode(file):
    # Load the QR code PNG image
    with Image.open(file) as img:
        qr_data = pyzbar.decode(img)[0].data

    i = 0 
    while qr_data[i] == 48: # Removing padding: 48 is the ASCII code of '0'
        i += 1
    i += 1 # Padding removed

    header_length = 1 + 4 + 1 + 4 + 4 # Continuation + security profile + url + dialect + version

    # Write the binary data to a file
    with open(f"{os.path.splitext(file)[0]}.bin", 'w') as f:
        f.write(qr_data[i + header_length:].decode('utf-8'))
