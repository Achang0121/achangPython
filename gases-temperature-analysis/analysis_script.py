# -*- coding:utf-8 -*-
import pandas as pd
from matplotlib import pyplot as plt


def climate_plot():
    # 读取NASA 全球温度变化数据集
    df_temperature = pd.read_excel('GlobalTemperature.xlsx', header=0)


    # 读取 世界银行气候变化数据集
    df_climate = pd.read_excel('ClimateChange.xlsx', sheetname='Data')

    # 温室气体数据清洁
    df_ghg = pd.DataFrame(df_climate).loc[df_climate['Series code'].isin(
        ['EN.ATM.CO2E.KT', 'EN.ATM.METH.KT.CE', 'EN.ATM.NOXE.KT.CE', 'EN.ATM.GHGO.KE.CE', 'EN.CLC.GHGR.MT.CE'])]

    df_ghg_nan = df_ghg.replace({'..': pd.np.NaN})
    df_ghg_fill = df_ghg_nan.iloc[:, 6:].fillna(
            method='ffill', axis=1).fillna(method='bfill', axis=1)
    df_ghg_clean = df_ghg_fill.sum()
    df_ghg_clean.index = pd.to_datetime(df_ghg_clean.index, format='%Y')

    # 全球气温数据清洁
    time_index = pd.to_datetime(df_temperature['Date'])

    df_temperature_reindex = pd.DataFrame(df_temperature.iloc[:, [1, 4]].values,
            index=time_index,
            columns=[['Land Average Temperature', 'Land And Ocean Average Temperature']])
    df_temperature_resample_A = df_temperature_reindex.resample('A').mean()
    df_temperature_resample_Q = df_temperature_reindex.resample('Q').mean()
    df_temperature_clean = df_temperature_resample_A.loc['1990-12-31':'2010-12-31']

    # 合并 DataFrame并整理
    df_merge_temp = pd.concat([df_temperature_clean.reset_index(), 
        df_ghg_clean.loc['1990':'2010'].reset_index()], axis=1)
    df_merge = pd.DataFrame(df_merge_temp.iloc[:, [1, 2, 4]].values,
            index=df_merge_temp['index'],
            columns=['Land Average Temperature', 'Land And Ocean Temperature', 'Total GHG'])
    # 数据归一化处理
    df_merge_max_min = (df_merge - df_merge.min()) / (df_merge.max() - df_merge.min())
    
    # 绘图
    fig, axes = plt.subplots(nrows=2, ncols=2)

    ax1 = df_merge_max_min.plot(
            kind='line',
            figsize=(16, 9),
            ax=axes[0, 0],
            )
    ax1.set_xlabel('Years')
    ax1.set_ylabel('Values')

    ax2 = df_merge_max_min.plot(
            kind='bar',
            figsize=(16, 9),
            ax=axes[0, 1],
            )
    ax2.set_xlabel('Years')
    ax2.set_ylabel('Values')

    ax3 = df_temperature_resample_Q.plot(
            kind='area',
            figsize=(16, 9),
            ax=axes[1, 0],
            )
    ax3.set_xlabel('Quarters')
    ax3.set_ylabel('Temperature')

    ax4 = df_temperature_resample_Q.plot(
            kind='kde',
            figsize=(16, 9),
            ax=axes[1, 1],
            )
    ax4.set_xlabel('Values')
    ax4.set_ylabel('Values')

    plt.show()
    
    return fig


climate_plot()
