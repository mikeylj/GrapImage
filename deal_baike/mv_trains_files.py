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

train_num   = 800
test_num    = 160
# pathName = '/home/ylj/tag_sys/GrapImage/TRAINS_bak'
pathName = '/home/ylj/tag_sys/GrapImage/TRAINS_bak';
fromPathName = '/home/ylj/tag_sys/GrapImage/baike_fl/download_deal/';

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

# for dir_path, dir_names, file_names in os.walk(pathName):
#     print dir_names
    # fileNums = len(file_names)
    #
    #
    # if fileNums > (train_num + test_num):
    #     print dir_path, fileNums


#取得文件夹名
# print os.listdir(pathName)
for dirname in os.listdir(pathName):
    path = '%s%s'%(fromPathName, dirname)
    # print path
    if not os.path.exists(path):
        continue
    else:
        print path
        # for dir_path, dir_names, file_names in os.walk(path):
        #     fileNums = len(file_names)
        #     # print fileNums
        #     for file in file_names:
        #         file_p = '%s/%s'%(dir_path, file)
        #         des_p = '%s%s/%s' % (pathName, dirname, file)
        #         print file_p
        #         print des_p
        #         os._exit(0)
        #         # shutil.copy(file_p, des_p)



