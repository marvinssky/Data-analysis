# -*- coding: utf-8 -*-
"""
    明确任务：
        将excel数据转换为json(输出的json为单行)
"""
import os
import numpy as np
import pandas as pd
import json


datafile_path = './data/BeijingTest.csv'
outputfile_name = 'BeijingTest.js'

output_path = './output'
if not os.path.exists(output_path):
    os.makedirs(output_path)


def collect_data():
    """
        数据获取
    """
    data_df = pd.read_csv(datafile_path, encoding='gbk')

    return data_df


def process_data(data_df):
    """
        数据处理
    """
    droped_data_df = data_df.drop(['序号', '楼盘ID', '楼盘交付时间', '目前开发状态', '需解决的问题', '城市'], axis=1)

    list_data_df = pd.DataFrame()
    list_data_df['name'] = droped_data_df['楼盘名称']
    list_data_df['value'] = '[' + droped_data_df['经纬度'].map(str) + ',' + droped_data_df['楼盘地址（到门牌号）'] + ',' + \
                            droped_data_df['入住户数'].map(str) + ',' + droped_data_df['物业名称'] + ',' + \
                            droped_data_df['预计投放点位数'].map(str) + ',' + droped_data_df['实际安装点位'].map(str) \
                            + ',' + droped_data_df['房价\n（元/m2）'].map(str) + ',' \
                            + droped_data_df['主力户型面积'].map(str) + ']'
    # print(list_data_df)
    json_data_df = list_data_df.to_json(orient='records', force_ascii=False)

    return json_data_df


def main():
    # 数据获取
    data_df = collect_data()
    # print(data_df)
    # 数据处理
    proc_data_df = process_data(data_df)
    # print(proc_data_df)

    # json_data_df = json.dumps(proc_data_df, ensure_ascii=False, indent=4)
    # json.dumps只可以将list类型转换为格式化的json显示，对str类型无法达到预期效果
    # print(json_data_df)

    with open(os.path.join(output_path, outputfile_name), 'w') as f:
        f.write(proc_data_df)

        # print(json.dumps(proc_data_df, ensure_ascii=False))


if __name__ == '__main__':
    main()
