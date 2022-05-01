# coding:utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def rosetype_pie(country, confirmed, size, colors):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示

    num = len(size)  # 柱子的数量
    width = 2 * np.pi / num  # 每个柱子的宽度
    rad = np.cumsum([width] * num)  # 每个柱子的角度

    plt.figure(figsize=(8, 8), dpi=500, )  # 创建画布
    ax = plt.subplot(projection='polar')
    ax.set_ylim(-1, np.ceil(max(size) + 1))  # 中间空白,-1为空白半径大小，可自行调整
    ax.set_theta_zero_location('N', -5.0)  # 设置极坐标的起点方向 W,N,E,S, -5.0为偏离数值，可自行调整
    ax.set_theta_direction(1)  # 1为逆时针，-1为顺时针
    ax.grid(False)  # 不显示极轴
    ax.spines['polar'].set_visible(False)  # 不显示极坐标最外的圆形
    ax.set_yticks([])  # 不显示坐标间隔
    ax.set_thetagrids([])  # 不显示极轴坐标

    ax.bar(rad, size, width=width, color=colors, alpha=1)  # 画图
    ax.bar(rad, 1, width=width, color='white', alpha=0.15)  # 中间添加白色色彩使图案变浅
    ax.bar(rad, 3, width=width, color='white', alpha=0.1)  # 中间添加白色色彩使图案变浅
    ax.bar(rad, 5, width=width, color='white', alpha=0.05)  # 中间添加白色色彩使图案变浅
    ax.bar(rad, 7, width=width, color='white', alpha=0.03)  # 中间添加白色色彩使图案变浅

    # 设置text
    for i in np.arange(num):
        if i < 8:
            ax.text(rad[i],  # 角度
                    size[i] - 0.2,  # 长度
                    country[i] + '\n' + str(confirmed[i]) + '例',  # 文本
                    rotation=rad[i] * 180 / np.pi - 5,  # 文字角度
                    rotation_mode='anchor',
                    # alpha=0.8,#透明度
                    fontstyle='normal',  # 设置字体类型，可选参数[ ‘normal’ | ‘italic’ | ‘oblique’ ]，italic斜体，oblique倾斜
                    fontweight='black',
                    # 设置字体粗细，可选参数 [‘light’, ‘normal’, ‘medium’, ‘semibold’, ‘bold’, ‘heavy’, ‘black’]
                    color='white',  # 设置字体颜色
                    size=size[i] / 2.2,  # 设置字体大小
                    ha="center",  # 'left','right','center'
                    va="top",  # 'top', 'bottom', 'center', 'baseline', 'center_baseline'
                    )
        elif i < 15:
            ax.text(rad[i] + 0.02,
                    size[i] - 0.7,
                    country[i] + '\n' + str(confirmed[i]) + '例',
                    fontstyle='normal',
                    fontweight='black',
                    color='white',
                    size=size[i] / 1.6,
                    ha="center",
                    )
        else:
            ax.text(rad[i],
                    size[i] + 0.1,
                    str(confirmed[i]) + '例 ' + country[i],
                    rotation=rad[i] * 180 / np.pi + 85,
                    rotation_mode='anchor',
                    fontstyle='normal',
                    fontweight='black',
                    color='black',
                    size=4,
                    ha="left",
                    va="bottom",
                    )

    plt.show()


if __name__ == '__main__':
    df = pd.read_csv('Wuhan-2019-nCoV.csv')  # 利用pandas读取数据
    colors = [(0.68359375, 0.02734375, 0.3203125),
              (0.78125, 0.05078125, 0.2578125),
              (0.875, 0.0390625, 0.1796875),
              (0.81640625, 0.06640625, 0.0625),
              (0.8515625, 0.1484375, 0.08203125),
              (0.90625, 0.203125, 0.13671875),
              (0.89453125, 0.2890625, 0.0703125),
              (0.84375, 0.2421875, 0.03125),
              (0.9140625, 0.26953125, 0.05078125),
              (0.85546875, 0.31640625, 0.125),
              (0.85546875, 0.3671875, 0.1171875),
              (0.94921875, 0.48046875, 0.28125),
              (0.9375, 0.51171875, 0.1484375),
              (0.93359375, 0.59765625, 0.0625),
              (0.93359375, 0.62890625, 0.14453125),
              (0.86328125, 0.5859375, 0.15234375),
              (0.86328125, 0.71875, 0.16015625),
              (0.86328125, 0.8203125, 0.16015625),
              (0.76171875, 0.8671875, 0.16015625),
              (0.53125, 0.85546875, 0.15625),
              (0.4765625, 0.94140625, 0.0703125),
              (0.21484375, 0.91015625, 0.0625),
              (0.15234375, 0.88671875, 0.08203125),
              (0.11328125, 0.87890625, 0.19921875),
              (0.11328125, 0.8125, 0.1796875),
              (0.1875, 0.76953125, 0.2109375),
              (0.2109375, 0.78125, 0.38671875),
              (0.1484375, 0.76953125, 0.30859375),
              (0.22265625, 0.73046875, 0.35546875),
              (0.2890625, 0.6875, 0.4765625)]  # 转化为小数的rgb色列表，
    df_top_confirmed = df.loc[(df['date'] == '2020-09-21') & (df['province'].isnull())].sort_values('confirmed',
                                                                                                    ascending=False).head(
        30)  # 选择9.21日确诊数前三十的国家
    country = df_top_confirmed['country'].tolist()
    confirmed = df_top_confirmed['confirmed'].tolist()
    size = [22, 19, 17, 12, 11, 10, 9, 8, 7.2, 7.0, 6.8, 6.6, 6.4, 6.2, 6.0, 5.8, 5.6, 5.4, 5.2, 5.0, 4.8, 4.6, 4.4,
            4.2, 4.0, 3.8, 3.6, 3.4, 3.2, 3.0]  # 自定义一个柱长度列
    rosetype_pie(country, confirmed, size, colors)
