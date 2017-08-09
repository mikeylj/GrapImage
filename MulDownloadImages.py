#coding: utf-8

import json
import logging
import os
from pathlib import Path
import urllib2
import urllib
import socket
from socket import error as SocketError
import uuid
import sys, threading
from time import sleep, time
import Queue
from threading import Thread
import multiprocessing
from mysql import Mysql
import math
import commands

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)

logger  = logging.getLogger(__name__)

socket.setdefaulttimeout(10.0)

def getHtml(url):
    try:
        page = urllib.urlopen(url)
        html = page.read()
        return html
    except socket.timeout:
        print 'ERROR:', "time out"
        return ''

def get_links(page, keyword):
    pn = page * 30
    url = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord+=&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&word=%s&z=&ic=0&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&step_word=%s&pn=%s&rn=30&gsm=5a&1493640402348=' % (
    keyword, keyword, pn)
    print url
    imglist = []
    try:
        json_data = getHtml(url)
        data = json.loads(json_data)
        datas =  data['data']
        for d in datas:
            try:
                imglist.append(d['thumbURL'])
                # print d['fromPageTitle']
            except Exception, e:
                print 'ERROR:', e
    except ValueError, e:
        print 'ERROR:', e
    return imglist


def download_link(directory, link):
    logger.info('Downloading %s', link)
    # download_path = directory / uuid.uuid1().__str__()  + ".jpg"
    download_path = '%s/%s' % (directory, uuid.uuid1().__str__() + ".jpg") #os.path.join(directory, uuid.uuid1().__str__() + ".jpg")
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

def setup_download_dir(keyword):
   download_dir = Path('new_baidu_flower/' + keyword)
   if not download_dir.exists():
       download_dir.mkdir(parents = True)
   return download_dir



def single_main(page, keyword):
    print str(threading.current_thread()) + ": " + str(page)
    download_dir = setup_download_dir(keyword)
    links = get_links(page, keyword)
    for link in links:
        download_link(download_dir, link)

def mul_thread_main(keyword):
    ts = time()
    nums = getNums(40)
    # Create a queue to communicate with the worker threads
    queue = Queue.Queue()
    # Create 4 worker threads
    # 创建四个工作线程
    for x in range(4):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        # 将daemon设置为True将会使主线程退出，即使worker都阻塞了
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue
    for num in nums:
        queue.put((num, keyword))
    # Causes the main thread to wait for the queue to finish processing all the tasks
    # 让主线程等待队列完成所有的任务
    queue.join()

def oneDoProcessor(page, keyword):
    single_main(page, keyword)
    return '%s%s%s' % (page, '===========>', keyword)



def getNums(N):
    return xrange(N)

class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            # 从队列中获取任务并扩展tuple
            page, keyword = self.queue.get()
            single_main(page, keyword)
            # print page, keyword
            # download_link(directory, link)
            self.queue.task_done()


#从数据库中取出所有class, sub_class
def getClassesFromDB():
    sql = 'select `class`, `sub_class` from new_baidu_flower group by `class`, `sub_class`'
    db = Mysql()
    query = db.queryDataBySql(sql)
    return query

#从数据库里取出总条数
def getTotalNum():
    sql = 'select count(*) from new_baidu_flower';
    db = Mysql()
    query = db.queryDataBySql(sql)
    return query

def getPageRows(page, pagesize):
    offset = page * pagesize
    sql = 'select * from new_baidu_flower limit %s, %s' %  (offset, pagesize);
    print sql;
    db = Mysql()
    query = db.queryDataBySql(sql)
    return query

def getCurrExecNum():
    (status, output) = commands.getstatusoutput('ps aux|grep "python DownloadOnePic.py"|grep -v grep|wc -l')
    return output


if __name__ == '__main__':
    ts = time()
    # result = getClassesFromDB()
    # for row in result:
    #     print row[0], row[1]
    #     download_dir = setup_download_dir('%s/%s' % (row[0], row[1]))
    pagesize = 100;
    print getTotalNum()[0][0]
    print getTotalNum()[0][0] * 1.0 / pagesize
    pages = int(math.ceil(getTotalNum()[0][0] * 1.0 / pagesize))
    print pages;

    print getCurrExecNum()
    os._exit(0)

    for i in xrange(pages):
        rows = getPageRows(i, pagesize)
        for row in rows:
            url = row[1]
            path = 'new_baidu_flower/%s/%s' % (row[2], row[3])
            # (status, output) = commands.getstatusoutput('python DownloadOnePic.py %s %s' % (url, path))

        print getCurrExecNum()
        while(getCurrExecNum() > 0):
            sleep(1)

        os._exit(0)




    # for i in getNums(40):
    #     single_main(i, '荷花')    #155s
    #多线程
    # mul_process_main('荷花')  #10s

    # #多进程 10s
    # nums = getNums(40)
    # pool = multiprocessing.Pool()
    # result = []
    # for k in nums:
    #     result.append(pool.apply_async(oneDoProcessor, (k, '荷花')))
    # pool.close()
    # pool.join()
    # for res in result:
    #     print ":::", res.get()
    # print "Sub-process(es) done."



    print "cost time is: {:.2f}s".format(time() - ts)
