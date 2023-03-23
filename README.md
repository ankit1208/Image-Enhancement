# Image-Enhancement
Image deblurring to achieve super resolution

For installing, follow these intructions

`conda create -n pytorch1 python=3.7`
`conda activate pytorch1`
`conda install pytorch=1.1 torchvision=0.3 cudatoolkit=9.0 -c pytorch`
`pip install matplotlib scikit-image opencv-python yacs joblib natsort h5py tqdm`

Install warmup scheduler

`cd pytorch-gradual-warmup-lr`
`python setup.py install`
`cd ..`


* activate environment
`conda activate pytorch1`

*run demo`
`python demo.py --task Deblurring --input_dir ./samples/input/ --result_dir ./samples/output/`