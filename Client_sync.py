import subprocess
import json
import base64

def get_image_input(file_path):
    with open (file_path, "rb") as f:
        encoded_string = base64.b64encode(f.read())
    return encoded_string.decode('utf-8')

def get_text_output(url, img_json):
    equiv_cmd = ['curl','-XPOST', url ,'-d', img_json]
    text_output = subprocess.check_output(equiv_cmd).decode()
    return text_output

if __name__ == "__main__":
    url = "http://localhost:5000/image"
    file_path = "./phototest.tif"
    img_input = get_image_input(file_path)
    img_json = json.dumps({"image_data":img_input})
    text_output = get_text_output(url, img_json)
    
    print(text_output)