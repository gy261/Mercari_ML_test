from flask import Flask, request
import base64
import subprocess
import os
app = Flask(__name__)

print("this is the app:", app)
@app.route('/image-sync', methods=['GET', 'POST'])
def func():
    if request.method == 'GET':
        return "Usage: to be filled in.."
    
    if request.method == 'POST':
        data = base64.b64decode(request.form['image_data'])
        storage = 
        text = subprocess.check_output('tesseract', pathToImages, 'stdout', '--psm', '1', '--oem', '1', 'quiet')
        # run OCR and get results
        # return results.. as a json obj
        # {"text": "<results>"} 
        return data

if __name__ == "__main__":
    print("this is the app:", app)
    app.run(debug=True)