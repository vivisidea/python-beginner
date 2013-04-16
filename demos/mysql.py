#!/usr/bin/env python
# -*- encoding:utf8 -*-
#
__author__ = 'vivi'

"""
todo:// 
"""

import MySQLdb

def getconnection():
    db = MySQLdb.connect(host='localhost', user='vivi', passwd='netease', db='test')
    return db

def mysqldemo():
    """
    official documentation is not good enough.
    http://www.mikusa.com/python-mysql-docs/index.html
    """
    db = getconnection()
    cur = db.cursor(MySQLdb.cursors.DictCursor) # default cursor is a list

    cur.execute("""INSERT INTO test(hobby, name) VALUES (%s, %s)""", ('vivi', 'test'))
    cur.execute('SELECT * FROM test LIMIT 100')
    for row in cur.fetchall():
        print row['NAME']

    cur.execute('SELECT * FROM test')
    print cur.rowcount
    row = cur.fetchone()
    while row is not None:
        print row
        row = cur.fetchone()


    db.commit() # you have to call db.commit() before closing the connection, or the insert/update will be lost
    cur.close()
    db.close()

if __name__ == '__main__':
    mysqldemo()