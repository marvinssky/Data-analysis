# -*- coding: utf-8 -*-
"""
    明确任务：比较咖啡厅菜单各饮品类型的产品数量，平均热量
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

datafile_path = './data/coffee_menu.csv'

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


def analyze_data(data_df):
    beverage_category_col = data_df['Beverage_category']
    beverage_categories = beverage_category_col.unique()
    print('饮品类别：')
    print(beverage_categories)

    category_grouped = data_df.groupby('Beverage_category')
    category_count = category_grouped['Calories'].count()
    category_mean_calories = category_grouped['Calories'].mean()

    return category_count, category_mean_calories


def save_and_show_results(category_count, category_mean_calories):
    """
        结果展示
    """
    category_count.to_csv(os.path.join(output_path, 'category_count.csv'))
    category_mean_calories.to_csv(os.path.join(output_path, 'category_mean_calories.csv'))

    # print(category_mean_calories)
    category_mean_calories.plot(kind='bar')
    plt.title('Category Average Calories')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'category_average_calories.png'))
    plt.show()


def main():
    # 数据获取
    data_df = collect_data()

    # 查看数据基本信息
    inspect_data(data_df)

    # 数据分析
    category_count, category_mean_calories = analyze_data(data_df)

    # 结果展示
    save_and_show_results(category_count, category_mean_calories)


if __name__ == '__main__':
    main()