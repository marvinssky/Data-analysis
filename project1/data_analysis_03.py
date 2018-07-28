# -*- coding: utf-8 -*-

"""
    明确任务：比较共享单车各用户类型(会员/非会员)比例
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
    member_type_list = []
    for data_filename in data_filenames:
        data_file = os.path.join(data_path, data_filename)
        data_arr = np.loadtxt(data_file, delimiter=',', dtype='str', skiprows=1)
        # 去掉双引号
        member_type_arr = np.core.defchararray.replace(data_arr[:, -1], '"', '')   # 当输入为一列时，转化后默认变为一行
        member_type_col = member_type_arr.reshape(-1, 1)

        member_type_list.append(member_type_col)

    year_member_type = np.concatenate(member_type_list)

    return year_member_type


def analyze_data(year_member_type):
    """
        Step 3: 数据分析
    """
    n_member = year_member_type[year_member_type == 'Member'].shape[0]
    n_casual = year_member_type[year_member_type == 'Casual'].shape[0]
    n_users = [n_member, n_casual]

    return n_users


def save_and_show_results(n_users):
    """
        Step 4：结果保存和展示
    """
    plt.figure()
    plt.pie(n_users, labels=['Member', 'Casual'], autopct='%.2f%%', shadow=True, explode=(0.05, 0))
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'piechart.png'))
    plt.show()


def main():

    year_member_type = collect_and_process_data()

    n_users = analyze_data(year_member_type)

    save_and_show_results(n_users)


if __name__ == '__main__':
    main()
