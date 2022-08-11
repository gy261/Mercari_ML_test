# This is Cilent_sync.py running on the local client.
# This is a synchronous running script.

import subprocess
import json
import base64
import os
import sys

# Convert the image_data to b64-encoded payload data:
def get_image_input(file_path):
    with open (file_path, "rb") as f:
        encoded_string = base64.b64encode(f.read())
    return encoded_string.decode('utf-8')

# Get the output of tesseract
def get_text_output(url, img_json):

    # This is the command provided in the assignment: 
    # $curl -XPOST "http://localhost:5000/image-sync" -d '{"image_data": "<b64 encoded image>"}'
    equiv_cmd = ['curl','-XPOST', url ,'-d', img_json]

    # Get the output:
    text_output = subprocess.check_output(equiv_cmd).decode()
    return text_output

if __name__ == "__main__":
    # /image-sync
    url = "http://localhost:5000/image-sync"
    file_path = os.path.join(sys.path[0], "phototest.tif")
    img_input = get_image_input(file_path)

    # Convert the image_data to json data type
    img_json = json.dumps({"image_data":img_input})

    # Get the output
    text_output = get_text_output(url, img_json)
    print(text_output)