# -*- coding: utf-8 -*-

import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Log():
    @staticmethod
    def cur_time(pre):
        return '[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " "+pre+"] "
    @staticmethod
    def info(msg, mtype = "info"):
        try:
            f = open("log.txt", "a")
            f.write(Log.cur_time(mtype) + msg.encode("utf-8") + "\n")
            f.close()
        except IOError, e:
            print '写入日志失败:', e
    @staticmethod
    def error(msg):
        try:
            Log.info(msg, "error")
        except IOError, e:
            print '写入日志失败:', e