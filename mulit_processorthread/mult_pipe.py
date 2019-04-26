#!/usr/bin/env python3

from multiprocessing import Process, Pipe

conn1, conn2 = Pipe()

def send():
    data = 'hello shiyanlou'
    conn1.send(data)
    print('Send Data: {}'.format(data))


def recv():
    data = conn2.recv()
    print('Receive Data: {}'.format(data))

def main():
    Process(target=send).start()
    Process(target=recv).start()


if __name__ == '__main__':
    main()
