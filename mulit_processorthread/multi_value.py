#!/usr/bin/env python3

import time
from multiprocessing import Process, Value, Lock

# 该函数运行在子进程中，参数Val 是一个Value对象，是全局变量
def func(val, lock):
    # 将val这个全局变量的值进行50次加1操作
    for i in range(50):
        time.sleep(0.01)
        # with lock 语句是对现面语句的简写
        """
        lock.acquire()
        val.value += 1
        lock.release()
        """
        # 为val变量加锁，结果就是任何时刻只有一个进程可以获得 lock锁
        # 自然val的值就不会同时被多个进程改变
        with lock:
            val.value += 1

def main():
    # 多进程无法使用全局变量，multiprocessing提供的Vlaue是一个代理器，可以实现多进程中共享这个变量
    # val是一个Value对象，它是全局变量，数据类型是int，初始值为0
    val = Value('i', 0)
    # 初始化锁
    # Lock和Value一样，是一个函数或者方法，Lock的返回值就是一把全局锁
    # 注意这把全局锁的使用范围就是当前主进程及其子进程，也就是在运行当前这个python文件过程中有效
    lock = Lock()
    # 创建10个任务，备用
    processes = [Process(target=func, args=(val, lock)) for i in range(10)]
    # 启动10个子进程来运行processes中的任务，对Value对象进行 +1操作
    for process in processes:
        process.start()
    # join方法使主进程挂起，直至所有子进程运行完毕
    for process in processes:
        process.join()
    print(val.value)

if __name__ == '__main__':
    for i in range(5):
        main()
