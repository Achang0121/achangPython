#!/usr/bin/env python3

from multiprocessing import Process, Queue

# 创建队列实例
queue = Queue()

# 该函数的任务是向队列中发送数据
def f1(q):
    i = 'Hello shiyanlou'
    q.put(i)
    print('Send Data: {}'.format(i))


# 该函数的任务是从队列中获取数据
def f2(q):
    data = q.get()
    print('Receive Data: {}'.format(data))


def main():
    Process(target=f1, args=(queue,)).start()
    Process(target=f2, args=(queue,)).start()


if __name__ == '__main__':
    main()
