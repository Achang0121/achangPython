#!/usr/bin/env python3

class Animal(object):
    __slots__ = ('name', 'age') # 限定 Animal 类只能定义 name 和 age 属性


class Cat(Animal):
    __slots__ = ('address')


dog = Animal()
dog.name = 'wangcai'
dog.age = 2
# dog.gender = 'male'  # dog 是 Animal 的实例化对象，无法定义 gender 属性
"""
^^^报错
dog.gender = 'male'  # dog 是 Animal 的实例化对象，无法定义 gender 属性
AttributeError: 'Animal' object has no attribute 'gender'
"""

cat = Cat()
cat.gender = 'male'  # 无法定义 gender 属性
cat.address = 'chengdu'
cat.name = 'tom'     # 由于 Cat 继承的是 Animal 所以可以定义 name 属性
"""
^^^报错
cat.gender = 'male'  # 无法定义 gender 属性
AttributeError: 'Cat' object has no attribute 'gender'
"""
