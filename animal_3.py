#!/usr/bin/env python3

class Animal(object):

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

    def __getattribute__(self, attr):
        print('调用了 __getattribute__ 方法， 访问{}属性'.format(attr))

        if attr in ('name', 'gender'):
            return object.__getattribute__(self, attr)
        else:
            print('交给 __getattr__ 处理...')
            return object.__getattr__(self, attr)

    def __getattr__(self, attr):
        print('调用了 __getattr__ 方法，访问{}属性'.format(attr))
        if attr == 'age':
            return 3
        else:
            return '__getattr__ 方法中未找到该属性'

dog = Animal('wangcai', 'male')
dog.name
dog.gender
dog.age
dog.address

