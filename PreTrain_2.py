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

train_num   = 512
test_num    = 128
pathName = '/home/ylj/tag_sys/GrapImage/baike_fl/download_deal/'
disPathName = '/home/ylj/tag_sys/GrapImage/baike_train'

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
    if(fileNums > 640):
        print dir_path, fileNums
        # 删除类型为None文件
        for i in range(fileNums):
            from_file = os.path.join(dir_path, file_names[i])
            pic_type = imghdr.what(from_file)
            if  pic_type == 'jpeg':
                print from_file, pic_type
            elif pic_type == 'gif':
                # s = from_file.split('.')
                # os.rename(from_file, s[-2] + ".gif")
                # print s[-2] + ".gif", pic_type
                # print from_file, pic_type
                os.unlink(from_file)
            elif pic_type == 'png':
                # s = from_file.split('.')
                # os.rename(from_file, s[-2] + ".png")
                # print s[-2] + ".png", pic_type
                # print from_file, pic_type
                os.unlink(from_file)
            else:
                os.unlink(from_file)
                # print from_file, pic_type

            image = Image.open(from_file)
            # try:
            #     image = Image.open(from_file)
            #     # print image
            #     print from_file
            # except IOError, e:
            #     print e
            #
            # except Exception, e:
            #     print from_file
            #     os.unlink(from_file)
            #     # print e


        # #测试训练集
        # for i in range(fileNums):
        #     p = dir_path.split('/')[-1]
        #     #复制进入训练集
        #     if i < train_num:
        #         d_p = os.path.join(train_dir, p)
        #         if not os.path.exists(d_p):
        #             os.makedirs(d_p)
        #     elif i < train_num + test_num:
        #         d_p = os.path.join(validation_dir, p )
        #         if not os.path.exists(d_p):
        #             os.makedirs(d_p)
        #     else:
        #         d_p = os.path.join(test_dir, p)
        #         if not os.path.exists(d_p):
        #             os.makedirs(d_p)
        #     # print i, d_p
        #     from_file = os.path.join(dir_path, file_names[i])
        #     if(getsize(from_file) < 100):
        #         print from_file, getsize(from_file)
        #     to_file =  os.path.join(d_p, file_names[i])
        #     print from_file, to_file
        #
        #     # shutil.copy(from_file, to_file)
    # #
