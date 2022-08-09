from imgtest import *
import subprocess

file_path = "./phototest.tif"
output_string = get_input(file_path)
obj = {'image_data': output_string}

print(subprocess.check_output(['curl','-XPOST','"http://localhost:5000/image-sync"','-d', obj]))
