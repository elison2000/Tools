#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ------------------------------------------------ #
#         Title        : 提取windows聚焦壁纸       #
#         Version      : v1.0                      #
#         Author       : Elison                    #
#         Email        : Ly99@qq.com               #
#         Updated Date : 2018-9-2                  #
# ------------------------------------------------ #

import os
import sys
import shutil
from PIL import Image

home = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
srcdir = home + r'\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets'
dstdir = r'D:\Pictures\Windows聚焦'


def mycopyfile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.copyfile(srcfile, dstfile)  # 复制文件
        print("copy %s -> %s" % (srcfile, dstfile))


try:
    os.chdir(dstdir)
    os.chdir(srcdir)
except Exception as e:
    print(e)
    sys.exit()

for i in os.listdir():
    dstfile = """{0}\{1}.jpg""".format(dstdir, i)
    im = Image.open(i)
    if im.size[0] == 1920 and not os.path.exists(dstfile):
        mycopyfile(i, dstfile)
