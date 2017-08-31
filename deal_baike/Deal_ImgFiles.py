#coding: utf-8

import commands
# from mysql import Mysql
from time import sleep, time
import os

# #从数据库中取出总数
# def getTableTotal(tablename):
#     sql = 'select count(1) from %s where isdel=0'%tablename;
#     db = Mysql()
#     query = db.queryDataBySql(sql)
#     return query
#
# #从数据库中取出一页
# def getPage(tablename, page = 1, pagesize = 10):
#     if page < 1 :
#         page = 1
#     offset  = (page - 1) * pagesize
#     end     = offset + pagesize
#     sql = 'select * from %s where isdel = 0 limit %s, %s' % (tablename, offset, end)
#     db = Mysql()
#     query = db.queryDataBySql(sql)
#     return query

#取得当前正在执行的命令数量
def getCurrExecNum( command ):
    output = 'ps aux|grep "python %s"|grep -v grep|wc -l' % command
    (status, output) = commands.getstatusoutput(output)
    return output
def ExecMul(count, commands):
    exec_command = 'Deal_ImgFile.py'
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
        # os.system(s)
        # # print getCurrExecNum(exec_command)
        # while (int(getCurrExecNum(exec_command)) > count):
        #     print "Current Proc:" + getCurrExecNum(exec_command)
        #     sleep(1)





# newBaiDs    = getPage('new_bing_flower', 1, 10000)
#
# ExecMul(10, newBaiDs)
root_dir = "/home/ylj/tag_sys/GrapImage/baike_fl/download/"
ImageFiles = []
for dirname in os.listdir(root_dir):
    flow_name_dir = root_dir + dirname + "/"
    for pic_name in os.listdir(flow_name_dir):
        pic_full_name = flow_name_dir+pic_name
        ImageFiles.append(pic_full_name)
        # print pic_full_name



ExecMul(10, ImageFiles)