import cv2
from pyzbar import pyzbar
import os

def decode(file):
    img = cv2.imread(file)      #Takes the QRCode

    detector = cv2.QRCodeDetector()
    
    data, vertices, _ = detector.detectAndDecode(img)

    if len(vertices) == 1:
        bits = "".join([ f"{byte:0>8b}" for byte in data.encode("latin-1") ])

        i = 0 
        while bits[i] == "0": # Removing padding
            i += 1
        i += 1 # Padding removed
        header_length = 1 + 4 + 1 + 4 + 4 # Continuation + security profile + url + dialect + version

        with open(f"{os.path.splitext(file)[0]}.bin", 'w') as f:
            f.write(bits[i + header_length:])
    else:
        raise Exception("No QRCode detected")
