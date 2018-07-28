# -*- coding: utf-8 -*-
"""
    明确任务：
        1. 比较不同类别精灵属性值的分布
        2. 查看双变量数据分布
        3. 查看变量间的关系
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

datafile_path = './data/pokemon.csv'

output_path = './output'
if not os.path.exists(output_path):
    os.makedirs(output_path)


def collect_data():
    """
        数据获取
    """
    col = ['Name', 'Type_1', 'Total', 'HP', 'Attack', 'Defense', 'Speed', 'Height_m', 'Weight_kg', 'Catch_Rate']
    data_df = pd.read_csv(datafile_path, usecols=col)
    return data_df


def inspect_data(data_df):
    """
        查看数据
    """
    print('数据一共有{}行，{}列'.format(data_df.shape[0], data_df.shape[1]))

    print('数据预览：')
    print(data_df.head())

    print('数据基本信息：')
    print(data_df.info())

    print('数据统计信息：')
    print(data_df.describe())


def process_data(data_df):
    """
        数据处理
    """
    cln_data_df = data_df.dropna()
    print('原始数据有{}行记录，处理后的数据有{}记录'.format(data_df.shape[0], cln_data_df.shape[0]))

    return cln_data_df


def analyze_data(data_df, attr):
    """
        比较不同类别精灵属性值的分布
    """
    sns.boxplot(x='Type_1', y=attr, data=data_df)
    plt.show()


def analyze_dual_variables(data_df, var1, var2):
    """
        双变量数据分布
    """
    sns.jointplot(x=var1, y=var2, data=data_df)
    plt.show()


def analyze_variables_relationship(data_df):
    """
        可视化变量间的关系
    """
    corr_df = data_df.corr()
    sns.heatmap(corr_df, annot=True)
    plt.show()


def main():
    # 数据获取
    data_df = collect_data()

    # 查看数据基本信息
    inspect_data(data_df)

    # 数据处理
    proc_data_df = process_data(data_df)

    # 数据分析
    analyze_data(proc_data_df, 'HP')
    analyze_dual_variables(data_df, 'Attack', 'Defense')
    analyze_variables_relationship(proc_data_df)


if __name__ == '__main__':
    main()
