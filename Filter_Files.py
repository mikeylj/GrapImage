#coding: utf-8

import commands
from mysql import Mysql
from time import sleep, time
import os

#从数据库中取出总数
def getTableTotal(tablename):
    sql = 'select count(1) from %s where isdel=0'%tablename;
    db = Mysql()
    query = db.queryDataBySql(sql)
    return query

#从数据库中取出一页
def getPage(tablename, page = 1, pagesize = 10):
    if page < 1 :
        page = 1
    offset  = (page - 1) * pagesize
    end     = offset + pagesize
    sql = "select * from %s where isdel = 1 and class in ('杜鹃', '桂花', '荷花', '菊花', '康乃馨', '梅花', '玫瑰', '米兰花', '茉莉', '牡丹', '郁金香', '栀子花') limit %s, %s" % (tablename, offset, end)
    # sql = "select id,url, class, sub_class, source, isdel, intro  from %s where isdel = 1 and class in ('杜鹃花') limit %s, %s" % (tablename, offset, end)
    db = Mysql()
    query = db.queryDataBySql(sql)
    return query

#取得当前正在执行的命令数量
def getCurrExecNum( command ):
    output = 'ps aux|grep "python %s"|grep -v grep|wc -l' % command
    (status, output) = commands.getstatusoutput(output)
    return output
def ExecMul(count, commands):
    exec_command = 'Filter_file.py'
    for row in commands:
        sid = row[0]
        url = row[1]
        sclass= row[2].strip()
        sub_class = row[3].strip()


        path = '/home/ylj/tag_sys/GrapImage/new_bing_flower/%s/%s' % (sclass, sub_class)
        s = 'python %s "%s" "%s" "%s" >> /tmp/ylj.log &' % (exec_command, sid, url, path)
        print s
        os.system(s)
        # print getCurrExecNum(exec_command)
        while (int(getCurrExecNum(exec_command)) > count):
            print "Current Proc:" + getCurrExecNum(exec_command)
            sleep(1)




        # print sid, url, sclass, sub_class, path
    # for i in xrange(len(commands)):
    #
    #     print sid
    #
    #     print s


        # os.system()




# getTableTotal('new_bing_flower')
newBaiDs    = getPage('new_bing_flower', 1, 10000)

ExecMul(10, newBaiDs)


# for row in result:
# print row[0], row[1]
# download_dir = setup_download_dir('%s/%s' % (row[0], row[1]))