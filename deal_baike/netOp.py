# -*- coding:utf-8 -*-

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import json
import urllib
# import socket
import re
import os
from socket import *

setdefaulttimeout(30.0)
register_openers()

class NETOP:
    def getName(self, html):
        reg = r'对该图片的最佳猜测.*?>(.*?)</a>'  # 正则
        # 括号表示分组，将括号的内容捕获到分组当中
        #  这个括号也就可以匹配网页中图片的url了
        imgre = re.compile(reg, re.S)
        # print imgre
        imglist = re.findall(imgre, html)
        l = len(imglist)
        # print l
        return imglist

    def getNamePro(self, html):
        reg = r'<li class="checked" update="yes">(.*?)</li>'  # 正则
        # 括号表示分组，将括号的内容捕获到分组当中
        #  这个括号也就可以匹配网页中图片的url了
        imgre = re.compile(reg, re.S)
        # print imgre
        imglist = re.findall(imgre, html)
        l = len(imglist)
        # print l
        return imglist

    def otherPro(self, html):
        reg = r'图中植物可能是 <(.*?)"shituplant-cont">'  # 正则
        # 括号表示分组，将括号的内容捕获到分组当中
        #  这个括号也就可以匹配网页中图片的url了
        imgre = re.compile(reg, re.S)
        # print imgre
        imglist = re.findall(imgre, html)
        l = len(imglist)
        # print l
        return imglist

    def checkName(self, name, reg):
        # reg = r' + pred + '  # 正则
        imgre = re.compile(name, re.S)
        # print imgre
        imglist = re.findall(imgre, reg)
        if len(imglist) > 0:
            return True
        else:
            return False

    def getHtml(self, url):
        try:
            page = urllib.urlopen(url)
            html = page.read()
            return html
        except timeout:
            print "time out"
            return ''
        except error, e:
            print "error out"
            return ''

    def getImageNameFromBaidu(self,imgUrl):
        # 开始对文件 "DSC0001.jpg" 的 multiart/form-data 编码
        # "image1" 是参数的名字，一般通过 HTML 中的 <input> 标签的 name 参数设置

        # headers 包含必须的 Content-Type 和 Content-Length
        # datagen 是一个生成器对象，返回编码过后的参数
        datagen, headers = multipart_encode({"file": open(imgUrl, "rb")})

        # 创建请求对象
        request = urllib2.Request("http://image.baidu.com/pcdutu/a_upload?fr=html5&target=pcSearchImage&needJson=true",
                                  datagen, headers)
        # 实际执行请求并取得返回
        ret = urllib2.urlopen(request).read()

        # print type(ret)
        retJson = json.loads(ret)
        if retJson['errno'] == 0:
            # print type(retJson)
            queryUrl = 'http://image.baidu.com/pcdutu?queryImageUrl=' + retJson['url'] + '&querySign=' + retJson[
                'querySign'] + '&fm=result&uptype=upload_pc&result=result_camera'
            print queryUrl
            html = self.getHtml(queryUrl)
            strNames = self.getName(html)
            strName = '';
            if len(strNames) > 0:
                for str in strNames:
                    strName = str
            else:
                strNames = self.getNamePro(html)
                if len(strNames) > 0:
                    for str in strNames:
                        strName = str
                else:
                    strNames = self.otherPro(html)
                    if len(strNames) > 0:
                        for str in strNames:
                            strName = str
            return strName
        else:
            return ''
