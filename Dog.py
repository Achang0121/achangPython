#!/usr/bin/env python3

class Dog():
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return 'Dog: {}'.format(self.name) #自定义打印格式

dog = Dog('jack', 2)
print(dog)   # 打印类的实例，执行print, 在Dog类中会自动调用 __repr__ 方法
print(dog.name)
print(dog.age)
