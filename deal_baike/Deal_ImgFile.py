#coding: utf-8
import sys
import os
import hashlib
from netOp import NETOP
# from mysql import Mysql
from pathlib import Path
import shutil

root_dir = "/home/ylj/tag_sys/GrapImage/baike_fl/download_deal/"

if __name__ == '__main__':
    sclass = sys.argv[1]
    path = sys.argv[2]

    #判断目录是否存在
    download_dir = Path(root_dir + sclass)
    if not download_dir.exists():
        download_dir.mkdir(parents=True)


    m2 = hashlib.md5()
    m2.update(path)
    filename = m2.hexdigest();
    filename = '%s%s/%s' % (root_dir, sclass, filename + ".jpg")


    #文件存在，判断文件是否与名字相同
    op = NETOP()
    strName = op.getImageNameFromBaidu(path)
    name = sclass

    # print strName, name, filename

    print path, filename, strName, name
    if op.checkName(name, strName):
        shutil.copy(path, filename)


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
