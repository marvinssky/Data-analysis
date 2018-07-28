# -*- coding: utf-8 -*-

"""
    明确任务：比较共享单车每个季度的平均骑行时间
"""
import os
import numpy as np
import matplotlib.pyplot as plt


data_path = './data/bikeshare'
data_filenames = ['2017-q1_trip_history_data.csv', '2017-q2_trip_history_data.csv',
                  '2017-q3_trip_history_data.csv', '2017-q4_trip_history_data.csv']


def collect_data():
    """
        Step 1: 数据收集
    """
    data_arr_list = []
    for data_filename in data_filenames:
        data_file = os.path.join(data_path, data_filename)
        data_arr = np.loadtxt(data_file, delimiter=',', dtype='str', skiprows=1)
        data_arr_list.append(data_arr)

    return data_arr_list


def process_data(data_arr_list):
    """
        Step 2: 数据处理
    """
    duration_in_min_list = []
    for data_arr in data_arr_list:
        duration_str_col = data_arr[:, 0]
        # 去掉双引号
        duration_in_ms = np.core.defchararray.replace(duration_str_col, '"', '')
        # 类型转换
        duration_in_min = duration_in_ms.astype('float')/1000/60
        duration_in_min_list.append(duration_in_min)

    return duration_in_min_list


def analyze_data(duration_list):
    """
        Step 3: 数据分析
    """
    duration_mean_list = []
    for i, duration in enumerate(duration_list):
        duration_mean = np.mean(duration)
        print("第{}季度平均骑行时间：{:.2f}分钟".format(i+1, duration_mean))
        duration_mean_list.append(duration_mean)

    return duration_mean_list


def show_results(duration_mean_list):
    """
        Step 4: 结果展示
    """
    plt.figure()
    plt.bar(range(len(duration_mean_list)), duration_mean_list)
    plt.show()


def main():
    """
        主函数
    """
    # 数据处理
    data_arr_list = collect_data()

    # 数据处理
    duration_list = process_data(data_arr_list)

    # 数据分析
    duration_mean_list = analyze_data(duration_list)

    # 结果展示
    show_results(duration_mean_list)


if __name__ == '__main__':
    main()
