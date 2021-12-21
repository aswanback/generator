# Dataset Generation
This repo is the starting point of the PART dataset generation effort to make a synthetic dataset for training a ML model for the AUVSI SUAS competition. See purdueieee.org/partieee for more info. This repo is no longer updated.

## Target Generation
Run src/make_targets.py to generate targets by calling\

``` python3 src/make_targets.py <dst_dir> <num_each> <size> [--font_size F] [--clean] ```

This will make ```num_each``` of each target shape of width and height ```size``` with font size ```font_size```, saved to folder ```dst_dir```. If no font size specificed, defualts to half of ```size```. The ```--clean``` argument if passed will clear ```dst_dir``` before regenerating the dataset. 

Example: run ```python3 src/make_targets.py shapes 3 50 --clean``` to put 3 images size 50px of each shape into directory 'shapes'

## Full Image Generation
Run src/make_images.py to generate full images by calling\
```python3 src/make_images.py <dst_dir> <shape_dir> <bkgd_dir> <number> [--targets t] [--seamless] [--clean]```

This makes ```number``` images with ```targets``` number of targets in each frame (default 1) by sampling background images from ```bkgd_dir``` and targets from ```shape_dir```. Results saved to ```dst_dir```. With ```--seamless```, cv2.seamlessClone is used, otherwise standard PIL is used. Passing ```--clean``` will clear the ```dst_dir``` before running the script.

Example: run ```python3 src/make_images.py out shapes bkgds 4 --targets 3 --clean``` to put 4 images with 3 targets each into 'out'
