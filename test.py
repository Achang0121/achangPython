#!/usr/bin/env python3

class Test(object):

    def __init__(self, data=0):
        self.data = data

    def __iter__(self):
        return self

    def __next__(self):
        if self.data > 5:
            raise StopIteration
        else:
            self.data += 1
            return self.data

for i in Test():
    print(i)
