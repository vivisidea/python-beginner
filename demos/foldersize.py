#!/usr/bin/env python
# -*- encoding:utf8 -*-
#
__author__ = 'vivi'

"""
calculate the size of the folders
"""

import os
import random

# define the conversion of bytes to Kilo & Mega & Giga bytes
KILO = 1024
MEGA = 1024 * KILO
GIGA = 1024 * MEGA

to10files = [('', 0) for x in xrange(10)]
def bytestoreadable(bytes):
    """
    convert bytes to human readable strings, eg: 1024k -> 1M
    """
    if bytes / GIGA > 0:
        return '%.2f G' % (bytes * 1.0 / GIGA)
    elif bytes / MEGA > 0:
        return '%.2f M' % (bytes * 1.0 / MEGA)
    elif bytes / KILO > 0:
        return '%.2f K' % (bytes * 1.0 / KILO)
    else:
        return '%s B' % bytes

def foldersize(path):
    sizebytes = 0
    files = os.listdir(path)
    for f in files:
        f = os.path.join(path, f)
        if os.path.isdir(f): # this will count the symbol link
            sizebytes += foldersize(f)
        else:
            size_t = os.stat(f).st_size
            print '%s sizebytes=%s(%s)' % (f, size_t, bytestoreadable(size_t))
            store_top_10((f, size_t))
            sizebytes += size_t
    return sizebytes

def store_top_10(size_t):
    """
    store the top 10 folders
    """
    if size_t[1] <= to10files[-1][1]: # not in the top N just return
        return
    else: # replace the minimal element and bubble up
        to10files[-1] = size_t
        for k in xrange(len(to10files) - 1, 0, -1):
            if to10files[k][1] > to10files[k-1][1]:
                t = to10files[k]
                to10files[k] = to10files[k-1]
                to10files[k-1] = t
    print to10files

if __name__ == '__main__':
    size = foldersize(os.path.expanduser('~/software'))
    print 'total size of this folder = %s' % bytestoreadable(size)
#    print foldersize(os.path.expanduser('~/software'))

    print
    print 'the top 10 large files are:'
    for (path, size) in to10files:
        print '%s=%s' % (path, bytestoreadable(size))
