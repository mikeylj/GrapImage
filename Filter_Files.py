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
    sql = 'select * from %s where isdel = 0 limit %s, %s' % (tablename, offset, end)
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


        path = 'new_baidu_flower/%s/%s' % (sclass, sub_class)
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




# getTableTotal('new_baidu_flower')
newBaiDs    = getPage('new_baidu_flower', 1, 1000)

ExecMul(500, newBaiDs)


# for row in result:
# print row[0], row[1]
# download_dir = setup_download_dir('%s/%s' % (row[0], row[1]))