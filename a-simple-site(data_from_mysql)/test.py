#!/usr/bin/env python3

import os

print(os.path.dirname(__file__))

print(os.path.dirname(os.path.dirname(__file__)))

dirs = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'files'))
print(dirs)
print(os.listdir(dirs))
