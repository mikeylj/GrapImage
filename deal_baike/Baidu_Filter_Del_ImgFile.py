#coding: utf-8
import sys
import os
import hashlib
from netOp import NETOP
# from mysql import Mysql
from pathlib import Path
import shutil

# root_dir = "/home/ylj/tag_sys/GrapImage/TRAINS_bak/"

if __name__ == '__main__':
    sclass = sys.argv[1]
    path = sys.argv[2]

    #文件存在，判断文件是否与名字相同
    op = NETOP()
    strName = op.getImageNameFromBaidu(path)

    # print strName, name, filename

    if not op.checkName(sclass, strName):
        print path, sclass, strName, "删除！"
        os.unlink(path)
        # shutil.copy(path, filename)


    #     os.unlink(filename)
    #     print "已删除文件：", filename, name, strName
    #     # sql = "update new_bing_flower set isdel=1 where id=%s" % sid
    #     db = Mysql()
    #     f_status_dict = {
    #         'isdel' : 1,
    #         'intro':strName
    #     }
    #     db.upDate('new_bing_flower', f_status_dict, " id='%s'" % sid)
    # else:
    #     print "正常：", filename, name, strName
    #     db = Mysql()
    #     f_status_dict = {
    #         'isdel': 2,
    #         'intro': strName
    #     }
    #     db.upDate('new_bing_flower', f_status_dict, " id='%s'" % sid)
