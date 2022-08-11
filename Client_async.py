# This is Cilent_async.py running on the local client.
# This is an asynchronous running script.

import subprocess
import json
import base64

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
    file_path = "./phototest.tif"

    # Firstly, post the sample image and get task_id:
    img_input = get_image_input(file_path)
    img_json = json.dumps({"image_data":img_input})
    task_id = get_task_id(url, img_json)
    print(task_id)

    # A while loop for you to play around:
    cmd = input("Please input your command: ")
    while cmd!="exit":
        
        # Post a new image:
        if cmd == "post":
            img_input = get_image_input(file_path)
            img_json = json.dumps({"image_data":img_input})
            task_id = get_task_id(url, img_json)
            print(task_id)

        # Get a text from input task_id:
        if cmd == "get":
            input_id = input("please input your task_id: ")
            task_id_json = json.dumps({"task_id":input_id})
            text = get_text_output(url, task_id_json)
            print(text)
        
        # Change the url and file path
        if cmd == "url":
            url = input("please input your url: ")
        if cmd == "file_path":
            file_path = input("please input your file_path: ")
        
        cmd = input("Please input your command: ")
