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

for name in os.listdir():
    lst = name.split('、')
    if len(lst) == 2:
        new_name = lst[1]
        print(new_name)
        try:
            os.rename(name, new_name)
        except Exception as e:
            pass
