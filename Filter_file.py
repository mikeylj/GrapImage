#coding: utf-8
import sys
import os
import hashlib
from netOp import NETOP
from mysql import Mysql

if __name__ == '__main__':
    sid = sys.argv[1]
    url = sys.argv[2]
    path = sys.argv[3]

    m2 = hashlib.md5()
    m2.update(url)
    filename = m2.hexdigest();
    filename    = download_path = '%s/%s' % (path, filename + ".jpg")
    #文件不存在，则下载
    if not os.path.isfile(filename):
        print '下载文件：python DownloadOnePic.py "%s" "%s"' % (url, path)
        os.system('python DownloadOnePic.py "%s" "%s" ' % (url, path))
    #文件存在，判断文件是否与名字相同
    op = NETOP()
    strName = op.getImageNameFromBaidu(filename)
    name = filename.split("/")[-3]

    # print strName, name, filename

    if not op.checkName(name, strName):
        # os.unlink(filename)
        print "已删除文件：", filename, name, strName
        # sql = "update new_baidu_flower set isdel=1 where id=%s" % sid
        db = Mysql()
        f_status_dict = {
            'isdel' : 1,
            'intro':strName
        }
        db.upDate('new_baidu_flower', f_status_dict, " id='%s'" % sid)
    else:
        print "正常：", filename, name, strName
        db = Mysql()
        f_status_dict = {
            'isdel': 2,
            'intro': strName
        }
        db.upDate('new_baidu_flower', f_status_dict, " id='%s'" % sid)
