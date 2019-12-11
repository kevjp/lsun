This repo is a cloned version of one found at https://github.com/fyu/lsun. The README contains information as provided by the original repo and is shown between the section within the marked lins

___

# LSUN

Please check [LSUN webpage](http://www.yf.io/p/lsun) for more information about the dataset.

## Data Release

All the images in one category are stored in one lmdb database
file. The value
 of each entry is the jpg binary data. We resize all the images so
 that the
  smaller dimension is 256 and compress the images in jpeg with
  quality 75.
  
### Citing LSUN

If you find LSUN dataset useful in your research, please consider citing:

    @article{yu15lsun,
        Author = {Yu, Fisher and Zhang, Yinda and Song, Shuran and Seff, Ari and Xiao, Jianxiong},
        Title = {LSUN: Construction of a Large-scale Image Dataset using Deep Learning with Humans in the Loop},
        Journal = {arXiv preprint arXiv:1506.03365},
        Year = {2015}
    }

### Download data
Please make sure you have cURL installed
```bash
# Download the whole latest data set
python3 download.py
# Download the whole latest data set to <data_dir>
python3 download.py -o <data_dir>
# Download data for bedroom
python3 download.py -c bedroom
# Download testing set
python3 download.py -c test
```

## Demo code

### Dependency

Install Python

Install Python dependency: numpy, lmdb, opencv

### Usage:

View the lmdb content

```bash
python3 data.py view <image db path>
```

Export the images to a folder

```bash
python3 data.py export <image db path> --out_dir <output directory>
```

### Example:

Export all the images in valuation sets in the current folder to a
"data"
subfolder.

```bash
python3 data.py export *_val_lmdb --out_dir data
```

## Submission

We expect one category prediction for each image in the testing
set. The name of each image is the key value in the LMDB
database. Each category has an index as listed in
[index list](https://github.com/fyu/lsun_toolkit/blob/master/category_indices.txt). The
submitted results on the testing set will be stored in a text file
with one line per image. In each line, there are two fields separated
by a whitespace. The first is the image key and the second is the
predicted category index. For example:

```
0001c44e5f5175a7e6358d207660f971d90abaf4 0
000319b73404935eec40ac49d1865ce197b3a553 1
00038e8b13a97577ada8a884702d607220ce6d15 2
00039ba1bf659c30e50b757280efd5eba6fc2fe1 3
...
```

The score for the submission is the percentage of correctly predicted
labels. In our evaluation, we will double check our ground truth
labels for the testing images and we may remove some images with
controversial labels in the final evaluation.

---

**The following changes have been made from the original code and are specific to this repo**

- Added in new function slice_lmdb() to data.py script. This function allows you to select a specific number of images from the lsun lmdb database. This function was generated so that I could scale down the number of images for training. The training exercise that this data was used for was to train the bedroom StyleGAN network obtained from NVIDIA labs repo (https://github.com/NVlabs/stylegan). A transfer training approach was used to train this framework on other room type images namely Living Room and Kitchen images as a proof of principle to determine whether this approach was effective at generating other room images. Training occurred on Google's colab environment and so training images needed to be saved on my personal Google drive. Consequently I only had sufficient space to store a proportion of the lsun data. The slice_lmdb() function takes 3 arguments:

   - the path to the original lsun image lmdb database
   - the path to the new lmdb image directory containing a sample of the original lmdb database
   - limit - the number of images to include in the new lmdb database
   ### usage
   The argument to call this function from data.py can be done using the arguments
   `python data.py slice --limit <number of images to slice out> --out_dir '/path/to/new/lmdb/database'` 
   
   Once the abridged lmdb database has been generated then the images can be downloaded from it by the command:
   `python3 data.py export <image db path> --out_dir <output directory>`
   
   

