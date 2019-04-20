#!/usr/bin/env python3

class UserData(object):

    def __init__(self, usr_id, usr_name):
        self.usr_id = usr_id
        self._usr_name = usr_name


class NewUser(UserData):    

    def __call__(self):
        print("{}'s id is {}".format(self.usr_name, self.usr_id))

    @property
    def usr_name(self):
        return self._usr_name

    @usr_name.setter
    def usr_name(self, value):
        if len(value) <= 3:
            print("ERROR")
        else:
            self._usr_name = value


if __name__ == '__main__':
    user = NewUser(101, 'Jack')
    user()
