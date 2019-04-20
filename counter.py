#!/usr/bin/env python3

class Counter(object):

    def __init__(self, func):
# 把类用作装饰器时， init 只能接受被装饰的函数这一个参数
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):   # 让对象可以调用
        self.count += 1
        return self.func(*args, **kwargs)

@Counter
def num_counter():
    pass


for i in range(20):
    num_counter()

print(num_counter.count)
