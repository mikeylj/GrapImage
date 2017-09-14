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


def getCurrExecNum( command ):
    output = 'ps aux|grep "python %s"|grep -v grep|wc -l' % command
    (status, output) = commands.getstatusoutput(output)
    return output
def ExecMul(count, commands):
    exec_command = 'Baidu_Filter_Del_ImgFile.py'
    for row in commands:
        # print row
        # sid = row[0]
        # url = row[1]
        # sclass= row[2].strip()
        # sub_class = row[3].strip()
        #
        #
        path = row
        sclass = path.split("/")[-2]
        s = 'python %s "%s" "%s" >> /tmp/ylj.log &' % (exec_command, sclass, path)
        print s
        os.system(s)
        # print getCurrExecNum(exec_command)
        while (int(getCurrExecNum(exec_command)) > count):
            print "Current Proc:" + getCurrExecNum(exec_command)
            sleep(1)

ImageFiles = getClasses(pathName)


ExecMul(10, ImageFiles)