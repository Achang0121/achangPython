#!/usr/bin/env python3

import time
from multiprocessing import Process


def io_task():
    # time.sleep() 强行挂起当前进程
    # 所谓‘挂起’，就是进程停滞，后续代码无法运行，CPU 无法工作的状态
    # 相当于进行了一个耗时1秒的IO操作
    # 上文提到过，IO操作可能会比较耗时，但它不会占用CPU
    # 在这一秒钟内，CPU可能被运算器派往其它进程/线程中工作
    time.sleep(1)


def main():
    start_time = time.time()
    # 循环IO操作5次
    for i in range(5):
       io_task()
    # 子进程运行完毕，以下代码运行在主进程中
    end_time = time.time()
    # 打印运行耗时，保留2位小数
    print('程序运行耗时：{:.2f} s'.format(end_time-start_time))

if __name__ =='__main__':
    main()



