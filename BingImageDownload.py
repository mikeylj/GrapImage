#coding: utf-8
from bs4 import BeautifulSoup
import socket
from socket import error as SocketError
import urllib
import urllib2
import os
import re
import uuid
import Queue
import threading
import time
import multiprocessing

socket.setdefaulttimeout(10.0)

extensions = [
    '',
    '背景',
    '背景图片',
    '背景素材',
    '图片',
    '唯美',
    '壁纸',
    '唯美壁纸图片',
    '高清图片',
    '高清',
    '图片大全大图',
    '大全大图',
    '大全',
    '大图'
]

def downLoad(urls, path, keyword):
    if not urls:
        return 0
    for url in urls:
        # print("Downloading:", url)
        try:
            # 伪装浏览器头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
            req = urllib2.Request(url)
            req.add_header("User-Agent", headers)
            req.add_header("Host", "tse4.mm.bing.net")
            req.add_header("GET", url)
            if not os.path.exists('%s' % path):
                os.makedirs('%s' % path)
            newPath = '%s/%s' % (path, keyword)

            content = urllib2.urlopen(req).read()
            filename = os.path.join(newPath, uuid.uuid1().__str__()  + ".jpg")
            # urllib.urlretrieve(url, filename)  # 直接将远程数据下载到本地。
            with open(filename, 'wb') as f:
                f.write(content)

            # user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            # headers = {'User-Agent': user_agent}
            # # data = urllib.urlencode(values)
            # # req = urllib2.Request(url, headers)
            # # response = urllib2.urlopen(req)
            # # the_page = response.read()
            # conn = httplib.HTTPConnection('image.baidu.com')
            # conn.request('GET', url, headers=headers)
            # r = conn.getresponse()


        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                error_status = e.code
                print e
                print error_status, "未下载成功：", url
                continue
            elif hasattr(e, 'reason'):
                print "downLoad 1 time out", url
                continue
        except socket.timeout:
            print "downLoad 2 time out", url
            continue
        except SocketError as e:
            print "SocketError", url
            continue

def getHtml(url):
    try:
        page = urllib.urlopen(url)
        html = page.read()
        return html
    except socket.timeout:
        print "getHtml time out", url
        return ''



def getPageImageUrl(page, keyword):
    pn = page * 35
    url = 'http://cn.bing.com/images/async?q=%s&first=%s&count=35&relp=35&lostate=r&mmasync=1&dgState=x*152_y*1187_h*190_c*1_i*141_r*27&IG=F7F9D77717C14FBBB80ACC9F0099C872&SFX=5&iid=images.5651' % (
    keyword, pn)
    print url
    imglist = []
    try:
        html_data = getHtml(url)
        # print html_data
        soup = BeautifulSoup(html_data, "lxml")
        allImages = soup.findAll(attrs={'class':"mimg"})
        # print allImages
        for i, image in enumerate(allImages):
            imglist.append(image.attrs['src'])
            # print i, image.attrs['src']
            # print i, image.attrs['alt']
            # downLoad(image.attrs['src'], path, keyword)
    except ValueError, e:
        print 'getPageImageUrl ValueError', e

    return imglist


class WorkManager(object):
    def __init__(self, thread_num=2, imagelist_utf8 = [], Savepath  = '', keyword   = ''):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.__init_work_queue(imagelist_utf8, Savepath, keyword)
        self.__init_thread_pool(thread_num)

    """
        初始化线程
    """

    def __init_thread_pool(self, thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))

    """
        初始化工作队列
    """

    def __init_work_queue(self, imagelist_utf8, Savepath, keyword):
        # time.sleep(3)
        newPath = '%s/%s/%s' % (Savepath, keyword, 'files.txt')
        with open(newPath, "w") as f:
            values = "\n".join(imagelist_utf8)
            f.writelines(values)
        for i in (imagelist_utf8):
            self.add_job(do_job, i, Savepath, keyword)

    """
        添加一项工作入队
    """

    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))  # 任务入队，Queue内部实现了同步机制

    """
        等待所有线程运行完毕
    """

    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive(): item.join()


class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        # 死循环，从而让创建的线程在一定条件下关闭退出
        while True:
            try:
                do, args = self.work_queue.get(block=False)  # 任务异步出队，Queue内部实现了同步机制
                do(args)
                self.work_queue.task_done()  # 通知系统任务完成
            except:
                break


#具体要做的任务
def do_job(args):
    # time.sleep(0.1)#模拟处理时间
    # print threading.current_thread()
    # print args[0]
    # print args[1]
    # print args[2]
    downLoad([args[0]], args[1], args[2])

def getArrDownloadImages(pathName, keyword):
    page = 0
    Savepath = '../flowers_data_bing/' + pathName
    if(not os.path.exists(Savepath)):
        os.makedirs(Savepath)
    if (not os.path.exists(Savepath + '/' + keyword)):
        os.makedirs(Savepath + '/' + keyword)
    elif file_count(Savepath + '/' + keyword) > 100:
        print keyword, '已抓取'
        return [], Savepath, keyword
    else:
        pass

    imagelist_utf8 = [];
    while page < 40:
        imagelist = getPageImageUrl(page, keyword)
        for image in imagelist:
            imagelist_utf8.append(image.encode("utf-8"))
            print page, '====>', image
        page = page + 1
        print page

    s = set(imagelist_utf8)
    imagelist_utf8 = [i for i in s]
    print '===================================='
    #downLoad(imagelist_utf8, Savepath, keyword)
    return imagelist_utf8, Savepath, keyword


def oneDoProcessor(pathName, keyword):
    imagelist_utf8, Savepath, keyword = getArrDownloadImages(pathName, keyword)
    work_manager = WorkManager(10, imagelist_utf8, Savepath, keyword)  # 或者work_manager =  WorkManager(10000, 20)
    work_manager.wait_allcomplete()

# getPageImageUrl(0, '倒挂金钟图片')
# ImageDownload('倒挂金钟图片', '倒挂金钟图片')
# 如果你用了迭代的话是不需要知道是不是最后一个文件的，因为所有的文件都会统计到。
# 给你一段参考的代码：
def file_count(dirname,filter_types=[]):
     '''Count the files in a directory includes its subfolder's files
        You can set the filter types to count specific types of file'''
     count=0
     filter_is_on=False
     if filter_types!=[]: filter_is_on=True
     for item in os.listdir(dirname):
         abs_item=os.path.join(dirname,item)
         #print item
         if os.path.isdir(abs_item):
             #Iteration for dir
             count+=file_count(abs_item,filter_types)
         elif os.path.isfile(abs_item):
             if filter_is_on:
                 #Get file's extension name
                 extname=os.path.splitext(abs_item)[1]
                 if extname in filter_types:
                     count+=1
             else:
                 count+=1
     return count
if __name__ == '__main__':
    start = time.time()
    pool = multiprocessing.Pool(processes=4)
    result = []

    file_path = os.path.split(os.path.realpath(__file__))[0]
    filename = '2.txt'
    filename = os.path.join(file_path, filename)
    #读得花文件名
    with open(filename, 'r') as f:
        lines = f.readlines()
        if not lines:
            print '文件为空'
        else:
            for line in lines:
                for ext in extensions:
                    tmpLine = line.replace('\n', '')
                    words = line.replace('\n', '') + ext
                    result.append(pool.apply_async(oneDoProcessor, (tmpLine, words)))
                    if ext == '' and '花' not in tmpLine:
                        result.append(pool.apply_async(oneDoProcessor, (tmpLine, words + '花')))
                    # ImageDownload(tmpLine, words)

    # for i in xrange(3):
    #     msg = "hello %d" % (i)
    #     result.append(pool.apply_async(oneDoProcessor, ('倒挂金钟图片', '倒挂金钟图片')))

    pool.close()
    pool.join()
    for res in result:
        print ":::", res.get()
    print "Sub-process(es) done."

    end = time.time()
    print "cost all time: %s" % (end-start)