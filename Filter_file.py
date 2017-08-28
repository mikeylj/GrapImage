#coding: utf-8
import sys
import os
import hashlib
from netOp import NETOP

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
        print 'python DownloadOnePic.py "%s" "%s"' % (url, path)
        os.system('python DownloadOnePic.py "%s" "%s" ' % (url, path))
    #文件存在，判断文件是否与名字相同
    strName = NETOP.getImageNameFromBaidu(filename)
    name = filename.split("/")[-2]

    print strName, name

    # if not NETOP.checkName(name, str):
    #     os.unlink(p)
    #     print "已删除文件：", p
    #
    # print sid, url, path, filename