#coding: utf-8

from mysql import Mysql
import hashlib

#从数据库中取出总数
def getTableTotal(tablename):
    sql = "select count(1) from %s where isdel=2 and class='一串红'"%tablename;
    db = Mysql()
    query = db.queryDataBySql(sql)
    return query

#从数据库中取出一页
def getPage(tablename, page = 1, pagesize = 10):
    if page < 1 :
        page = 1
    offset  = (page - 1) * pagesize
    end     = offset + pagesize
    sql = 'select * from %s where isdel = 2 limit %s, %s' % (tablename, offset, end)
    db = Mysql()
    query = db.queryDataBySql(sql)
    return query

def ExecMul():
    newBaiDs = getPage('new_baidu_flower', 1, 1000000)
    for row in newBaiDs:
        sid = row[0]
        url = row[1]
        sclass= row[2].strip()
        sub_class = row[3].strip()
        m2 = hashlib.md5()
        m2.update(url)
        filename = m2.hexdigest();

        path = '/home/ylj/tag_sys/GrapImage/new_baidu_flower/%s/%s/%s.jpg' % (sclass, sub_class, filename)

        des_path = '/home/ylj/tag_sys/GrapImage/baike_fl/download_deal/%s/%s.jpg' % (sclass, filename)
        print sclass, sub_class, path, des_path

ExecMul()






