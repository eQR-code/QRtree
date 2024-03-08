############################################################################################################################
# QRtree Software
# This software is released under the GNU General Public License v3.0.
#
# The QRtree software is an implementation of the QRtree dialect, that allows the embedding of decision trees in a QR code.
# For more information, read the file README.md.
#
# Please, cite this software (even if you just use a part of it) as:
# S. Scanzio, M. Rosani, and M. Scamuzzi, “QRtree software,” GitHub. [Online]. Available: https://github.com/eQR-code/QRtree
############################################################################################################################

import pyzbar.pyzbar as pyzbar
import cv2
import os

def decode(file):
    # Load the QR code PNG image
    img = cv2.imread(file)      #Takes the QRCode
    
    mask = cv2.inRange(img, (0,0,0), (100,100,100))
    threasholded = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)       #mask to better decode the QRCode
    img = 255-threasholded

    codes = pyzbar.decode(img, symbols=[pyzbar.ZBarSymbol.QRCODE])

    if len(codes) == 1:
        qr_data = codes[0].data
        qr_data = "".join([ f"{byte:0>8b}" for byte in _format_bytes(qr_data) ])

        i = 0 
        while qr_data[i] == "0": # Removing padding: 48 is the ASCII code of '0'
            i += 1
        i += 1 # Padding removed

        header_length = 1 + 4 + 1 + 4 + 4 + 1 # Continuation + security profile + url + dialect + version + qrtree_header

        # Write the binary data to a file
        with open(f"{os.path.splitext(file)[0]}.bin", 'w') as f:
            f.write(qr_data[i + header_length:])
    else:
        raise Exception("No QRCode detected")

def _format_bytes(data_in):
    i = 0
    while i < len(data_in):
        byte = data_in[i]
        i += 1
        if byte >= 194:
            next_byte = data_in[i]
            i += 1
            yield int((byte & 0b00011111) << 6 | (next_byte & 0b00111111))
        else:
            yield int(byte)
