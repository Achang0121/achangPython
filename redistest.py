#!/usr/bin/env python3

import redis

r = redis.StrictRedis(host='127.0.0.1', db=0)

r.hmset('user1', {
    'id': '1000',
    'name': 'Shiyan',
    'pass': '10',
    'study_time': '50',
    })
r.hmset('user2',{
    'id': '2000',
    'name': 'Lou',
    'pass': '15',
    'study_time': '171',
    })

