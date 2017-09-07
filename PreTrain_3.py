# -*- coding: utf-8 -*-
nums = 100
import codecs
import os
import shutil
from os.path import join, getsize
import imghdr
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

train_num   = 960
test_num    = 160
pathName = '/home/ylj/tag_sys/GrapImage/new_data/'
disPathName = '/home/ylj/tag_sys/GrapImage/new_data_train/'

# train_dir = os.path.join(disPathName, 'train')
# validation_dir = os.path.join(disPathName, 'validation')
# test_dir = os.path.join(disPathName, 'test')
# if not os.path.exists(train_dir):
#     os.makedirs(train_dir)
#
# if not os.path.exists(validation_dir):
#     os.makedirs(validation_dir)
#
# if not os.path.exists(test_dir):
#     os.makedirs(test_dir)

for dir_path, dir_names, file_names in os.walk(pathName):
    fileNums = len(file_names)


    if fileNums > (train_num + test_num):
        print dir_path, fileNums
