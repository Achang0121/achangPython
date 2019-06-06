# -*- coding:utf-8 -*-

import pandas as pd

def co2():

    # 读取 Data 数据表

    df_data = pd.read_excel('ClimateChange.xlsx', sheetname='Data')
    # 选取 EN.ATM.CO2E.KT 数据，并将国家代码设置为索引
    df_data = df_data[df_data['Series code']=='EN.ATM.CO2E.KT'].set_index('Country code')
    # 剔除不必要的数据
    df_data.drop(labels=['Country name', 'Series code', 'Series name', 'SCALE', 'Decimals'], axis=1, inplace=True)
    # 将原数据集中不规范的空值替换为NaN 方便填充
    df_data.replace({'..': pd.np.NaN}, inplace=True)
    # 对NaN空值进行向前和向后填充
    df_data = df_data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    # 对填充后依旧全部为空值的数据进行剔除
    df_data.dropna(how='all', inplace=True)
    df_data['Sum emissions'] = df_data.sum(axis=1)
    df_data = df_data['Sum emissions']


    # 处理 Country 数据表
    # 将国家代码设置为索引
    df_countries = pd.read_excel('ClimateChange.xlsx', sheetname='Country')
    df_countries.set_index('Country code', inplace=True)
    # 剔除不必要的数据
    df_countries.drop(labels=['Capital city', 'Region', 'Lending category'], axis=1, inplace=True)

    # 合并数据表
    df_union = pd.concat([df_data, df_countries], axis=1)

    # 按收入群体对数据进行求和
    df_sum = df_union.groupby('Income group').sum()

    df_max = df_union.sort_values(by='Sum emissions', ascending=False).groupby('Income group').head(1).set_index('Income group')
    df_max.columns = ['Highest emissions', 'Highest emission country']
    df_max = df_max.reindex(columns=['Highest emission country', 'Highest emissions'])
    df_min = df_union.sort_values(by='Sum emissions').groupby('Income group').head(1).set_index('Income group')
    df_min.columns = ['Lowest emissions', 'Lowest emission country']
    df_min = df_min.reindex(columns=['Lowest emission country', 'Lowest emissions'])
    result = pd.concat([df_sum, df_max, df_min], axis=1)

    return result


re = co2()
print(re)
