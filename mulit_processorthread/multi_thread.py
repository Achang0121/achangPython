#!/usr/bin/env python3

import threading

def hello(name):
    # get_ident() 方法获取当前线程ID
    print('当前为子线程，线程ID: {}'.format(threading.get_ident()))
    print('Hello' + name)


def main():
    print('当前为主线程，线程ID:{}'.format(threading.get_ident()))
    print('-----------------------------------------------------')
    # 初始化一个子线程，参数传递和使用同Process
    t = threading.Thread(target=hello, args=("shiyanlou",))
    # 启动线程和等待线程结束，和Process的接口一样
    t.start()
    t.join()
    print('-----------------------------------------------------')
    print('当前为主线程，线程ID:{}'.format(threading.get_ident()))

if __name__ =='__main__':
    main()
