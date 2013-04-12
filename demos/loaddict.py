#!/usr/bin/env python
# -*- encoding=utf8 -*-
#

import os
__author__ = 'vivi'


def load_dictionary(filename, sep='='):
    """
    simple function to load dictionary data from file
    """
    dic = dict()
    if os.path.exists(filename):
        f = open(filename, 'r')
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                continue
            else:
                splits = line.split(sep)
                if len(splits) != 2:
                    continue
                else:
                    dic[splits[0].strip()] = splits[1].strip()
        f.close()
    else:
        print "file %s is missing." % filename
    return dic

def jieba_segment_test():
    import jieba
    import jieba.analyse

    words = jieba.cut("中华人民共和国中央人民政府在今天成立了！")
    print '/'.join(words)
    for word in words:
        print word.flag

    tags = jieba.analyse.extract_tags('中华人民共和国中央人民政府在今天成立了！')
    print '/'.join(tags)

if __name__ == '__main__':
    dic = load_dictionary('dict.txt')
    print dic
    jieba_segment_test()