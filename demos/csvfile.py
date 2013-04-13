#!/usr/bin/env python
# -*- encoding:utf8 -*-
#
__author__ = 'vivi'

"""
this is a simple code snipet manipulating csv file
csv = comma separated values
http://en.wikipedia.org/wiki/Comma-separated_values
一般来说，csv文件每行一条记录，一般来说每条记录的field的数量是相同的
field之间使用delimiter来分割，如果field里面有delemiter，field需要使用quotechar包起来，field里面的quotechar使用两个quote表示
"""

import csv

def write_csv_file(rows, filepath='file-out.csv'):
    """
    write the data into a csv file.
    """
    with open(filepath, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            csvwriter.writerow(row)

def read_csv_file(filepath='file.csv'):
    """
    reads the csv file and process
    """
    rows = []
    with open(filepath, 'rb') as f:
        csvreader = csv.reader(f, delimiter=',', quotechar='"') # reader 可以接收一个file-like-obj
        for row in csvreader:
            rows.append(row)
            print '-'.join(row)
    return rows

def usewith():
    with with_file() as f:
        for line in f:
            print line,

class with_file:
    """
    this is how with statement works maybe.
    """
    def __enter__(self):
        print 'inside enter.'
        return 'abcdef'
    def __exit__(self, exc_type, exc_val, exc_tb):
        print 'inside exit block'
        return

if __name__ == '__main__':
    usewith()
#    rows = [x for x in xrange(1,10,1)]
#    write_csv_file(rows)
    rows = read_csv_file('file.csv')
    write_csv_file(rows)

