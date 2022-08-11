# This is Server.py running on the local server.
# The synchronous and asynchronous http-based API are both implemented here.
# There will be detailed comments for you to understand my codes ('◡')

from flask import Flask, request, jsonify
import base64
import subprocess
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# POST /image-sync API is implemented below:

# This function serves as an ID generator, which generates a task ID when a new image is posted to /image-sync.
# For simplicity, the task ID is just an incremental number of 5 digits (It pads leading zeros if the number is shorter than 5 digits.).
id = 0
def task_id_generator():
    global id
    id += 1       
    return str(id).zfill(5)

# This function implements the main body of POST /image-sync API.
@app.route('/image-sync', methods=['GET', 'POST'])
def image_sync():

    # A simple GET method to check if the Server is on.
    if request.method == 'GET':
        return "Server is on. Please run Client.py to get text from images."
    
    # POST method.
    if request.method == 'POST':
        
        # The input {"image_data": "<b64 encoded image>"} is json data type:
        img = request.get_json(force=True)
        # Then decode the b64-encoded payload data:
        img_data = base64.b64decode(img['image_data'].encode())
        
        # Generate a task ID, which is then used to name the files.
        id = task_id_generator()
        image_name = "submit_image_" + id
        text_name = "task_" + id

        # Write the image_data into an image file
        open(image_name, "wb").write(img_data)

        # Run the command to get output text from ocr_cmd, which will be stored in the text_name file.
        ocr_cmd = ['tesseract', '--psm', '1', '--oem', '1', image_name, text_name]
        subprocess.run(ocr_cmd, stdout=subprocess.PIPE)
        
        # Cat the content in the text_name file:
        text = subprocess.check_output(['cat',text_name+'.txt']).decode('utf-8')
        
        # Return the content in a json data type:
        text_json = {"text":text}
        return text_json



# POST /image and GET /image API are implemented below

# This class is used to manage task and task_id.
class Tasks:

    # initialize: 
    # a dictionary 'task' to store all tasks and their status;
    # an integer number 'id' to generate incremental task ID;
    # a set 'unsolved' to record all tasks not finished.     
    def __init__(self):
        self.task = {}
        self.id = 0
        self.unsolved = set()

    # Add a new task; return the id to name the image and text files.
    def new(self):
        task_id = str(self.id).zfill(5)
        self.id += 1 
        self.task[task_id] = "pending"
        self.unsolved.add(task_id)
        return task_id
    
    # Mark a given task as "finished".
    def done(self, task_id):
        self.task[task_id] = "finished"

    # Check the status of a given task.
    def status(self, task_id):
        if task_id not in self.task:
            return "id_not_exist"
        return self.task[task_id]

    # If a task was unsolved but is now finished , then change its status;
    # Also print out the information: the job is done at what time to notify the Server and User.
    def notified(self):
        if len(self.unsolved)!=0:
            for i in self.unsolved.copy():
                if self.task[i] == "finished":
                    self.unsolved.remove(i)
                    print("task_id: ",i," - job done at ",datetime.now())

    # Process a given task to get the text output:
    def ocr_cmd_run(self, image_name, text_name, task_id):
        print("job", task_id, "processing...")
        ocr_cmd = ['tesseract', '--psm', '1', '--oem', '1', image_name, text_name, 'quiet']
        subprocess.run(ocr_cmd, stdout=subprocess.PIPE)
        time.sleep(0.5)
        self.done(task_id)

Task_set = Tasks()

# This block of codes are used to setup the APScheduler

# Set a Background Scheduler, add the job to notify whether a job is done every 2 seconds:
sched = BackgroundScheduler(daemon=True)
sched.add_job(Task_set.notified,'interval',seconds=2)
sched.start()

# Set a Background Scheduler, waiting for new jobs.
ocr = BackgroundScheduler(daemon=True)
ocr.start()

# This function implements the main body of POST /image and GET /image API.
@app.route('/image', methods=['GET', 'POST'])
def image():

    # GET /image: input task_id, output corresponding text:
    if request.method == 'GET':

        # Get the task_id from command: 
        temp = request.get_json(force=True)
        task_id = temp['task_id']

        # Check the status of the task_id:
        status = Task_set.status(task_id)
        if (status == "id_not_exist") or (status == "pending"):
            task_text = "null"
        
        # if the task_id is finished, then cat the output text from stored text file.
        else:
            task_name = "task_" + task_id
            task_text = subprocess.check_output(['cat',task_name+'.txt']).decode('utf-8')    

        # Return the text
        text_json = jsonify({"task_id": task_text})
        return text_json

    # POST /image: 
    if request.method == 'POST':
        
        # Same idea as image-sync.
        img = request.get_json(force=True)
        img_data = base64.b64decode(img['image_data'].encode())
        
        # Generate task_id and use it to name image and text files.
        task_id = Task_set.new()
        image_name = "submit_image_" + task_id
        text_name = "task_" + task_id

        # Write the image_data into the image file.
        open(image_name, "wb").write(img_data)
        
        # Add background job to run the OCR command line, so that the user does not need to wait
        ocr.add_job(Task_set.ocr_cmd_run,  args=[image_name, text_name, task_id])
        
        # Return the task_id
        id_json = jsonify({"task_id":task_id})
        return id_json

if __name__ == "__main__":
    app.run(debug=True)