# -*- coding: utf-8 -*-
"""
    明确任务：
        将excel数据转换为json(格式化输出json)
"""
import os
# import numpy as np
import pandas as pd
# import json

# 文件路径及名称
datafile_path = './data/Guiyang.csv'

# 输出文件名
outputfile_name = 'Guiyang_v2.js'

# 输出路径
output_path = './output'
if not os.path.exists(output_path):
    os.makedirs(output_path)


def collect_data():
    """
        数据获取
    """
    # 这次需要读入的文件是以gbk格式编码的
    data_df = pd.read_csv(datafile_path, encoding='gbk')

    return data_df


def process_data(data_df):
    """
        数据处理
    """
    droped_data_df = data_df.drop(['序号', '楼盘ID', '楼盘交付时间', '目前开发状态', '需解决的问题', '城市'], axis=1)

    # 创建空的DataFrame
    list_data_df = pd.DataFrame()

    # 把所有楼盘名称存储到name列下
    list_data_df['name'] = droped_data_df['楼盘名称']
    # print(list_data_df)
    '''
    list_data_df['value'] = '[' + droped_data_df['经纬度'].map(str) + ',' + '"' + droped_data_df['楼盘地址（到门牌号）'] \
                            + '"' + ',' + droped_data_df['入住户数'].map(str) + ',' + '"' + droped_data_df['物业名称'] \
                            + '"' + ',' + droped_data_df['预计投放点位数'].map(str) + ',' + \
                            droped_data_df['实际安装点位'].map(str) + ',' + droped_data_df['房价\n（元/m2）'].map(str) \
                            + ',' + droped_data_df['主力户型面积'].map(str) + ']'
    '''

    # 存放转换后的json数据，list格式
    list_json_df = []

    for i in range(len(list_data_df)):
        list_value = []   # 存放每一行对应的value数组

        try:
            list_value.append(float(droped_data_df.ix[i, '经纬度'].split(',')[1]))
        except:
            list_value.append('')   # 如果将经度转化为float类型，并读入list_value的过程出错，则直接读入空字符串
            print('error->经度：line:{}->data:{}；已赋值空字符串'.format(i, droped_data_df.ix[i, '经纬度']))  # 输出出错的行号和出错的原始数据
        try:
            list_value.append(float(droped_data_df.ix[i, '经纬度'].split(',')[0]))
        except:
            list_value.append('')
            print('error->纬度：line:{}->data:{}；已赋值空字符串'.format(i, droped_data_df.ix[i, '经纬度']))
        try:
            list_value.append(float(droped_data_df.ix[i, '房价\n（元/m2）']))
        except:
            # list_value.append(126238)   # 原数据中房价有两个值，转换为float失败，手动选择一个房价值读入
            # list_value.append(str(droped_data_df.ix[i, '房价\n（元/m2）'])) # 原数据中表述为"月租金..元"等，则以字符串格式读入
            print('error->房价（元/m2）line:{}->data:{}；需手动处理'.format(i, droped_data_df.ix[i, '房价\n（元/m2）']))
        # 以字符串格式读入'楼盘地址（到门牌号）'的信息，若为空值nan，替换为''
        list_value.append(str(droped_data_df.ix[i, '楼盘地址（到门牌号）']).replace("nan", ""))
        list_value.append(str(droped_data_df.ix[i, '入住户数']).replace("nan", ""))
        list_value.append(str(droped_data_df.ix[i, '物业名称']).replace("nan", ""))
        list_value.append(str(droped_data_df.ix[i, '预计投放点位数']).replace("nan", ""))
        list_value.append(str(droped_data_df.ix[i, '实际安装点位']).replace("nan", ""))
        list_value.append(str(droped_data_df.ix[i, '主力户型面积']).replace("nan", ""))

        # 将name和value信息保存到字典结构中
        dict_temp = {'name': list_data_df.ix[i, 'name'], 'value': list_value}
        # print(dict_temp)

        list_json_df.append(dict_temp)

    # print(len(list_json_df))

    # json_data_df = list_data_df.to_json(orient='records', force_ascii=False)

    # 将list结构转化为str，将所有的单引号替换为双引号
    proc_list_json_df = str(list_json_df).replace("'", "\"")

    return proc_list_json_df


def main():
    # 数据获取
    data_df = collect_data()
    # print(data_df)

    # 数据处理
    proc_data_df = process_data(data_df)
    # print(proc_data_df)

    # json_data_df = json.dumps(proc_data_df, ensure_ascii=False, indent=4)
    # print(json_data_df)

    # 写入文件
    with open(os.path.join(output_path, outputfile_name), 'w') as f:
        f.write(proc_data_df)


if __name__ == '__main__':
    main()
