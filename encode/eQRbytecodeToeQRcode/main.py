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

import qrcode
from qrcode.util import QRData, MODE_8BIT_BYTE
import os

def encode(inputFileName, outputFileName): 

    with open(f"{os.path.splitext(inputFileName)[0]}.bin", 'r') as f:

        data = f.read()

        continuation = "0"
        security_profile = "0000"
        url = "0"
        dialect = "0000"
        version = "0001"
        qrtree_header = "0"
        padding = "0" * ((8 - (len(continuation) + len(security_profile) + len(url) + len(dialect) + len(version) + len(qrtree_header) + len(data) + 1)) % 8) + "1"

        data = f"{padding}{continuation}{security_profile}{url}{dialect}{version}{qrtree_header}{data}"

        data = bytes([ int(data[i:i + 8], 2) for i in range(0, len(data), 8) ])

        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)     #Options for the QRCode

        qr.add_data(QRData(data, MODE_8BIT_BYTE, False))       #Adds the data to the QRCode

        qr.make(fit=True)       #Generates the QRCode making sure that the dimension is compliant with the size of the data

        img = qr.make_image(fill_color="black", back_color="white")     #Creates the real QRCode

        img.save(f"{outputFileName}")      #Saves the QRCode in a file
