# -*- coding:utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def co2_gdp_plot():
    
    # 读取数据
    df_data = pd.read_excel('ClimateChange.xlsx', sheetname='Data') 
    
    # 选择CO2和GDP数据并设置国家代码为索引
    df_co2 = df_data[df_data['Series code']==
            'EN.ATM.CO2E.KT'].set_index('Country code')
    df_gdp = df_data[df_data['Series code']==
            'NY.GDP.MKTP.CD'].set_index('Country code')
    
    # 处理缺失值
    df_co2_nan = df_co2.replace({'..': pd.np.NaN})
    df_gdp_nan = df_gdp.replace({'..': pd.np.NaN})
    df_co2_fill = df_co2_nan.iloc[:, 5:].fillna(
            method='ffill', axis=1).fillna(method='bfill', axis=1)
    df_gdp_fill = df_gdp_nan.iloc[:, 5:].fillna(
            method='ffill', axis=1).fillna(method='bfill', axis=1)

    # 数据合并
    df_co2_fill['CO2-SUM'] = df_co2_fill.sum(axis=1)
    df_gdp_fill['GDP-SUM'] = df_gdp_fill.sum(axis=1)
    df_union = pd.concat(
            [df_co2_fill['CO2-SUM'], df_gdp_fill['GDP-SUM']], axis=1)
    df_union = df_union.fillna(value=0)

    # 数据归一化处理
    df_max_min = (df_union - df_union.min()) / (df_union.max() - df_union.min())
    
    # 获取中国归一化后的 CO2和GDP 数据
    china = []
    for i in df_max_min[df_max_min.index == 'CHN'].values:
        china.extend(np.round(i, 3).tolist())

    # 获取5个常任理事国标签和对应的坐标刻度
    countries_labels = ['USA', 'CHN', 'FRA', 'RUS', 'GBR']
    sticks_labels = []
    labels_position = []

    for i in range(len(df_max_min)):
        if df_max_min.index[i] in countries_labels:
            sticks_labels.append(df_max_min.index[i])
            labels_position.append(i)

    # 绘图
    fig = plt.subplot()
    df_max_min.plot(kind='line', title='GDP-CO2', ax=fig)
    plt.xlabel('Countries')
    plt.ylabel('Values')
    plt.xticks(labels_position, sticks_labels, rotation='vertical')
    plt.show()
    return fig, china
