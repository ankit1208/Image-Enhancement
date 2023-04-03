from flask import Flask, request, send_file
from PIL import Image
# import joblib

# import pickle
import os
import demo
import time
import glob
import io



app = Flask(__name__)

# model = joblib.load('demo.py')

def get_latest_file(path,*paths):
    """Returns the name of the latest (most recent) file 
    of the joined path(s)"""
    fullpath = os.path.join(path,*paths)
    files = glob.glob(fullpath)  # You may use iglob in Python3
    if not files:                # I prefer using the negation
        return None                      # because it behaves like a shortcut
    latest_file = max(files, key=os.path.getctime)
    _, filename = os.path.split(latest_file)
    return filename

# Define a route to handle the request
@app.route('/api/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        f = request.files['file']
        os.chdir('D:\\Github_Projects\\Image-Enhancement\\samples\\input')
        f.save(f.filename)
        os.chdir('D:\\Github_Projects\\Image-Enhancement')
        image = demo.demo()
        img = Image.fromarray(image)
        image_object = io.BytesIO()
        img.save(image_object, 'PNG')
        image_object.seek(0)
        return send_file(image_object, mimetype='image/PNG')
    elif request.method=="GET":
        # folder_path = r'samples\output'
        # file_type = r'*png'
        # files = glob.glob(folder_path + file_type)
        # max_file = max(files, key=os.path.getctime)

        # print(max_file)
        fname=get_latest_file('samples\output','*png')
        print(fname)
        path=f'samples\output\{fname}'
        out=demo.ocr(path)
        print(out)
        return out


if __name__ == "__main__":
    app.run(debug = "True",port=8080)