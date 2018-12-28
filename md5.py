#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from hashlib import md5


def md5_text(text):
    code = md5(text.encode('gbk')).hexdigest()
    return code


def md5_file(filename):
    with open(filename, 'rb') as f:
        code = md5(f.read()).hexdigest()
    return code


if __name__ == "__main__":
    filename1 = r'D:\py3proj\Tools\md5.py'
    filename2 = r'D:\py3proj\Tools\md5.py'
    print(md5_file(filename1))
    print(md5_file(filename2))
