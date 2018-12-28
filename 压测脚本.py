#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# ------------------------------------------------ #
#         Title        : 压测脚本                  #
#         Version      : v1.1                      #
#         Author       : Elison                    #
#         Email        : Ly99@qq.com               #
#         Updated Date : 2018-8-1                  #
# ------------------------------------------------ #


import datetime
import random
import pymysql
from multiprocessing import Process, Queue, Lock, Manager

# 自定义变量
connstr = {'host': '172.29.0.201', 'port': 3311, 'user': 'elison', 'passwd': 'abc123', 'db': 'test'}
parallel = 100
count = 100000
stop_token = 'stop!!!'


class mysql():
    def __init__(self, connstr):
        self.conn = pymysql.connect(host=connstr['host'], port=int(connstr['port']), user=connstr['user'],
                                    password=connstr['passwd'], db=connstr['db'], charset='utf8mb4')

    def query(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        return res

    def close(self):
        self.conn.close()


def get_sql():
    # sql = """update bid_purchase_order01 set bid_record_id=bid_record_id+1 where id={0}""".format(random.randint(1, 20000000))
    sql = """select /* test_performance */ order_id,user_id,business_no,loan_no,bid_record_id,credit_amount,actual_amount,state,remark,create_time,update_time,invest_record_id,invest_type,business_date,batch_no from bid_purchase_order01 where id={0}""".format(
        random.randint(1, 20000000))
    return sql


def loop_query(count, conn):
    for i in range(count):
        sql = get_sql()
        # print(sql)
        res = conn.query(sql)


conn_pool = [mysql(connstr) for i in range(parallel)]
prc_pool = []

# 开始
print("[{0}]  开始压测".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

# 开启压测进程
for i in range(parallel):
    p = Process(name="Worker" + str(i + 1), target=loop_query, args=(count, conn_pool[i]))
    p.daemon = True
    p.start()
    prc_pool.append(p)
    # print("[{0}]  {1} 进程已启动".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),p.name))

# 压测进程退出
for p in prc_pool:
    p.join()
# print("[{0}]  {1} 进程已结束".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),p.name))


# 结束
print("[{0}]  压测结束".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
