#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import random


def GenPassword(len=8):
    return ''.join(random.sample('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#*_', len))


for i in range(10):
    print(GenPassword(12))
