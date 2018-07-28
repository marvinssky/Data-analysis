# -*- coding: utf-8 -*-

"""
    明确任务：统计共享单车不同用户类别(会员/非会员)骑行时间直方图
"""
import os
import numpy as np
import matplotlib.pyplot as plt


data_path = './data/bikeshare'
data_filenames = ['2017-q1_trip_history_data.csv', '2017-q2_trip_history_data.csv',
                  '2017-q3_trip_history_data.csv', '2017-q4_trip_history_data.csv']

# 结果保存目录
output_path = './output'
if not os.path.exists(output_path):
    os.mkdir(output_path)


def collect_and_process_data():
    """
        Step 1+2: 数据获取，数据处理
    """
    year_duration_member_type_list = []
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

        year_duration_member_type_list.append(duration_member_type_arr)

    year_duration_member_type = np.concatenate(year_duration_member_type_list, axis=0)

    member_arr = year_duration_member_type[year_duration_member_type[:, 1] == 'Member']
    casual_arr = year_duration_member_type[year_duration_member_type[:, 1] == 'Casual']
    # 这两行也可以写成以下形式：
    # member_arr = year_duration_member_type[year_duration_member_type[:, 1] == 'Member', :]   # 代表列全部索引，可以省略不写
    # casual_arr = year_duration_member_type[year_duration_member_type[:, 1] == 'Casual', :]

    year_member_duration = member_arr[:, 0].astype('float')/1000/60
    year_casual_duration = casual_arr[:, 0].astype('float') / 1000 / 60

    return year_member_duration, year_casual_duration


def analyze_data(year_member_duration, year_casual_duration):
    """
        Step 3: 数据分析
    """
    member_duration_histogram, member_bin_edge = np.histogram(year_member_duration, range=(0, 180), bins=12)
    casual_duration_histogram, casual_bin_edge = np.histogram(year_casual_duration, range=(0, 180), bins=12)
    print('会员直方图统计信息：{}，直方图分组边界：{}'.format(member_duration_histogram, member_bin_edge))
    print('非会员直方图统计信息：{}，直方图分组边界：{}'.format(casual_duration_histogram, casual_bin_edge))


def save_and_show_results(year_member_duration, year_casual_duration):
    """
        Step 4：结果展示
    """
    fig = plt.figure(figsize=(10, 5))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2, sharey=ax1)

    # 会员直方图
    ax1.hist(year_member_duration, range=(0, 180), bins=12)
    ax1.set_xticks(range(0, 181, 15))
    ax1.set_title('Member')
    ax1.set_ylabel('Count')
    ax1.set_xlabel('Time/min')

    # 非会员直方图
    ax2.hist(year_casual_duration, range=(0, 180), bins=12)
    ax2.set_xticks(range(0, 181, 15))
    ax2.set_title('Casual')
    ax2.set_ylabel('Count')
    ax2.set_xlabel('Time/min')

    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'type_histogram.png'))
    plt.show()


def main():

    # 数据获取，数据处理
    year_member_duration, year_casual_duration = collect_and_process_data()

    analyze_data(year_member_duration, year_casual_duration)

    save_and_show_results(year_member_duration, year_casual_duration)


if __name__ == '__main__':
    main()
