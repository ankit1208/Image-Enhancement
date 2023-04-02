# from flask import Flask
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms.functional as TF
from PIL import Image
import os
from runpy import run_path
from skimage import img_as_ubyte
from collections import OrderedDict
from natsort import natsorted
from glob import glob
import cv2
import argparse
import gc
import os
import io
from google.cloud import vision
from google.cloud.vision_v1 import types
gc.collect()
torch.cuda.empty_cache()

# app = Flask(__name__)

#torch.cuda.empty_cache()
#torch.cuda.memory_summary(device=None, abbreviated=False)
# parser = argparse.ArgumentParser(description='Demo MPRNet')
# parser.add_argument('--input_dir', default='./samples/input/', type=str, help='Input images')
# parser.add_argument('--result_dir', default='./samples/output/', type=str, help='Directory for results')
# parser.add_argument('--task', required=True, type=str, help='Task to run', choices=['Deblurring'])#, 'Denoising', 'Deraining'])

# args = parser.parse_args()
def demo():
    def save_img(filepath, img):
        cv2.imwrite(filepath,cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    def load_checkpoint(model, weights):
        checkpoint = torch.load(weights)
        try:
            model.load_state_dict(checkpoint["state_dict"])
        except:
            state_dict = checkpoint["state_dict"]
            new_state_dict = OrderedDict()
            for k, v in state_dict.items():
                name = k[7:] # remove `module.`
                new_state_dict[name] = v
            model.load_state_dict(new_state_dict)

    task    = 'Deblurring'
    inp_dir ='./samples/input/'
    out_dir = './samples/output/'

    os.makedirs(out_dir, exist_ok=True)

    files = natsorted(glob(os.path.join(inp_dir, '*.jpg'))
                    + glob(os.path.join(inp_dir, '*.JPG'))
                    + glob(os.path.join(inp_dir, '*.png'))
                    + glob(os.path.join(inp_dir, '*.PNG')))

    if len(files) == 0:
        raise Exception(f"No files found at {inp_dir}")

    # Load corresponding model architecture and weights
    load_file = run_path(os.path.join(task, "MPRNet.py"))
    model = load_file['MPRNet']()
    model.cuda()

    weights = os.path.join(task, "pretrained_models", "model_"+task.lower()+".pth")
    load_checkpoint(model, weights)
    model.eval()

    img_multiple_of = 8

    for file_ in files:
        img = Image.open(file_).convert('RGB')
        input_ = TF.to_tensor(img).unsqueeze(0).cuda()

        # Pad the input if not_multiple_of 8
        h,w = input_.shape[2], input_.shape[3]
        H,W = ((h+img_multiple_of)//img_multiple_of)*img_multiple_of, ((w+img_multiple_of)//img_multiple_of)*img_multiple_of
        padh = H-h if h%img_multiple_of!=0 else 0
        padw = W-w if w%img_multiple_of!=0 else 0
        input_ = F.pad(input_, (0,padw,0,padh), 'reflect')

        with torch.no_grad():
            model.eval()
            restored = model(input_)
        restored = restored[0]
        restored = torch.clamp(restored, 0, 1)

        # Unpad the output
        restored = restored[:,:,:h,:w]

        restored = restored.permute(0, 2, 3, 1).cpu().detach().numpy()
        restored = img_as_ubyte(restored[0])

        f = os.path.splitext(os.path.split(file_)[-1])[0]
        save_img((os.path.join(out_dir, f+'.png')), restored)

    print(f"Files saved at {out_dir}")

def ocr(path):
    #the JSON file you downloaded in step 5 above
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'high-theme-381806-e676f023df9a.json'

    # Instantiates a client
    client = vision.ImageAnnotatorClient()


    # # set this thumbnail as the url
    # image = types.Image()

    # image.source.image_uri = '/content/testimage.jpeg'
    # path='samples\output\img1.png'
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

        image = vision.Image(content=content)


    #### TEXT DETECTION ######

    response_text = client.text_detection(image=image)
    # print(response_text)
    # d = ""
    str = response_text.text_annotations[0].description
    return str



# if __name__ == "__main__":
#     app.run(debug = "True",port=3000)