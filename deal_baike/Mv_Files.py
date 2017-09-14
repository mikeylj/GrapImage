#coding: utf-8

from mysql import Mysql
import hashlib
import shutil
import os
from pathlib import Path


#从数据库中取出总数
def getTableTotal(tablename):
    sql = 'select count(1) from %s where isdel=2'%tablename;
    db = Mysql()
    query = db.queryDataBySql(sql)
    return query

#从数据库中取出一页
def getPage(tablename, page = 1, pagesize = 10):
    if page < 1 :
        page = 1
    offset  = (page - 1) * pagesize
    end     = offset + pagesize
    sql = "select * from %s where isdel = 2 and class in ('杜鹃', '桂花', '荷花', '菊花', '康乃馨', '梅花', '玫瑰', '米兰花', '茉莉', '牡丹', '郁金香', '栀子花') limit %s, %s" % (tablename, offset, end)
    print sql
    db = Mysql()
    query = db.queryDataBySql(sql)
    return query

def ExecMul():
    newBaiDs = getPage('new_bing_flower', 1, 1000000)
    for row in newBaiDs:
        sid = row[0]
        url = row[1]
        sclass= row[2].strip()
        sub_class = row[3].strip()
        m2 = hashlib.md5()
        m2.update(url)
        filename = m2.hexdigest();

        path = '/home/ylj/tag_sys/GrapImage/new_bing_flower/%s/%s/%s.jpg' % (sclass, sub_class, filename)

        des_path = '/home/ylj/tag_sys/GrapImage/TRAINS_bak/%s/%s.jpg' % (sclass, filename)
        des = '/home/ylj/tag_sys/GrapImage/TRAINS_bak/%s/' % sclass
        if os.path.isfile(path):
            ddir = Path(des)
            if not ddir.exists():
                ddir.mkdir(parents=True)

            shutil.copy(path, des_path)
        else:
            print sclass, sub_class, path, des_path

ExecMul()






