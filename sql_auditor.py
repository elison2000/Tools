#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
# ------------------------------------------------ #
#         Title        : DDL审计程序               #
#         Version      : v1.1                      #
#         Author       : Elison                    #
#         Email        : Ly99@qq.com               #
#         Updated Date : 2018-11-15                #
# ------------------------------------------------ #
"""

import re
import sys
import pymysql
from datetime import datetime
from optparse import OptionParser


def filterSQL(sql):
    "过滤无效DDL"
    regex1 = re.compile('\s*$')  # 空白行
    regex2 = re.compile('(\s*#|\s*--|#|--).*')  # 注释
    if regex1.match(sql):
        print("过滤空白行：{0}".format((sql,)))
    elif regex2.match(sql):
        print("过滤注释：{0}".format((sql,)))
    else:
        return 100


def getSQLHead(sql):
    "获取ddl头部信息"
    regex = re.compile('(create|alter)\s*(table)\s*(\w\w*)\s', re.I)
    text = regex.search(sql)
    try:
        head = ' '.join((text.group(1), text.group(2), text.group(3)))
        return head
    except Exception as e:
        print("DDL不合法：{0}".format((sql,)))


class auditor:
    def __init__(self, conf):
        host = conf['host']
        port = int(conf['port'])
        db = conf['db']
        user = 'audit'
        passwd = 'audit'
        if db[len(db) - 2:] not in ['01', '02', '03', '04', '05', '06', '07', '08']:
            print('数据库名有误：{0}'.format(db))
            sys.exit(-1)
        self.sql_list = []
        self.exec_sql_list = []
        try:
            self.conn = pymysql.connect(host=host, port=port, db=db, user=user, password=passwd, charset='utf8mb4')
            self.conn.cursor().execute('select now()')  # 测试连接
        except Exception as e:
            print("数据库连接失败：{0}".format(str(e)))
            sys.exit(-1)

    def execute(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        return 1

    def getDDL(self, filename):
        "获取DDL"
        sql_list = []
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()

        sql_list = data.split(';')
        for sql in sql_list:
            if filterSQL(sql):  # 过滤空白行
                head = getSQLHead(sql)
                if head:
                    dict = {'head': head, 'sql': sql}
                    self.sql_list.append(dict)

    def auditDDL(self):
        "审核DDL"
        for i in self.sql_list:
            head = i['head']
            sql = i['sql']
            # 检验规则
            if re.search('rename\s', sql, re.I):
                print("不能重命名表名或列名：{0}".format((sql,)))
            elif re.search('\schange\s', sql, re.I):
                print("不能使用change语法：{0}".format((sql,)))
            elif re.search('drop table', sql, re.I):
                print("不能删除表：{0}".format((sql,)))
            elif re.search('alter\s*table.*drop\s', sql, re.I):
                print("不能删除列：{0}".format((sql,)))
            else:
                self.exec_sql_list.append(i)

    def execDDL(self):
        "执行DDL"
        for i in self.exec_sql_list:
            head = i['head']
            sql = i['sql']
            print("[{0}] 执行： {1}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), head))
            try:
                self.execute(sql)
                print("[{0}] 执行成功".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            except Exception as e:
                print("[{0}] 执行失败：{1}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(e)))

    def close(self):
        self.conn.close()


# main

# 参数处理
parser = OptionParser(add_help_option=False)
parser.add_option("--help", action="help")
parser.add_option("-v", "--version", dest="version", action='store_true',
                  help="show version of the program")
parser.add_option("-H", "--host", dest="host", type='string',
                  help="the host & port of database, eq: 127.0.0.1:3306")
parser.add_option("-u", "--user", dest="user", type='string',
                  help="the login user of database")
parser.add_option("-p", "--password", dest="password", type='string',
                  help="the login password of database")
parser.add_option("-d", "--database", dest="database", type='string',
                  help="the name of database")
parser.add_option("-f", "--file", dest="file", type='string',
                  help="the filename which be executed")

(options, args) = parser.parse_args()

if options.version:
    print(__doc__)
    sys.exit()

try:
    host = options.host.split(':')[0]
    port = options.host.split(':')[1]
    host.split('.')[3]
except Exception as e:
    print("IP或端口格式错误!")
    sys.exit(-1)

if options.database:
    db = options.database
else:
    print("必须指定数据库名")
    sys.exit(-1)

if options.file:
    filename = options.file
else:
    print("必须指定要执行的文件名")
    sys.exit(-1)

if options.user:
    user = options.user
else:
    user = 'audit'

if options.password:
    passwd = options.password
else:
    passwd = 'elison321'

conf = {'host': host, 'port': port, 'db': db}

# 创建实例
aud = auditor(conf)
aud.getDDL(filename)  # 获取DDL
aud.auditDDL()  # 审核DDL
aud.execDDL()  # 执行DDL
