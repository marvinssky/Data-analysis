# -*- coding: utf-8 -*-

"""
    明确任务：统计共享单车各类用户的季度骑行时间的分组柱状图
"""
import os
import numpy as np
import matplotlib.pyplot as plt

# 解决matplotlib中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']

data_path = './data/bikeshare'
data_filenames = ['2017-q1_trip_history_data.csv', '2017-q2_trip_history_data.csv',
                  '2017-q3_trip_history_data.csv', '2017-q4_trip_history_data.csv']

# 结果保存目录
output_path = './output'
if not os.path.exists(output_path):
    os.mkdir(output_path)


def collect_process_analyze_data():
    """
        Step 1+2+3: 数据获取，数据处理，数据分析
    """
    member_mean_duration_list = []
    casual_mean_duration_list = []

    for data_filename in data_filenames:
        data_file = os.path.join(data_path, data_filename)
        data_arr = np.loadtxt(data_file, delimiter=',', dtype='str', skiprows=1)

        # 去掉双引号
        # 骑行时间
        duration_arr = np.core.defchararray.replace(data_arr[:, 0], '"', '')  # 当输入为一列时，转化后默认变为一行
        duration_col = duration_arr.reshape(-1, 1)
        # 用户类别
        member_type_arr = np.core.defchararray.replace(data_arr[:, -1], '"', '')   # 当输入为一列时，转化后默认变为一行
        member_type_col = member_type_arr.reshape(-1, 1)

        duration_member_type_arr = np.concatenate([duration_col, member_type_col], axis=1)

        # 会员平均骑行时间
        member_arr = duration_member_type_arr[duration_member_type_arr[:, 1] == 'Member']
        member_mean_duration = np.mean(member_arr[:, 0].astype('float') / 1000 / 60)
        member_mean_duration_list.append(member_mean_duration)
        # 非会员平均骑行时间
        casual_arr = duration_member_type_arr[duration_member_type_arr[:, 1] == 'Casual']
        casual_mean_duration = np.mean(casual_arr[:, 0].astype('float') / 1000 / 60)
        casual_mean_duration_list.append(casual_mean_duration)

    return member_mean_duration_list, casual_mean_duration_list


def save_and_show_results(member_mean_duration_list, casual_mean_duration_list):
    """
        Step 4：结果展示
    """
    bar_locs = np.arange(4)   # 分组：0，1，2，3
    bar_width = 0.35   # 柱子宽度
    xtick_labels = ['第{}季度'.format(i+1) for i in range(4)]    # 列表推导式

    plt.figure()
    plt.bar(bar_locs, member_mean_duration_list, width=bar_width, color='g', alpha=0.7, label='会员')
    plt.bar(bar_locs + bar_width, casual_mean_duration_list, width=bar_width, color='r', alpha=0.7, label='非会员')
    plt.xticks(bar_locs + bar_width/2, xtick_labels, rotation=45)
    plt.ylabel('平均骑行时间/min')
    plt.title('柱状图')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'group_bar_chart.png'))
    plt.show()


def main():

    # 数据获取，数据处理，数据分析
    member_mean_duration_list, casual_mean_duration_list = collect_process_analyze_data()

    save_and_show_results(member_mean_duration_list, casual_mean_duration_list)


if __name__ == '__main__':
    main()
