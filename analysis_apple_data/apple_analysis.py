# -*- coding:utf-8 -*-

import pandas as pd


def quarter_volume():
    data = pd.read_csv('apple.csv', header=0)

    # 选择数据
    s = data.Volume

    # 转换为时间序列
    s.index = pd.to_datetime(data.Date)
    
    #按季度重采样并排序
    second_volume = s.resample('Q').sum().sort_values()[-2]

    return second_volume

