#!/usr/bin/env python3

from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client.louplus

db.users.insert_many([
    {'user_id': 1000, 'name': 'Shiyan', 'pass': 10, 'study_time': 50,},
    {'user_id': 2000, 'name': 'Lou', 'pass': 15, 'study_time':171,}
])


