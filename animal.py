#!/usr/bin/env python3

class Animal(object):
    owner = 'jack'

    def __init__(self, name):   # 初始化设置名字
        self._name = name      # 设置为私有属性
    
    @staticmethod
    def order_animal_food():
        print('ording...')
        print('ok')

    @classmethod
    def get_owner(cls):
        return cls.owner

    @classmethod
    def set_owner(cls, name):
        cls.owner = name

    def get_name(self):     # 获取名字，私有属性不可以直接被访问，因此设置该方法获取属性值
        return self._name

    def set_name(self, value):      # 设置私有属性
        self._name = value

    def make_sound(self):
        pass


class Dog(Animal):   # 继承父类 Animal
    def make_sound(self):    # 重写父类的 make_sound 方法
        print(self.get_name() + ' is making sound wang wang wang...')


class Cat(Animal):
    def make_sound(self):
        print(self.get_name() + ' is making sound miu miu miu...')


def main():
  #  dog = Dog('旺财')
  #  cat = Cat('Kitty')
  #  dog.make_sound()
  #  cat.make_sound()
    print(Animal.owner)      # 通过类本身访问公有的类属性
    print(Cat.owner)         # 通过子类访问公有的类属性
    animal = Animal('dog') # 实例化对象
    print(animal.owner)           # 通过实例化对象访问公有的类属性
    Animal.order_animal_food()

if __name__ == "__main__":
    main()
