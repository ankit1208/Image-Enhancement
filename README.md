# Image-Enhancement
Image deblurring to achieve super resolution

### For installing, follow these intructions
```bash
$ conda create -n pytorch1 python=3.7

$ conda activate pytorch1

$ pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

$ pip install matplotlib scikit-image opencv-python yacs joblib natsort h5py tqdm google-cloud-vision flask
```

### Install warmup scheduler

```bash
$ cd pytorch-gradual-warmup-lr

$ python setup.py install

$ cd ..
```

### Activate environment
```bash
For Unix: $ conda activate pytorch1
For Windows: $ source activate pytorch1
```

### Run server
```bash
$ python app.py
```

### Run frontend
```bash
$ cd frontend
$ npm install
$ npm run dev
```