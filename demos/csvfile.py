#!/usr/bin/env python
# -*- encoding:utf8 -*-
#
__author__ = 'vivi'

"""
this is a simple code snipet manipulating csv file
csv = comma separated values
"""

import csv

def write_csv_file(rows, filepath='file.csv'):
    """
    write the data into a csv file.
    """
    with open(filepath, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(rows)

def read_csv_file(filepath='file.csv'):
    """
    reads the csv file and process
    """
    with open(filepath, 'rb') as f:
        csvreader = csv.reader(f, delimiter=',') # reader 可以接收一个file-like-obj
        for row in csvreader:
            print '-'.join(row)

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
    rows = [x for x in xrange(1,10,1)]
    write_csv_file(rows)
    read_csv_file('file.csv')

