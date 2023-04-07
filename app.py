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


def get_file_by_name(path, *paths, fileName):
    fullpath = os.path.join(path, *paths)
    files = glob.glob(fullpath)
    print(files)
    for file in files:
        _, filename = os.path.split(file)
        if filename.split(".")[0] == fileName:
            return filename
    return ""

# Define a route to handle the request
@app.route('/api/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        f = request.files['file']
        os.chdir('D:\\Github_Projects\\Image-Enhancement\\samples\\input')
        f.save(f.filename)
        os.chdir('D:\\Github_Projects\\Image-Enhancement')
        image = demo.demo(filename=f.filename)
        img = Image.fromarray(image)
        image_object = io.BytesIO()
        img.save(image_object, 'PNG')
        image_object.seek(0)
        return send_file(image_object, mimetype='image/PNG')
    elif request.method == "GET":
        fileName = request.args.get('fileName')
        fname = get_file_by_name('samples\output', '*png', fileName=fileName)
        path = f'samples\output\{fname}'
        out = demo.ocr(path)
        return {"text": out}


if __name__ == "__main__":
    app.run(debug="True", port=8080)
