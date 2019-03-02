#!/usr/bin/python
# -*- coding: utf-8 -*-
# From: ubuntu.org.cn Copyright: GPLv2

from datetime import datetime
import requests

# 测试代理是否有效  http://httpbin.org/get
# 获取代理列表 http://free-proxy.cz/zh/proxylist/country/all/socks5/ping/all
# YouTube
# Google

test_url = "http://httpbin.org/get"

file_path = 'ip.txt'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
}

loop_count = 2


def avg_list(c_list):
    total = 0
    for i in range(len(c_list)):
        total += c_list[i]
    return total / len(c_list)


def avg_proxy_cost(ip):
    cost_list = []
    for j in range(loop_count):
        start = datetime.now()
        flag = check_proxy(ip)
        end = datetime.now()
        if flag:
            ss = (end - start).total_seconds()
            print "ip=", ip, " 第", j + 1, "次,花费时间=", ss, "s"
            cost_list.append(ss)

    # 每次check都通过，取平均值
    if len(cost_list) == loop_count:
        avg = avg_list(cost_list)
        print ip, '平均花费', avg, 's时间'
        return avg
    else:
        return -1


def find_proxy():
    a = {}
    for ip in read_ip(file_path):
        avg = avg_proxy_cost(ip)
        if avg != -1:
            a[avg] = ip

    # 排序结果
    items = a.items()
    items.sort()
    print '\n\n\n\n\n速度排序 :'
    i = 0
    for k, v in items:
        print i, ' ', k, '-', v
        i = i + 1


def read_ip(path):
    ips = []
    with open(path, 'r') as f:
        for line in f.readlines():
            ips.append(line.strip())
    return ips


def check_proxy(ip):
    try:
        proxies = {
            'https': 'https://' + ip,
            'http': 'http://' + ip,
        }
        resp = requests.get(test_url, proxies=proxies, headers=headers, timeout=10)
        l = resp.text
        print((l))
        return True
    except Exception, err:
        print  err
        return False


if __name__ == '__main__':
    find_proxy()
