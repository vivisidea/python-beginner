#!/usr/bin/python
# -*- encoding:utf8 -*-
#
#

SLASH_COUNT = 4
def get_prefix(input):
    count = line.count('/')
    if count <= 3:
        return None
    else:
        index = -1
        for i in xrange(0, SLASH_COUNT):
            index = input.index('/', index + 1)
        return input[0:index]

if __name__ == '__main__':
    f = open('list.txt', 'r')
    dic = dict()
    for line in f:
        key = get_prefix(line)
        if key is None:
            continue
        else:
            value = dic.get(key, None)
            dic[key] = 1 if value is None else value +1 
    f.close()
    for key, value in dic.items():
        print key, value
