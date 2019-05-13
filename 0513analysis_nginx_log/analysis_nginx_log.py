# -*- coding:utf-8 -*-

import re
from datetime import datetime
from collections import Counter

# 使用正则表达式解析日志文件，返回数据列表
def open_parser(filename):
    with open(filename) as logfile:
        # 似乎用正则表达式解析日志文件
        pattern = (
                   r'(\d+.\d+.\d+.\d+)\s-\s-\s'  # IP地址
                   r'\[(.+)\]\s'              # 时间
                   r'"GET\s(.+)\s\w+/.+"\s'   # 请求路径
                   r'(\d+)\s'                 # 状态码
                   r'(\d+)\s'                 # 数据大小
                   r'"(.+)"\s'                # 请求头
                   r'"(.+)"'                  # 客户端信息
                   )
        parsers = re.findall(pattern, logfile.read())
    return parsers


def main():
    
    # 使用正则表达式解析日志文件
    logs = open_parser('/home/shiyanlou/Code/nginx.log')
    ip_list = []
    request404_list = []

    """
    1. 解析文件就是分离不同类型数据（IP, 时间, 状态码等）
    2. 从解析后的文件中统计挑战需要的信息
    """
    for log in logs:
        # 转换原时间格式
        dt = datetime.strptime(log[1][:-6], "%d/%b/%Y:%H:%M:%S")
        # 获取 11 日当天的数据，返回所有满足条件的 IP
        if int(dt.strftime("%d")) == 11:
            ip_list.append(log[0])
        # 获取状态码为 404 的数据，返回满足条件的请求地址
        if int(log[3]) == 404:
            request404_list.append(log[2])

    ip_counts = Counter(ip_list)
    request404_counts = Counter(request404_list)

    # 排序
    sorted_ip = sorted(ip_counts.items(), key=lambda x: x[1])
    sorted_request404 = sorted(request404_counts.items(), key=lambda x: x[1])

    ip_dict = dict([sorted_ip[-1]])
    url_dict = dict([sorted_request404[-1]])
    
    return ip_dict, url_dict


if __name__ == '__main__':
    ip_dict, url_dict = main()
    print(ip_dict, url_dict)
    


