# -*- coding:utf-8 -*-


import MySQLdb
import time
from Log import Log


class Mysql:
    # 获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    # 数据库初始化
    def __init__(self):
        try:
            self.db = MySQLdb.connect('127.0.0.1', 'root', '123456', 'flowers')
            self.cur = self.db.cursor()
        except MySQLdb.Error, e:
            Log.error("连接数据库错误，原因%d: %s" % (e.args[0], e.args[1]))

    # 插入数据
    def insertData(self, table, my_dict):
        try:
            self.db.set_character_set('utf8')
            cols = ', '.join(my_dict.keys())
            values = '", "'.join(my_dict.values())
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, '"' + values + '"')
            Log.info(sql)
            try:
                result = self.cur.execute(sql)
                insert_id = self.db.insert_id()
                self.db.commit()
                # 判断是否执行成功
                if result:
                    return insert_id
                else:
                    return 0
            except MySQLdb.Error, e:
                # 发生错误时回滚
                self.db.rollback()
                # 主键唯一，无法插入
                if "key 'PRIMARY'" in e.args[1]:
                    Log.error("数据已存在，未插入数据")
                else:
                    Log.error("插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
        except MySQLdb.Error, e:
            Log.error("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))
            if "server has gone away" in e.args[1]:
                self.db = MySQLdb.connect('127.0.0.1', 'ceshi', 'sq_123456', 'tag_sys')
                self.cur = self.db.cursor()

    #修改数据
    def updateData(self, tablename, data, condition):
        val = []
        for i in range(len(data)):
            val.append(data.keys()[i] + "='" + str(data.values()[i]) + "'")
        val1 = ",".join(val)
        sql = "update " + tablename + " set " + val1 + " where " + condition
        return sql

    def upDate(self, tablename, data, condition):
        try:
            print data
            sql = self.updateData(tablename, data, condition)
            Log.info(sql)
            result = self.cur.execute(sql)
            self.db.commit()
            print result
        except MySQLdb.Error, e:
            Log.error("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))
    #查询数据
    def queryData(self, table, fields, conditions):
        try:
            self.db.set_character_set('utf8')
            sql = "select %s from %s where %s" % (fields, table, conditions)
            Log.info(sql)
            try:
                self.cur.execute(sql)
                results = self.cur.fetchall()
                return results
            except MySQLdb.Error, e:
                Log.error("查询失败")
        except MySQLdb.Error, e:
            Log.error("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))

    #根据条件直接查询
    def queryDataBySql(self, sql):
        try:
            self.db.set_character_set('utf8')
            Log.info(sql)
            try:
                self.cur.execute(sql)
                results = self.cur.fetchall()
                return results
            except MySQLdb.Error, e:
                Log.error("查询失败")
        except MySQLdb.Error, e:
            Log.error("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))


