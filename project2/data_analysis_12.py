# -*- coding: utf-8 -*-
"""
    明确任务：
        为幸福指数添加对应的等级
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


report_datafile_path = './data/happiness_report.csv'

output_path = './output'
if not os.path.exists(output_path):
    os.makedirs(output_path)


def collect_data():
    """
        数据获取
    """
    data_df = pd.read_csv(report_datafile_path)

    return data_df


def process_data(data_df):
    """
        数据处理
    """
    data_df.dropna(inplace=True)
    # 将数据先按Year从小到大排序，再按Happiness Score从大到小排序
    data_df.sort_values(['Year', 'Happiness Score'], ascending=[True, False], inplace=True)

    return data_df


def analyze_data(data_df):
    """
        数据分析
    """
    # apply()
    # def score2level(score_val):
    #    if score_val <= 3:
    #        level = 'Low'
    #    elif score_val <= 5:
    #        level = 'Middle'
    #    else:
    #        level = 'High'
    #
    #    return level
    #
    # data_df['level'] = data_df['Happiness Score'].apply(score2level)

    # cut()
    data_df['level'] = pd.cut(data_df['Happiness Score'], bins=[-np.inf, 3, 5, np.inf], labels=['Low', 'Middle', 'High'])

    region_year_label_df = pd.pivot_table(data_df, index='Region', columns=['Year', 'level'],
                                          values=['Country'], aggfunc='count')

    return region_year_label_df


def save_plot_results(region_year_level_df):
    """
        结果展示
    """
    region_year_level_df.to_csv(os.path.join(output_path, 'region_year_label_df.csv'))

    for year in [2015, 2016, 2017]:
        # 层级索引：'Country'列名下面的'2015'列
        region_year_level_df['Country', year].plot(kind='bar', stacked=True, title=year)
        plt.tight_layout()
        plt.savefig(os.path.join(output_path, '{}_level_stack.png'.format(year)))
        plt.show()


def main():
    # 数据获取
    data_df = collect_data()

    # 数据处理
    proc_data_df = process_data(data_df)

    # 数据分析
    region_year_level_df = analyze_data(proc_data_df)

    # 结果展示
    save_plot_results(region_year_level_df)


if __name__ == '__main__':
    main()
