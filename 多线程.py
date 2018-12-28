#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# ------------------------------------------------ #
#         Title        : 多线程                    #
#         Version      : v1.0                      #
#         Author       : Elison                    #
#         Email        : Ly99@qq.com               #
#         Updated Date : 2018-5-1                  #
# ------------------------------------------------ #

import time
from datetime import datetime
from queue import Queue
import threading
import util.mysql
import util.crypt
import util.ssh


def get_nowstr():
    "获取当前时间"
    nowstr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return nowstr


def whether_to_run(rule):
    "1:运行  0:不运行  -1:规则有问题"
    now = datetime.now()
    r = rule.split()
    if len(r) == 5:
        if r[0] == '*': r[0] = now.minute
        if r[1] == '*': r[1] = now.hour
        if r[2] == '*': r[2] = now.day
        if r[3] == '*': r[3] = now.month
        if r[4] == '*': r[4] = now.isoweekday()

        if int(r[0]) == now.minute and int(r[1]) == now.hour and int(r[2]) == now.day and int(
                r[3]) == now.month and int(r[4]) == now.isoweekday():
            recode = 1
        else:
            recode = 0
    else:
        print("run_rule无效: {0}".format(rule))
        recode = -1
    return recode


def get_job_list():
    "获取即将运行的JOB"
    sql = "select job_id,job_name,job_type,run_rule,remote_hostname,remote_ip,remote_port,remote_user,remote_passwd ,run_command from jobs where enabled='Y'"
    job_info = util.mysql.query_eclk(sql)
    job_list = [i for i in job_info if whether_to_run(i['run_rule']) == 1]
    return job_list


def begin_log(row):
    "记录开始执行日志"
    sql = "insert into job_logs(job_id,begin_time,exec_status,exec_log) values(%s,%s,%s,%s)"
    stat = util.mysql.dml_eclk(sql, row)
    return stat


def end_log(row):
    "记录执行结束日志"
    sql1 = "update job_logs set end_time=%s,exec_status=%s,exec_log=%s where job_id=%s and begin_time=%s"
    sql2 = "update job_logs set exec_seconds=timestampdiff(second,begin_time,end_time) where job_id=%s and begin_time=%s"
    sql3 = "update jobs set last_exec_time=%s,last_exec_status=%s where job_id=%s"
    stat1 = util.mysql.dml_eclk(sql1, (row[2], row[3], row[4], row[0], row[1]))
    stat2 = util.mysql.dml_eclk(sql2, (row[0], row[1]))
    stat3 = util.mysql.dml_eclk(sql3, (row[2], row[3], row[0]))
    return min([stat1, stat2])


def run_job(row):
    "运行JOB"
    btime = get_nowstr()
    job_id = row['job_id']
    job_name = row['job_name']
    print('[{0}]  开始执行：【{1}, {2}】'.format(get_nowstr(), job_id, job_name))
    cmd = row['run_command']
    conf = {'host': row['remote_ip'], 'port': row['remote_port'], 'user': row['remote_user'],
            'passwd': util.crypt.decodePassword(row['remote_passwd'])}

    bdata = [job_id, btime, '1', '执行中或异常结束']
    # 插入开始日志
    begin_log(bdata)

    # 执行命令
    res = util.ssh.exec_cmd(conf, cmd)
    etime = get_nowstr()

    # 插入结束日志
    edata = [job_id, btime, etime, res[0], res[1]]
    end_log(edata)
    print('[{0}]  执行结束：【{1}, {2}】'.format(get_nowstr(), job_id, job_name))


def put_job_queue(queue):
    while True:
        now = datetime.now()
        time.sleep(60 - now.second)  # 下一分钟0秒执行
        [job_queue.put(i) for i in get_job_list()]  # 获取即将运行的JOB放入队列


# main
job_queue = Queue()

job_queue.qsize()

# 开启获取job线程
Producer = threading.Thread(name='Producer', target=put_job_queue, args=(job_queue,))
Producer.setDaemon(True)
Producer.start()

# 运行job
Consumers = {'Consumer-1': None, 'Consumer-2': None, 'Consumer-3': None, 'Consumer-4': None, 'Consumer-5': None,
             'Consumer-6': None, 'Consumer-7': None, 'Consumer-8': None, 'Consumer-9': None, 'Consumer-10': None}
while True:
    for name in Consumers.keys():
        if Consumers[name] is None or not Consumers[name].isAlive():
            job = job_queue.get_nowait()
            if job:
                thd = threading.Thread(name=name, target=run_job, args=(job,))
                thd.setDaemon(True)
                thd.start()
                Consumers[name] = thd
    else:
        time.sleep(10)
