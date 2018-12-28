#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# -----------------------------------------------#
#         Title        : 上网认证                #
#         Version      : v1.0                    #
#         Author       : Elison                  #
#         Email        : Ly99@qq.com             #
#         Updated Date : 2018-12-22              #
# -----------------------------------------------#


import requests
from cryptor import decode_password

if __name__ == "__main__":
    cpwd = '0TG6KQgqLPX3P5qR0YzAOQ=='
    pwd = decode_password(cpwd)
    url = 'http://1.1.1.3/ac_portal/login.php'
    payload = {'opr': 'pwdLogin', 'userName': 'chenyjc', 'pwd': pwd, 'rememberPwd': 0}
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    response = requests.post(url, headers=headers, data=payload)
    data = response.content
    text = data.decode('utf-8', 'ignore')
    print(text)
