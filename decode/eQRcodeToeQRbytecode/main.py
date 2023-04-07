import cv2
from pyzbar import pyzbar
import os

def decode(file):
    img = cv2.imread(file)      #Takes the QRCode
    
    mask = cv2.inRange(img, (0,0,0), (100,100,100))
    threasholded = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)       #mask to better decode the QRCode
    img = 255-threasholded
    
    codes = pyzbar.decode(img, symbols=[pyzbar.ZBarSymbol.QRCODE])

    if len(codes) == 1:
        code = codes[0]

        data = str(bin(int(code.data))[25:])

        with open(f"{os.path.splitext(file)[0]}.bin", 'w') as f:
            f.write(data)
    else:
        raise Exception("No QRCode detected")
