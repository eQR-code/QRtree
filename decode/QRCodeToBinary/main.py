import numpy as np
import cv2
from PIL import Image
from pyzbar import pyzbar

def decode(file):
    img = cv2.imread(file)      #Takes the QRCode

    mask = cv2.inRange(img, (0,0,0), (100,100,100))
    threasholded = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)       #mask to better decode the QRCode
    img = 255-threasholded
    
    codes = pyzbar.decode(img, symbols=[pyzbar.ZBarSymbol.QRCODE])

    if len(codes) == 1:
        code = codes[0]

        data = str(bin(int(code.data))[3:])

        with open(f"{file}.txt", 'w') as f:
            f.write(data)
    else:
        raise Exception("No QRCode detected")
