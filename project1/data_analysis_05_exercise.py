# -*- coding: utf-8 -*-

"""
    明确任务：统计1-3月每月零上和零下气温天数的分组柱状图
"""
import os
import numpy as np
import matplotlib.pyplot as plt

# 解决matplotlib中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']

data_path = './data'
data_filename = 'temp.csv'

# 结果保存目录
output_path = './output'
if not os.path.exists(output_path):
    os.mkdir(output_path)


def collect_process_analyze():
    positive_temp_list = []
    negitive_temp_list = []

    month_list = ['1', '2', '3']

    data_file = os.path.join(data_path, data_filename)
    temp_data = np.loadtxt(data_file, delimiter=',', dtype='str', skiprows=1)

    for i in month_list:
        month_temp = temp_data[temp_data[:, 0] == i][:, 1]

        month_temp_arr = np.core.defchararray.replace(month_temp, ' C', '')
        month_temp_col = month_temp_arr.reshape(-1, 1).astype('float')

        positive_temp = month_temp_col[month_temp_col >= 0].shape[0]
        negitive_temp = month_temp_col[month_temp_col < 0].shape[0]

        positive_temp_list.append(positive_temp)
        negitive_temp_list.append(negitive_temp)

    return positive_temp_list, negitive_temp_list


def save_and_show_result(positive_temp_list, negitive_temp_list):
    bar_locs = np.arange(3)
    bar_width = 0.35
    xtick_label = ['第{}月份'.format(i+1) for i in range(3)]

    plt.figure()
    plt.bar(bar_locs, positive_temp_list, width=bar_width, color='g', alpha=0.7, label='零上气温')
    plt.bar(bar_locs + bar_width, negitive_temp_list, width=bar_width, color='r', alpha=0.7, label='零下气温')
    plt.ylabel('天数')
    plt.xticks(bar_locs+bar_width/2, xtick_label)
    plt.title('气温天数图')

    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'temp_group_chart.png'))
    plt.show()


def main():

    positive_temp_list, negitive_temp_list = collect_process_analyze()

    save_and_show_result(positive_temp_list, negitive_temp_list)


if __name__ == '__main__':
    main()
