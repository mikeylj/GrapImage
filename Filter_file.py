#coding: utf-8
import sys
import os
import hashlib

if __name__ == '__main__':
    sid = sys.argv[1]
    url = sys.argv[2]
    path = sys.argv[3]

    m2 = hashlib.md5()
    m2.update(url)
    filename = m2.hexdigest();
    filename    = download_path = '%s/%s' % (path, filename + ".jpg")
    if not os.path.isfile(filename):
        print 'python DownloadOnePic.py "%s" "%s"' % (url, path)
        os.system('python DownloadOnePic.py "%s" "%s" ' % (url, path))


    print sid, url, path, filename