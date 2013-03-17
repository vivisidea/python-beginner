#!/usr/bin/env python
# -*- encoding=utf8 -*-
#
"""
simple script demo the usage of pickle module
"""

import pickle
import os
from cStringIO import StringIO

data = dict.fromkeys([i for i in xrange(1, 10)], 'pickle test')
list_data = [x for x in xrange(1, 100, 2)]

if __name__ == '__main__':
    print data
    print list_data
    file_name = 'demos/pickle.dat'

    if os.path.exists(file_name):
        f = open(file_name, 'r')
        data = pickle.load(open(file_name))
        print 'load data from pickle file %s, data=%s' % (file_name, data)
        f.close()
    else:
        f = open(file_name, 'w+')
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL) # 指定使用的协议，load的时候不需要指定
        print 'dump object to pickle file done, file = %s' % (file_name)
        f.flush()
        f.close()
    s = pickle.dumps('12345', pickle.HIGHEST_PROTOCOL)
    print s
    obj = pickle.loads(s)
    print obj
    sio = StringIO()
    pickle.dump([x for x in xrange(1,10)], sio)
    print sio.getvalue()