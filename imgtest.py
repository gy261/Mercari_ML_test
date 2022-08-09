import os
from PIL import Image
import base64

def get_input(file):
    with open (file, "rb") as f:
        encoded_string = base64.b64encode(f.read())
    return encoded_string

#img = Image.open('phototest.tif')
#img.show()

