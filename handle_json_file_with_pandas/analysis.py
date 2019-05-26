#!/usr/bin/env python3

import pandas as pd
import json

def analysis(file, user_id):
    times = 0
    minutes = 0

    # 读取数据
    try:
        datas = pd.read_json(file)
    except ValueError:
        return 0, 0

    # 选择数据
    s = datas[datas['user_id'] == user_id].minutes

    return s.count(), s.sum()

