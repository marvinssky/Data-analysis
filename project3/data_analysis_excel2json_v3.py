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
datafile_path = './data/Gz.csv'

# 输出文件名
outputfile_name_Aim = 'Gz_Aim_v3.js'  # 目标楼盘输出文件名
outputfile_name_PutPos = 'Gz_PutPos_v3.js'  # 已签约楼盘输出文件名

# 输出路径
output_path = './output'
if not os.path.exists(output_path):
    os.makedirs(output_path)


def collect_data():
    """
        数据获取
    """
    # 这次需要读入的文件是以gbk格式编码的, keep_default_na=False 将空的字段读为""（不加该参数的话，pandas默认将空的内容读成nan）
    data_df = pd.read_csv(datafile_path, encoding='gbk', keep_default_na=False)

    return data_df


def process_data(data_df):
    """
        数据处理
    """
    droped_data_df = data_df.drop(['序号', '楼盘ID', '需解决的问题', '城市'], axis=1)

    # 将所有楼盘信息分成目标楼盘和已签约楼盘
    # 已经签约，已经安装，已入柜三种状态均算作已签楼盘
    Aim_data_df = droped_data_df[(droped_data_df['目前开发状态'] != '已经签约') & (droped_data_df['目前开发状态'] != '已经安装') & (droped_data_df['目前开发状态'] != '已入柜')]
    Aim_data_df = Aim_data_df.reset_index(drop=True)  # 重新设置行索引index，方便后面的loc操作
    # Aim_data_df.to_csv('test.csv', encoding='gbk')

    # 除以上三种状态外，均算作目标楼盘
    PutPos_data_df = droped_data_df[(droped_data_df['目前开发状态'] == '已经签约') | (droped_data_df['目前开发状态'] == '已经安装') | (droped_data_df['目前开发状态'] == '已入柜')]
    PutPos_data_df = PutPos_data_df.reset_index(drop=True)
    # print(Aim_data_df.count())
    # print(PutPos_data_df.count())

    # 创建空的DataFrame
    Aim_list_data_df = pd.DataFrame()  # 目标楼盘
    PutPos_list_data_df = pd.DataFrame()  # 已签楼盘

    # 目标楼盘信息处理
    # 把所有楼盘名称存储到name列下
    Aim_list_data_df['name'] = Aim_data_df['楼盘名称']
    PutPos_list_data_df['name'] = PutPos_data_df['楼盘名称']
    # print(Aim_list_data_df)
    '''
    Aim_list_data_df['value'] = '[' + droped_data_df['经纬度'].map(str) + ',' + '"' + droped_data_df['楼盘地址（到门牌号）'] \
                            + '"' + ',' + droped_data_df['入住户数'].map(str) + ',' + '"' + droped_data_df['物业名称'] \
                            + '"' + ',' + droped_data_df['预计投放点位数'].map(str) + ',' + \
                            droped_data_df['实际安装点位'].map(str) + ',' + droped_data_df['房价\n（元/m2）'].map(str) \
                            + ',' + droped_data_df['主力户型面积'].map(str) + ']'
    '''

    # 存放转换后的json数据，list格式
    Aim_list_json_df = []
    PutPos_list_json_df = []

    # 目标楼盘的json数据的value值
    for i in range(len(Aim_list_data_df)):
        list_value = []   # 存放每一行对应的value数组
        # print(i)
        try:
            # Aim_data_df.ilc[i, '经纬度'].replace("，", ",")
            # print(Aim_data_df.loc[i, '楼盘名称'])
            # print(Aim_data_df.loc[i, '经纬度'])
            list_value.append(float(Aim_data_df.loc[i, '经纬度'].split(',')[0]))
        except:
            list_value.append('')   # 如果将经度转化为float类型，并读入list_value的过程出错，则直接读入空字符串
            print('error_Aim->经度：line:{}->data:{}；已赋值空字符串'.format(i, Aim_data_df.loc[i, '经纬度']))  # 输出出错的行号和出错的原始数据
        try:
            # Aim_data_df.loc[i, '经纬度'].replace("，", ",")
            list_value.append(float(Aim_data_df.loc[i, '经纬度'].split(',')[1]))
        except:
            list_value.append('')
            print('error_Aim->纬度：line:{}->data:{}；已赋值空字符串'.format(i, Aim_data_df.loc[i, '经纬度']))
        try:
            list_value.append(float(Aim_data_df.loc[i, '房价\n（元/m2）']))
        except:
            # list_value.append(126238)   # 原数据中房价有两个值，转换为float失败，手动选择一个房价值读入
            # list_value.append(str(droped_data_df.loc[i, '房价\n（元/m2）'])) # 原数据中表述为"月租金..元"等，则以字符串格式读入
            print('error_Aim->房价（元/m2）line:{}->data:{}；需手动处理'.format(i, Aim_data_df.loc[i, '房价\n（元/m2）']))
        # 以字符串格式读入'楼盘地址（到门牌号）'的信息，若为空值nan，替换为''
        list_value.append(str(Aim_data_df.loc[i, '入住户数']).replace("nan", ""))
        list_value.append(str(Aim_data_df.loc[i, '物业名称']).replace("nan", ""))
        list_value.append("")  # '小区类型'用""代替
        list_value.append(str(Aim_data_df.loc[i, '主力户型面积']).replace("nan", ""))  # 主力户型面积
        list_value.append("4.0%")  # '容积率'用"4.0%"代替
        # list_value.append(str(Aim_data_df.loc[i, '预计投放点位数']).replace("nan", ""))
        # list_value.append(str(Aim_data_df.loc[i, '实际安装点位']).replace("nan", ""))

        # 将name和value信息保存到字典结构中
        dict_temp = {'name': Aim_list_data_df.loc[i, 'name'], 'value': list_value}
        # print(dict_temp)

        Aim_list_json_df.append(dict_temp)

    # 已签楼盘的json数据的value值
    for i in range(len(PutPos_list_data_df)):
        list_value = []   # 存放每一行对应的value数组

        try:
            # PutPos_data_df.loc[i, '经纬度'].replace("，", ",")
            list_value.append(float(PutPos_data_df.loc[i, '经纬度'].split(',')[0]))
        except:
            list_value.append('')   # 如果将经度转化为float类型，并读入list_value的过程出错，则直接读入空字符串
            print('error_PutPos->经度：line:{}->data:{}；已赋值空字符串'.format(i, PutPos_data_df.loc[i, '经纬度']))  # 输出出错的行号和出错的原始数据
        try:
            # PutPos_data_df.loc[i, '经纬度'].replace("，", ",")
            list_value.append(float(PutPos_data_df.loc[i, '经纬度'].split(',')[1]))
        except:
            list_value.append('')
            print('error_PutPos->纬度：line:{}->data:{}；已赋值空字符串'.format(i, PutPos_data_df.loc[i, '经纬度']))
        try:
            list_value.append(float(PutPos_data_df.loc[i, '房价\n（元/m2）']))
        except:
            # list_value.append(126238)   # 原数据中房价有两个值，转换为float失败，手动选择一个房价值读入
            # list_value.append(str(droped_data_df.loc[i, '房价\n（元/m2）'])) # 原数据中表述为"月租金..元"等，则以字符串格式读入
            # list_value.append('')
            print('error_PutPos->房价（元/m2）line:{}->data:{}；需手动处理'.format(i, PutPos_data_df.loc[i, '房价\n（元/m2）']))
        # 以字符串格式读入'楼盘地址（到门牌号）'的信息，若为空值nan，替换为''
        list_value.append(str(PutPos_data_df.loc[i, '入住户数']).replace("nan", ""))
        list_value.append(str(PutPos_data_df.loc[i, '物业名称']).replace("nan", ""))
        list_value.append("")  # '小区类型'用""代替
        list_value.append(str(PutPos_data_df.loc[i, '主力户型面积']).replace("nan", ""))  # 主力户型面积
        list_value.append("4.0%")  # '容积率'用"4.0%"代替

        # 将name和value信息保存到字典结构中
        dict_temp = {'name': PutPos_list_data_df.loc[i, 'name'], 'value': list_value}
        # print(dict_temp)

        PutPos_list_json_df.append(dict_temp)

    # print(len(Aim_list_json_df))

    # json_data_df = Aim_list_data_df.to_json(orient='records', force_ascii=False)

    # 将list结构转化为str，将所有的单引号替换为双引号
    proc_Aim_list_json_df = str(Aim_list_json_df).replace("'", "\"")
    proc_PutPos_list_json_df = str(PutPos_list_json_df).replace("'", "\"")

    return proc_Aim_list_json_df, proc_PutPos_list_json_df


def main():
    # 数据获取
    data_df = collect_data()
    # print(data_df)

    # 数据处理
    proc_Aim_list_json_df, proc_PutPos_list_json_df = process_data(data_df)
    # print(proc_data_df)

    # json_data_df = json.dumps(proc_data_df, ensure_ascii=False, indent=4)
    # print(json_data_df)

    # 写入文件
    with open(os.path.join(output_path, outputfile_name_Aim), 'w') as f:
        f.write(proc_Aim_list_json_df)

    with open(os.path.join(output_path, outputfile_name_PutPos), 'w') as f:
        f.write(proc_PutPos_list_json_df)


if __name__ == '__main__':
    main()
