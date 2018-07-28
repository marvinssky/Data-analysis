# -*- coding: utf-8 -*-
"""
    明确任务：
        分析不同操作系统手机每月流量使用情况
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

# 用户及其使用的手机数据文件
user_device_datafile_path = './data/mobile_data/user_device.csv'

# 用户及其套餐使用的数据文件
user_usage_datafile_path = './data/mobile_data/user_usage.csv'

output_path = './output'
if not os.path.exists(output_path):
    os.makedirs(output_path)


def collect_data():
    """
        数据获取
    """
    user_device_df = pd.read_csv(user_device_datafile_path)

    user_usage_df = pd.read_csv(user_usage_datafile_path)

    return user_device_df, user_usage_df


def process_data(user_device_df, user_usage_df):
    """
        数据处理
    """
    # 字符串合并
    user_device_df['platform_version'] = user_device_df['platform_version'].astype('str')
    # 字符串数据的向量操作
    user_device_df['system'] = user_device_df['platform'].str.cat(user_device_df['platform_version'], sep='_')

    # 合并数据集
    merged_df = pd.merge(user_device_df, user_usage_df, how='inner', on='user_id')

    return merged_df


def analyze_data(proc_data_df):
    """
        数据分析
    """
    system_usage_series = proc_data_df.groupby('system')['monthly_mb'].mean()
    # print(system_usage_series)
    system_usage_series.sort_values(ascending=False, inplace=True)
    return system_usage_series


def save_plot_results(system_usage_series):
    system_usage_series.to_csv(os.path.join(output_path, 'mobile_system_usage.csv'))

    system_usage_series.plot(kind='bar', rot=45)
    plt.ylabel('Monthly Usage (MB)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'mobile_system_usage.png'))
    plt.show()


def main():
    # 数据获取
    user_device_df, user_usage_df = collect_data()

    # 数据处理
    proc_data_df = process_data(user_device_df, user_usage_df)

    # 数据分析
    system_usage_series = analyze_data(proc_data_df)

    # 结果展示
    save_plot_results(system_usage_series)


if __name__ == '__main__':
    main()
