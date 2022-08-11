# Mercari_ML_test

This is Guo Yang's Submission for the Mercari ML test.

## Description

The codes implements the required API.

* ```Server.py```: Run on the local server. Implement both the ```/image-sync``` and ```/image``` endpoints.

* ```Client_sync.py```: For synchronous OCR. Equivalent to ```curl -POST "http://localhost:5000/image-sync" -d '{"image_data": "<b64 encoded image>"}'```

* ```Client_async.py```: For asynchronous OCR. Equivalent to ```curl -POST "http://localhost:5000/image" -d '{"image_data": "<b64 encoded image>"}'```. Run this file also enters a testing loop, where the user can continuously ```POST``` images, receive ```task_id``` and ```GET``` OCR text back. User can also post a batch of images in a row.

* ```img.txt```: Stores the file names of a batch of images.

* ```<name>.tif```: The test photos.

* For more details, please refer to the comments in the ```<name>.py``` files.

## Getting Started

### Dependencies

* Python version == 3.8.10  
* Flask version == 2.2.2  
* APScheduler version == 3.9.1  
* tesseract version == 4.1.1  


### Installing

```
$ python3 -m pip install flask  
$ python3 -m pip install apscheduler  
$ apt-get update && apt-get install -y tesseract-ocr-eng  
```

### Executing program

Run ```python3 Server.py```

* If you want to test the codes, simply run ```python3 Client_sync.py``` or ```python3 Client_async.py```.

* If you want to change the images you want to send to ```Client_async.py```: First put all your images in the same directory as the ```Client_async.py```, and create a ```<your_image>.txt``` file. Then Run ```python3 Client_async.py```, type ```img_bundle```, enter the absolute path of ```<your_image>.txt```, and run ```multi-post```.

## Help

Type  ```help``` to see valid commands in ```Client_async.py```.



