# -*- coding: utf-8 -*-
"""
    明确任务：
        按年度/地区分析全球心腹报告
"""
import os
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
    # 求出每年每各区域的Happiness Score的数据(一列Series)    层级索引
    year_region_grouped_result = data_df.groupby(by=['Year', 'Region'])['Happiness Score'].mean()

    year_region_pivot_result = pd.pivot_table(data_df, index='Region', columns='Year',
                                              values=['Happiness Score', 'Economy (GDP per Capita)'], aggfunc='mean')

    return year_region_grouped_result, year_region_pivot_result


def save_plot_results(year_region_grouped_result, year_region_pivot_result):
    """
        结果展示
    """
    year_region_grouped_result.to_csv(os.path.join(output_path, 'year_region_grouped_result.csv'))
    year_region_pivot_result.to_csv(os.path.join(output_path, 'year_region_pivot_result.csv'))

    year_region_pivot_result['Happiness Score'].plot(kind='bar', title='Happiness Score')
    plt.savefig(os.path.join(output_path, 'year_region_pivot_result_Happiness_Score.png'))
    plt.tight_layout()
    plt.show()

    year_region_pivot_result['Economy (GDP per Capita)'].plot(kind='bar', title='Economy (GDP per Capita)')
    plt.savefig(os.path.join(output_path, 'year_region_pivot_result_Economy_GDP_per_Capita.png'))
    plt.tight_layout()
    plt.show()


def main():
    # 数据获取
    data_df = collect_data()

    # 数据处理
    proc_data_df = process_data(data_df)

    # 数据分析
    year_region_grouped_result, year_region_pivot_result = analyze_data(proc_data_df)

    # 结果展示
    save_plot_results(year_region_grouped_result, year_region_pivot_result)


if __name__ == '__main__':
    main()
