# -*- coding: utf-8 -*-
nums = 6000
import codecs
import os
import shutil

train_num   = nums * 0.8
test_num    = nums * 0.2
pathName = '/Volumes/天天/PIC'
disPathName = '/Volumes/天天/PIC_DATA'

train_dir = os.path.join(disPathName, 'train')
validation_dir = os.path.join(disPathName, 'validation')

if not os.path.exists(train_dir):
    os.makedirs(train_dir)

if not os.path.exists(validation_dir):
    os.makedirs(validation_dir)

for dir_path, dir_names, file_names in os.walk(pathName):
    fileNums = len(file_names)
    if(fileNums > 10):
        #测试训练集
        for i in range(nums):
            p = dir_path.split('/')[-1]
            #复制进入训练集
            if i < train_num:
                d_p = os.path.join(train_dir, p)
                if not os.path.exists(d_p):
                    os.makedirs(d_p)
            else:
                d_p = os.path.join(validation_dir, p )
                if not os.path.exists(d_p):
                    os.makedirs(d_p)
            print i, d_p
            from_file = os.path.join(dir_path, file_names[i])
            to_file =  os.path.join(d_p, file_names[i])
            shutil.copy(from_file, to_file)

