# This is Cilent_async.py running on the local client.
# This is an asynchronous running script.

import subprocess
import json
import base64
import time
import sys
import os

# Convert the image_data to b64-encoded payload data:
def get_image_input(file_path):
    with open (file_path, "rb") as f:
        encoded_string = base64.b64encode(f.read())
    return encoded_string.decode('utf-8')

# Get the task_id after posting image to the API:
def get_task_id(url, img_json):

    # This is the command provided in the assignment: 
    # $curl -XPOST "http://localhost:5000/image" -d '{"image_data": "<b64 encoded image>"}'
    equiv_cmd = ['curl','-XPOST', url ,'-d', img_json]

    # Get the task_id:
    task_id = subprocess.check_output(equiv_cmd).decode()
    return task_id

# Get the corresponding text output:
def get_text_output(url, task_id_json):

    # This is the command provided in the assignment: 
    # $curl -XGET "http://localhost:5000/image" -d '{"task_id": "<task id as received from POST /image>"}'

    equiv_cmd = ['curl','-XGET', url ,'-d', task_id_json]

    # Get the corresponding text:
    text_output = subprocess.check_output(equiv_cmd).decode()
    return text_output

if __name__ == "__main__":
    # /image
    url = "http://localhost:5000/image"
    file_path = os.path.join(sys.path[0], "phototest.tif")
    img_bundle = os.path.join(sys.path[0], "img.txt")
    # Firstly, post the sample image and get task_id:
    img_input = get_image_input(file_path)
    img_json = json.dumps({"image_data":img_input})
    task_id = get_task_id(url, img_json)
    print(task_id)

    # A while loop for you to play around:
    cmd = input("Please input your command (type help for help): ")
    while cmd!="exit":
        
        if cmd == "help":
            print("*-----------------* \
            \nUsage: \
            \npost: post the specific image (default: phototest.tif) to the url (default: http://localhost:5000/image) and get task_id back. \
            \nmulti-post: post a batch of images in a row, the names of images are stored in a .txt file (default: img.txt) \
            \nget: get the text output by input the corresponding task_id. \
            \nurl: specify the url. \
            \nfile_path: specify the absolute path for the specific image in post cmd. \
            \nimg_bundle: specify the absolute path for .txt file required in multi-post cmd. \
            \n*-----------------*")

        # Post a new image:
        elif cmd == "post":
            img_input = get_image_input(file_path)
            img_json = json.dumps({"image_data":img_input})
            task_id = get_task_id(url, img_json)
            print(task_id)

        # Post a batch of images in one command
        # The file name of the images are stored in the img.txt file.
        elif cmd == "multi-post":
            with open(img_bundle) as f:
                lines = [line.rstrip('\n') for line in f]
            for i in range(0, len(lines)):
                time.sleep(0.5)
                img_input = get_image_input(os.path.join(sys.path[0],lines[i]))
                img_json = json.dumps({"image_data":img_input})
                task_id = get_task_id(url, img_json)
                print(task_id)

        # Get a text from input task_id:
        elif cmd == "get":
            input_id = input("Please input your task_id: ")
            task_id_json = json.dumps({"task_id":input_id})
            text = get_text_output(url, task_id_json)
            print(text)
        
        # Change the url and file path
        elif cmd == "url":
            url = input("Please input your url: ")
        elif cmd == "file_path":
            file_path = input("Please input your file_path: ")
        elif cmd == "img_bundle":
            img_bundle = input("Please input your img_bundle: ")
        
        else:
            print("Unrecognized command. Please input again.")
        cmd = input("Please input your command: ")
    print("Client-async exited.")