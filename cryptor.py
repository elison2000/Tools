#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# ------------------------------------------------ #
#         Title        : 加密解密程序              #
#         Version      : v1.1                      #
#         Author       : Elison                    #
#         Email        : Ly99@qq.com               #
#         Updated Date : 2018-8-21                 #
# ------------------------------------------------ #


import base64_
from Crypto.Cipher import AES
import settings


class Cryptor:
    "加密解密程序"

    def __init__(self, *, key, mode='ECB'):
        bs = AES.block_size
        self.pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs).encode('utf-8')
        self.unpad = lambda s: s[0:-s[-1]]

        iv = key[::-1]  # 初始向量为key的逆序
        if mode == 'ECB':
            self.cryptor = AES.new(key, AES.MODE_ECB)
        elif mode == 'CBC':
            self.cryptor = AES.new(key, AES.MODE_CBC, iv)
        else:
            assert mode in ('ECB', 'CBC'), 'mode参数错误'

    def encrypt(self, text):
        "加密方法"
        text = self.pad(text.encode('utf-8'))
        ciphertext = self.cryptor.encrypt(text)
        return base64_.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, text):
        "解密方法"
        ciphertext = base64_.b64decode(text)
        plain_text = self.cryptor.decrypt(ciphertext)
        return self.unpad(plain_text).decode('utf-8')


def encode_password(text, *, mode='ECB'):
    pc = Cryptor(key=settings.CRYPTOR_KEY, mode=mode)
    return pc.encrypt(text)


def decode_password(text, *, mode='ECB'):
    pc = Cryptor(key=settings.CRYPTOR_KEY, mode=mode)
    return pc.decrypt(text)


if __name__ == "__main__":
    text = '讯美科技广场'
    etext = encode_password(text)
    dtext = decode_password(etext)
    print((dtext, etext))
