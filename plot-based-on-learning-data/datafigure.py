import pandas as pd
import matplotlib.pyplot as plt



def data_plot():

    # 读取json数据
    df = pd.read_json('/home/shiyanlou/Code/user_study.json')
    # 获取重复的user_id数据，并算出各user_id对应的学习总时长
    datas = df.groupby('user_id').sum().head(100)
    
    # 绘制线型图
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title('StudyData')
    ax.set_xlabel('User ID')
    ax.set_ylabel('Study Time')
    ax.plot(datas.index, datas.minutes)
    plt.show()
    return ax


if __name__ == '__main__':
    data_plot()
