from flask import Flask, request, jsonify
import base64
import subprocess
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
# To do list: 1. tesseract multilple images; 2. deep learning model instead of it.

app = Flask(__name__)
id = 0

def task_id_generator():
    global id
    id += 1       
    return str(id).zfill(5)


@app.route('/image-sync', methods=['GET', 'POST'])
def image_sync():

    if request.method == 'GET':
        return "Server is on. Please run Client.py to get text from images."
    
    if request.method == 'POST':
        
        # time.sleep(10)
        img = request.get_json(force=True)
        img_data = base64.b64decode(img['image_data'].encode())
        
        id = task_id_generator()
        image_name = "submit_image_" + id
        text_name = "task_" + id

        open(image_name, "wb").write(img_data)
        ocr_cmd = ['tesseract', '--psm', '1', '--oem', '1', image_name, text_name]
        subprocess.run(ocr_cmd, stdout=subprocess.PIPE)
        
        text = subprocess.check_output(['cat',text_name+'.txt']).decode('utf-8')
        
        text_json = {"text":text}
        return text_json




# test this..
class Tasks:
    def __init__(self):
        # id:state
        self.task = {}
        self.id = 0
        self.unsolved = set()

    def new(self):
        task_id = str(self.id).zfill(5)
        self.id += 1 
        self.task[task_id] = "pending"
        self.unsolved.add(task_id)
        return task_id
    
    def done(self, task_id):
        self.task[task_id] = "finished"

    def state(self, task_id):
        if task_id not in self.task:
            return "id_not_exist"
        return self.task[task_id]

    def notified(self):
        if len(self.unsolved)!=0:
            for i in self.unsolved.copy():
                if self.task[i] == "finished":
                    self.unsolved.remove(i)
                    print("task_id: ",i," - job done at ",datetime.now())

    def ocr_cmd_run(self, image_name, text_name, task_id):
        print("job", task_id, "processing...")
        ocr_cmd = ['tesseract', '--psm', '1', '--oem', '1', image_name, text_name, 'quiet']
        subprocess.run(ocr_cmd, stdout=subprocess.PIPE)
        time.sleep(0.5)
        self.done(task_id)

Task_set = Tasks()
sched = BackgroundScheduler(daemon=True)
sched.add_job(Task_set.notified,'interval',seconds=2)
sched.start()

ocr = BackgroundScheduler(daemon=True)
ocr.start()

@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == 'GET':
        task_id = request.get_json(force=True)
        task_id = task_id['task_id']
        state = Task_set.state(task_id)
    
        if (state == "id_not_exist") or (state == "pending"):
            task_text = "null"
        else:
            task_name = "task_" + task_id
            task_text = subprocess.check_output(['cat',task_name+'.txt']).decode('utf-8')    

        text_json = jsonify({"task_id": task_text})
        return text_json

    if request.method == 'POST':
        
        img = request.get_json(force=True)
        img_data = base64.b64decode(img['image_data'].encode())
        
        task_id = Task_set.new()
        image_name = "submit_image_" + task_id
        text_name = "task_" + task_id

        open(image_name, "wb").write(img_data)
        
        # text = subprocess.check_output(['cat',text_name+'.txt']).decode('utf-8')
        ocr.add_job(Task_set.ocr_cmd_run,  args=[image_name, text_name, task_id])
        
        id_json = jsonify({"task_id":task_id})
        return id_json

if __name__ == "__main__":
    app.run(debug=True)