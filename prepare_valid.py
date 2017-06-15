# -*- coding: utf-8 -*-
import pandas as pd
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')
import numpy as np
# import jieba
import codecs
import re
import shutil
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
import random

datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')


#读取目录,得到文件名
def load_file_names(dir):
    nums = 6000
    fileDict = {}
    # print dir
    for dir_path, dir_names, file_names in os.walk(dir):
        # print file_names
        # files = []
        if '.DS_Store' in file_names:
            file_names.remove('.DS_Store')
            p = os.path.join(dir_path, '.DS_Store')
            os.remove(p)
            print p

        # print type(file_names)
        # os._exit(0)
        fileNums = len(file_names)

        print dir_path, fileNums

        # if fileNums  > 10:
        #     for i in range(nums):
        #         if i >= fileNums:
        #             if file_names[i % fileNums] == '.DS_Store':
        #                 continue
        #             #复制文件
        #             from_url = dir_path + '/' + file_names[i % fileNums]
        #             print from_url
        #             img = load_img(from_url)  # this is a PIL image
        #             x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
        #             x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)
        #             for batch in datagen.flow(x, batch_size=1,
        #                                       save_to_dir=dir_path, save_prefix='c_' +  str(random.randint(111111,999999)), save_format='jpeg'):
        #                 break  # otherwise the generator would loop indefinitely
        #
        #     print dir_path



        # for file_name in sorted(file_names):
        #     name = dir_path.split('/')[3]
        #     url = dir_path + '/' + file_name
        #     print name, '==========>', url


    #         # files.append(url)
    #
    #         # print url
    #         # print name, '=========>', file_name
    #
    #
    #
    #         # print "Value : %s" % fileDict.has_key('Age')
    #         if not fileDict.has_key(name):
    #             fileDict[name] = [url]
    #         else:
    #             fileDict[name].append(url)
    #
    # return  fileDict
    # return file_urls, file_names

pathName = '/home/ylj/tag_sys/PIC_DATA/train'


dict = load_file_names(pathName)
# for key in dict:
#     print key
    # for i in range(1600):
    #     file = dict[key][i % len(dict[key])]


        # print dict[key][i % len(dict[key])]
    # for file in dict[key]:
    #     print file
    # print key
    # print len(dict[key])








# print dict

# # dict = [ v for v in sorted(dict.values())]
# # dict= sorted(fileDict.iteritems(), key=lambda d:d[1]['val'], reverse = True)
# dict = sorted(dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
#
# # print dict
# num = 0
# for key in dict:
#     for i in range(1600):
#
#
#
#
#
#
#
#     if key[1] > 120:
#         num  = num +1
#         print key[0], '===>', key[1]
#         formDir = '../ai_pic/%s' % key[0]
#         toDir = './data/train/%s' % key[0]
#         if not os.path.exists(toDir):
#             os.makedirs(toDir)
#         valDir = './data/valid/%s' % key[0]
#         if not os.path.exists(valDir):
#             os.makedirs(valDir)
#
#         train_num = key[1] * 0.8
#         i = 1
#         for dir_path, dir_names, file_names in os.walk(formDir):
#             for file_name in sorted(file_names):
#                 from_file = formDir + '/' + file_name
#                 to_file = toDir + '/' + file_name
#                 val_file = valDir + '/' + file_name
#                 if not "DS_Store" in from_file:
#                     if i < train_num :
#                         shutil.copy(from_file, to_file)
#                     else:
#                         shutil.copy(from_file, val_file)
#                     i = i + 1
# print num