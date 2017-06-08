#coding: utf-8
import os
import re
import urllib
import urllib2
import json
import requests
import httplib
import uuid
import socket
from socket import error as SocketError

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



# index = 1
# keyword = '油菜花'
# keywords    = ['油菜花', '油菜花背景', '油菜花背景素材', '油菜花图片', '油菜花 唯美', '油菜花 壁纸', '油菜花唯美壁纸图片'];

def getHtml(url):
    try:
        page = urllib.urlopen(url)
        html = page.read()
        return html
    except socket.timeout:
        print "time out"
        return ''

def getImg(html):
    reg = r'"objURL":"(.*?)"'  # 正则
    # 括号表示分组，将括号的内容捕获到分组当中
    #  这个括号也就可以匹配网页中图片的url了
    imgre = re.compile(reg)
    print imgre
    imglist = re.findall(imgre, html)
    l = len(imglist)
    print l
    return imglist

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
            req.add_header("Host", "img3.imgtn.bdimg.com")
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
                print error_status, "未下载成功：", url
                continue
            elif hasattr(e, 'reason'):
                print "time out", url
                continue
        except socket.timeout:
            print "time out"
            continue
        except SocketError as e:
            print "SocketError"
            continue


def nextPageUrl(page, keyword):
    pn = page * 30
    url = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord+=&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&word=%s&z=&ic=0&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&step_word=%s&pn=%s&rn=30&gsm=5a&1493640402348=' %(keyword, keyword, pn)
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
                print e
    except ValueError, e:
        print e
    return imglist

        # print d['thumbURL']
    # images = getImg(json_data)
    # print images

# html =getHtml("http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&s"
#                 "f=1&fmq=1484296421424_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&"
#                 "word=茉莉花&f=3&oq=xinyuanj&rsp=0")

# imagelist = getImg(html)
# print imagelist
# downLoad(getImg(html),Savepath)

def ImageDownload(pathName, keyword):
    page = 0
    Savepath = "/home/yulijun/tag_sys/flowers_data/" + pathName
    if(not os.path.exists(Savepath)):
        os.makedirs(Savepath)
    if (not os.path.exists(Savepath + '/' + keyword)):
        os.makedirs(Savepath + '/' + keyword)
    else:
        print keyword, '已抓取'
        return 0


    while page < 40:
        imagelist = nextPageUrl(page, keyword)
        imagelist_utf8 = [];
        for image in imagelist:
            imagelist_utf8.append(image.encode("utf-8"))
            print page, '====>', image

        print '===================================='
        downLoad(imagelist_utf8, Savepath, keyword)
        page = page + 1
        print page


# for w in keywords:
#     i = 0
#     keyword = w
#     Savepath = "./" + keyword
#     while i < 40:
#         imagelist = nextPageUrl(i)
#         imagelist_utf8 = [];
#         for image in imagelist:
#             imagelist_utf8.append(image.encode("utf-8"))
#         downLoad(imagelist_utf8, Savepath)
#         i = i +1
#         print i
# print imagelist_utf8

# print nextPageUrl(i)
# while True:
#     downLoad(nextPageUrl(i), Savepath)
#     i = i + 1

#


file_path   = os.path.split(os.path.realpath(__file__))[0]
filename    = '2.txt'
filename = os.path.join(file_path, filename)

with open(filename, 'r') as f:
    lines = f.readlines()
    if not lines:
        print '文件为空'
    else:
        for line in lines:
            for ext in extensions:
                tmpLine = line.replace('\n', '')
                words = line.replace('\n', '') + ext
                ImageDownload(tmpLine, words)

                # print line.replace('\n', '') + ext




