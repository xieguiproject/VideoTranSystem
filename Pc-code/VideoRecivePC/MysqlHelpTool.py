#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# exit interrupt lib
import time
import sys
import os
import pymysql

#1、安装 mysql https://pypi.org/project/MySQL-python/#files
class MysqlHelpTool(object):
    def __init__(self,host,user,passwd,databases):
        self.db = pymysql.Connect(host=host, user=user, password=passwd, database=databases, charset='utf8')
        self.cursor = self.db.cursor()
        pass
    def get(self,table,Conditions):
        sql = "SELECT * FROM %s WHERE %s" % (table,Conditions)
        #print(sql)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
            #print(result)
        except:
            print("Error : unable to fech data")
            return None
    def delete(self,table,Field):
        #删除指定记录
        sql = 'DELETE FROM %s WHERE %s;' % (table, Field)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print("Error : unable to update data")
    def update(self,table,Field,condition):
        sql = 'UPDATE %s SET %s WHERE %s;' % (table,Field,condition)
        #print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print("Error : unable to update data")
    def insert(self,table,Field,data):
        sql = "INSERT INTO %s (%s) VALUES (%s);" % (table,Field,data)
        #print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print("Error : unable to insert data")