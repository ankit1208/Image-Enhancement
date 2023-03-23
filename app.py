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
gc.collect()
torch.cuda.empty_cache()
#torch.cuda.empty_cache()
#torch.cuda.memory_summary(device=None, abbreviated=False)
parser = argparse.ArgumentParser(description='Demo MPRNet')
parser.add_argument('--input_dir', default='./samples/input/', type=str, help='Input images')
parser.add_argument('--result_dir', default='./samples/output/', type=str, help='Directory for results')
parser.add_argument('--task', required=True, type=str, help='Task to run', choices=['Deblurring'])#, 'Denoising', 'Deraining'])

args = parser.parse_args()


import matplotlib.pyplot as plt
import numpy as np
import urllib.request
import pickle
from utils import load_image
#from helper import standardize, evaluate, plot_attention
#importing all the helper fxn from helper.py which we will create later
import requests
from streamlit_lottie import st_lottie
import streamlit as st
import hydralit_components as hc
import time
import seaborn as sns


sns.set_theme(style="darkgrid")


sns.set()



 


def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
        
lottie_load = load_lottieurl('https://assets6.lottiefiles.com/packages/lf20_nncar5qq.json')

with st.spinner('Loading...'):
    #st_lottie(lottie_load, speed=1, height=500, key="initial")
    #time.sleep(7)

    with hc.HyLoader('',hc.Loaders.pulse_bars,):
    #time.sleep(7)
        time.sleep(7)

# a dedicated single loader


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

task    = args.task
inp_dir = args.input_dir
out_dir = args.result_dir


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

def save_uploaded_file(uploaded_file):

    try:

        with open(os.path.join('static/images',uploaded_file.name),'wb') as f:

            f.write(uploaded_file.getbuffer())

        return 1    

    except:

        return 0

def app():
    st.title('Automatic Image Enhancement')
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
        
    #image_path =''
    lottie_att = load_lottieurl('https://assets10.lottiefiles.com/private_files/lf30_jynxrd4m.json')
    st_lottie(lottie_att, speed=1, height=380)
    st.subheader("Increase resolution of images automatically!")
    st.markdown("Hey there! Welcome to Automatic Image Enhancemen App. This app uses (and never keeps or stores!) the image you want to analyze and produce a high resolution image of it.")
    
    st.write("__________________________________________________________________________________")
    # Radio Buttons
    st.markdown(" **To begin, let's select the type of fetching you want to conduct. You can either fetch an image via url or search upload an image from your local device 👇.** ")
    st.write("")
    stauses = st.radio('Select the mode of fetching',("Fetch image via url","Upload image from local device"))
    if stauses == 'Fetch image via url':
        st.success("Enter Url")
        image_url = st.text_input("Copy paste URL of image")
        if image_url is not "":
            urllib.request.urlretrieve(image_url, "temp.png")
            st.image(image_url)
 
                    
            st.subheader('5 Predicted Captions for the above image :-')
            st.write("__________________________________________________________________________________")

 
        #print(image_path)
    elif stauses == 'Upload image from local device':
        st.success("Upload Image")
        st_lottie(load_lottieurl('https://assets2.lottiefiles.com/packages/lf20_2oranrew.json'), speed=1, height=280)
        uploaded_file = st.file_uploader("Upload Image")
        # text over upload button "Upload Image"

        if uploaded_file is not None:

            if save_uploaded_file(uploaded_file): 

                # display the image

                display_image = Image.open(uploaded_file)

                st.image(display_image)

                image_path = os.path.join('static/images',uploaded_file.name)

 

                st.set_option('deprecation.showPyplotGlobalUse', False)
                        
                st.subheader('5 Predicted Captions for the above image :-')
                st.write("__________________________________________________________________________________")
                        

                os.remove('static/images/'+uploaded_file.name) # deleting uploaded saved picture after prediction
                #print(image_path)
    else:
        st.warning("Choose an option")

    st.markdown('***')
    st.markdown("Thanks for going with us. Cheers!")
    

if __name__ == "__main__":
	app()