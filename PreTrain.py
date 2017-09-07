# -*- coding: utf-8 -*-
nums = 100
import codecs
import os
import shutil
from os.path import join, getsize
import imghdr

train_num   = 1200
test_num    = 320
# pathName = '/home/ylj/tag_sys/GrapImage/baike_fl/download_deal/'
# disPathName = '/home/ylj/tag_sys/GrapImage/baike_train'

pathName = '/home/ylj/tag_sys/GrapImage/new_data/'
disPathName = '/home/ylj/tag_sys/GrapImage/new_data_train/'


train_dir = os.path.join(disPathName, 'train')
validation_dir = os.path.join(disPathName, 'validation')
test_dir = os.path.join(disPathName, 'test')
if not os.path.exists(train_dir):
    os.makedirs(train_dir)

if not os.path.exists(validation_dir):
    os.makedirs(validation_dir)

if not os.path.exists(test_dir):
    os.makedirs(test_dir)

for dir_path, dir_names, file_names in os.walk(pathName):
    fileNums = len(file_names)


    # if fileNums > 640:
    #     print dir_path, fileNums
    if(fileNums > (train_num + test_num)):
        # print dir_path, fileNums
        #删除类型为None文件
        # for i in range(fileNums):
        #     from_file = os.path.join(dir_path, file_names[i])
        #     pic_type = imghdr.what(from_file)
        #     if  pic_type == 'jpeg':
        #         pass
        #     elif pic_type == 'gif':
        #         pass
        #     elif pic_type == 'png':
        #         pass
        #     else:
        #         os.unlink(from_file)
        #         print from_file, pic_type


        #测试训练集
        for i in range(fileNums):
            p = dir_path.split('/')[-1]
            #复制进入训练集
            if i < train_num:
                d_p = os.path.join(train_dir, p)
                if not os.path.exists(d_p):
                    os.makedirs(d_p)
            elif i < train_num + test_num:
                d_p = os.path.join(validation_dir, p )
                if not os.path.exists(d_p):
                    os.makedirs(d_p)
            else:
                d_p = os.path.join(test_dir, p)
                if not os.path.exists(d_p):
                    os.makedirs(d_p)
            # print i, d_p
            from_file = os.path.join(dir_path, file_names[i])
            if(getsize(from_file) < 100):
                print from_file, getsize(from_file)
            to_file =  os.path.join(d_p, file_names[i])
            print from_file, to_file

            shutil.copy(from_file, to_file)
    # #
