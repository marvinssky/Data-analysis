# -*- coding: utf-8 -*-

"""
    明确任务：比较共享单车各类用户的平均骑行时间趋势
"""
import os
import numpy as np
import matplotlib.pyplot as plt


data_path = './data/bikeshare'
data_filenames = ['2017-q1_trip_history_data.csv', '2017-q2_trip_history_data.csv',
                  '2017-q3_trip_history_data.csv', '2017-q4_trip_history_data.csv']


def collect_and_process_data():
    """
        Step 1+2: 数据获取，数据处理
    """
    cln_data_arr_list = []
    for data_filename in data_filenames:
        data_file = os.path.join(data_path, data_filename)
        data_arr = np.loadtxt(data_file, delimiter=',', dtype='str', skiprows=1)
        # 去掉双引号
        cln_data_arr = np.core.defchararray.replace(data_arr, '"', '')
        cln_data_arr_list.append(cln_data_arr)

    return cln_data_arr_list


def get_mean_duration_by_type(data_arr_list, member_type):
    """
        Step 3: 数据分析
    """
    mean_duration_list = []
    for data_arr in data_arr_list:
        bool_arr = data_arr[:, -1] == member_type
        filtered_arr = data_arr[bool_arr]
        mean_duration = np.mean(filtered_arr[:, 0].astype('float')/1000/60)
        mean_duration_list.append(mean_duration)

    return mean_duration_list


def save_and_show_results(member_mean_duration_list, casual_mean_duration_list):
    """
        Step 4：结果保存和展示
    """
    # 1.信息输出
    for idx in range(len(member_mean_duration_list)):
        member_mean_duration = member_mean_duration_list[idx]
        casual_mean_duration = casual_mean_duration_list[idx]
        print('第{}季度会员平均骑行时长{:.2f}分钟，非会员平均骑行市场{:.2f}分钟'.format(
            idx+1, member_mean_duration, casual_mean_duration))

    # 2.分析结果保存
    # 构造多维数组
    mean_duration_arr = np.array([member_mean_duration_list, casual_mean_duration_list]).transpose()
    np.savetxt('./mean_duration.csv', mean_duration_arr, delimiter=',',
               header='Member Mean Duration, Casual Mean Duration', fmt='%.4f',
               comments='')

    # 3. 可视化结果保存
    plt.figure()
    plt.plot(member_mean_duration_list, color='g', linestyle='-', marker='o', label='Member')
    plt.plot(casual_mean_duration_list, color='r', linestyle='--', marker='*', label='Casual')
    plt.title('Member VS Casual')
    plt.xticks(range(0, 4), ['1st', '2nd', '3rd', '4th'], rotation=45)
    plt.xlabel('Quarter')
    plt.ylabel('Mean duration (min)')
    plt.legend(loc='best')
    plt.tight_layout()

    plt.savefig('./duration_trend.png')
    plt.show()


def main():
    # 数据分析和数据处理
    cln_data_arr_list = collect_and_process_data()

    # 数据分析
    # 会员数据分析
    member_mean_duration_list = get_mean_duration_by_type(cln_data_arr_list, 'Member')
    # 非会员数据分析
    casual_mean_duration_list = get_mean_duration_by_type(cln_data_arr_list, 'Casual')

    save_and_show_results(member_mean_duration_list,  casual_mean_duration_list)


if __name__ == '__main__':
    main()
