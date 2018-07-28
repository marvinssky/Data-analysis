# -*- coding: utf-8 -*-
"""
    明确任务：
        1. 2005-2017全球销量top20的游戏
        2. 2005-2017年各游戏生产商的销量对比，并使用堆叠柱状图进行可视化
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

datafile_path = './data/video_games_sales.csv'

output_path = './output'
if not os.path.exists(output_path):
    os.makedirs(output_path)


def collect_data():
    """
        数据获取
    """
    data_df = pd.read_csv(datafile_path)
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
    # 处理空值
    cln_data_df = data_df.dropna()

    # 按年份过滤
    cond = (cln_data_df['Year'] >= 2005) & (cln_data_df['Year'] <= 2007)
    cln_data_df1 = cln_data_df[cond]
    filtered_data_df = cln_data_df1.copy()   # 保证filtered_data_df上的操作不会影响到cln_data_df

    # 全球销量计算
    filtered_data_df['Global_Sales'] = filtered_data_df['NA_Sales'] + filtered_data_df['EU_Sales'] + \
                                       filtered_data_df['JP_Sales'] + filtered_data_df['Other_Sales']

    print('原始数据有{}行记录，处理后的数据有{}记录'.format(data_df.shape[0], filtered_data_df.shape[0]))

    return filtered_data_df


def analyze_data(data_df):
    """
        数据分析
    """
    top20_games = data_df.sort_values(by='Global_Sales', ascending=False).head(20)

    filter_data_df = data_df[data_df['Global_Sales'] > 5]
    sales_comp_results = filter_data_df.groupby('Publisher')[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()

    return top20_games, sales_comp_results


def save_and_show_results(top20_games, sales_comp_results):
    """
        结果展示
    """
    top20_games.to_csv(os.path.join(output_path, 'top20_games.csv'), index=False)
    sales_comp_results.to_csv(os.path.join(output_path, 'sales_comp_results.csv'))

    # print(top20_games)
    top20_games.plot(kind='bar', x='Name', y='Global_Sales')
    plt.title('Top 20 Games (2005 - 2017)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'top20_games.png'))

    sales_comp_results.plot.bar(stacked=True)
    plt.title('Games Sales Comparsion (2005 - 2017)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'Games Sales Comparsion.png'))
    plt.show()


def main():
    # 数据获取
    data_df = collect_data()

    # 查看数据基本信息
    inspect_data(data_df)

    # 数据处理
    proc_data_df = process_data(data_df)

    # 数据分析
    top20_games, sales_comp_results = analyze_data(proc_data_df)

    # 结果展示
    save_and_show_results(top20_games, sales_comp_results)


if __name__ == '__main__':
    main()