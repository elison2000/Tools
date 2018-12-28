#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import os

dir = 'E:/Music/1、俄罗斯'
# dir = 'E:/Music/2、欧美'
# dir = 'E:/Music/3、日韩'
# dir = 'E:/Music/4、中国'
# dir = 'E:/Music/5、歌手'
# dir = 'E:/Music/6、张学友'

os.chdir(dir)
i = 0
for name in os.listdir():
    i += 1
    lst = name.split('、')
    if len(lst) == 1:
        pre = '{0:0>3}'.format(600 + i)
        new_name = pre + '、' + name
        print(new_name)
        os.rename(name, new_name)
