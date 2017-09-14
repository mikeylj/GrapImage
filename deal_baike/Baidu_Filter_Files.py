#coding: utf-8

import commands
from mysql import Mysql
from time import sleep, time
import os

#读取目录下的文件
# pathName = '/Volumes/天天/TRAIN_NOW'
pathName = '/home/ylj/tag_sys/GrapImage/TRAINS_bak/'
def getClasses(path):
    image_paths = []
    for dir_path, dir_names, file_names in os.walk(path):
        if '.DS_Store' in file_names:
            file_names.remove('.DS_Store')
            p = os.path.join(dir_path, '.DS_Store')
            os.remove(p)
            print p
        if len(file_names) > 2:
            for f in file_names:
                # print dir_path + '/' + f
                image_paths.append(dir_path + '/' + f)
        # fileNums = len(file_names)
        # print dir_path, fileNums

    return image_paths;

images = getClasses(pathName)
print images