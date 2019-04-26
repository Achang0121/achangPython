#!/usr/bin/env python3

import os
from multiprocessing import Process

def hello(name):
    # os.getpid() 用来获取当前进程 ID
    print('child process: {}'.format(os.getpid()))
    print('Hello ' + name)

# 当运行一个python程序，系统会创建一个进程来运行代码，被称为主进程或父进程
# 下面的 main() 函数就在主进程中运行
def main():
    # 打印当前进程即主进程的 ID
    print('parent process: {}'.format(os.getpid()))
    # Process 对象只是一个子任务，运行该任务时系统会自动创建一个子进程
    # 注意 args 参数要以tuple的方式传入
    p = Process(target=hello, args=('shiyanlou',))
    print('child process strat')
    # 启动一个子进程来运行子任务，该进程运行的是hello()函数中的代码
    p.start()
    p.join()
    # 子进程完成后，继续运行主进程
    print('child process stop')
    print('parent process: {}'.format(os.getpid()))


if __name__ == '__main__':
    main()
