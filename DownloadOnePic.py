#coding: utf-8

import sys
from pathlib import Path
import logging
import urllib2
import urllib
import hashlib
import socket
from socket import error as SocketError
import os


logger  = logging.getLogger(__name__)


def checkPath(path):
    if '' == path:
        return False
    download_dir = Path(path)
    if not download_dir.exists():
        download_dir.mkdir(parents=True)
    return download_dir
def checkFileExsist(filename):
    return os.path.isfile(filename)

def download_link(directory, link):
    checkPath(directory)
    # download_path = directory / uuid.uuid1().__str__()  + ".jpg"
    m2 = hashlib.md5()
    m2.update(link)
    filename = m2.hexdigest();
    download_path = '%s/%s' % (directory, filename + ".jpg") #os.path.join(directory, uuid.uuid1().__str__() + ".jpg")
    if checkFileExsist(download_path):
        logger.info('文件已存在 %s', link)
        return True

    logger.info('Downloading %s', link)

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
        req = urllib2.Request(link)
        req.add_header("User-Agent", headers)
        # req.add_header("Host", "img3.imgtn.bdimg.com")
        req.add_header("GET", link)

        content = urllib2.urlopen(req).read()
        # filename = os.path.join(newPath, uuid.uuid1().__str__() + ".jpg")
        # urllib.urlretrieve(url, filename)  # 直接将远程数据下载到本地。
        with open(download_path, 'wb') as f:
            f.write(content)
    except urllib2.URLError, e:
        if hasattr(e, 'code'):
            error_status = e.code
            print 'DOWNLOAD ERROR:', error_status, "未下载成功：", link
        elif hasattr(e, 'reason'):
            print 'DOWNLOAD ERROR:', "time out", link
    except socket.timeout:
        print 'DOWNLOAD ERROR:', "time out", link
    except SocketError as e:
        print 'DOWNLOAD ERROR:', "SocketError", link



if __name__ == '__main__':
    url = sys.argv[0]
    path = sys.argv[0]
    download_link(path, url)