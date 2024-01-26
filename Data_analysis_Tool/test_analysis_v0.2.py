import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import shutil
import yaml


def read_config(file_path):
    with open(file_path, 'r') as file:
        config_data = yaml.safe_load(file)
    return config_data


def visualise_result1(df, columns, title, img_name):
    ax = df[columns].plot(kind='bar', figsize=(14, 8))
    ax.set_xticklabels(df.index, rotation=45, ha='right')  # 设置横坐标标签旋转
    ax.set_title(title)
    plt.savefig(img_name)


def visualise_result2(df, title, img_name):
    df.set_index('PN', inplace=True)
    df_transposed = df.T
    ax = df_transposed.plot(kind='bar', rot=0, figsize=(10, 6))
    ax.set_title(title)
    plt.savefig(img_name)


def filter_AllRun(config_data):
    """
    按条件筛选出所需Run
    """
    AllRun_file = config_data['AllRun_file']
    keyword_FileName = config_data['keyword_FileName']
    keyword_NP = config_data['keyword_NP']

    df_AllRun = pd.read_csv(AllRun_file, encoding='ANSI')
    df_matched = df_AllRun[df_AllRun['FileName'].str.contains(keyword_FileName)
                           & df_AllRun['NP'].apply(lambda x: any(item in x for item in keyword_NP))]
    df_matched.to_csv('Run_info.csv', index=False, encoding='ANSI')


def rename_Run():
    '''
    重命名Run文件
    '''
    Run_file_dir = './Run_file'
    for Run_file in os.listdir(Run_file_dir):
        Run_file_path = os.path.join(Run_file_dir, Run_file)
        df_Run_file = pd.read_csv(Run_file_path)
        NP = df_Run_file['NP'].values[0]
        re_NP = re.sub(r'[^\w-]', '-', NP)
        new_Run_file_path = f'./{re_NP}.csv'
        shutil.move(Run_file_path, new_Run_file_path)


def filter_config(data, keywords):
    '''
    :param data:
    :param keywords:
    :return:
    '''
    run_files = {key: value for key, value in data.items() if keywords in key}
    return run_files

def filter_Run(df):
    coverage_more_than_80 = df['coverage'] >= 0.8
    read_len_more_than_1000 = df['read_len'] >= 1000
    LT_more_than_30 = df['LT'] >= 1798
    df_more_than_c80_rl1000 = df[coverage_more_than_80 & read_len_more_than_1000]
    df_more_than_c80_LT30 = df[coverage_more_than_80 & LT_more_than_30]

    return df_more_than_c80_rl1000, df_more_than_c80_LT30


def get_prop(value, bins):
    cuts = pd.cut(value, bins)
    counts = cuts.value_counts().sort_index()
    prop = counts / len(value)

    return prop


def get_props(df_group):
    df_more_than_c80_rl1000, df_more_than_c80_LT30 = filter_Run(df_group)
    average_identity = df_more_than_c80_rl1000['average_identity']
    linker_speed = df_more_than_c80_LT30['linker_speed']
    read_len = df_more_than_c80_LT30['read_len']

    bins_identity = [0] + [i for i in range(75, 91)] + [100]
    prop_identity = get_prop(average_identity, bins_identity)

    bins_speed = [0] + np.arange(0.5, 3.75, 0.25).tolist()
    bins_speed.append(np.inf)
    prop_speed = get_prop(linker_speed, bins_speed)

    bins_read_len = np.arange(0, 12500, 500).tolist()
    bins_read_len.append(np.inf)
    prop_read_len = get_prop(read_len, bins_read_len)

    return prop_identity, prop_speed, prop_read_len


def analysis_Run(config_data):
    '''
    读取所需Run文件，按条件做处理
    '''
    df_run_file_dict = {}
    run_file_info = filter_config(config_data, 'Run_file_')
    for key, value in run_file_info.items():
        df_run_file = pd.read_csv(value)
        df_run_file_dict[key] = df_run_file

    df_group_dict = {}
    key_list = []
    group_info = filter_config(config_data, 'group_')
    for key, values in group_info.items():
        key_list.append(key)
        df_list = []
        for value in values:
            df = df_run_file_dict[value]
            df_list.append(df)
            df_group = pd.concat(df_list)
            df_group.reset_index(drop=True)
            df_group_dict[key] = df_group

    prop_identity_list = []
    prop_speed_list = []
    prop_read_len_list = []

    for key, value in df_group_dict.items():
        prop_identity, prop_speed, prop_read_len = get_props(value)
        prop_identity_list.append(prop_identity)
        prop_speed_list.append(prop_speed)
        prop_read_len_list.append(prop_read_len)

    PN = filter_config(config_data, 'PN_')
    columns_name = PN.values()

    df_identity = pd.concat(prop_identity_list, axis=1)
    df_identity.columns = columns_name
    df_identity.index = df_identity.index.map(lambda x: f'{x.left}-{x.right}')
    title = config_data['result_identity']
    visualise_result1(df_identity, columns_name, title, 'result_identity')

    df_speed = pd.concat(prop_speed_list, axis=1)
    df_speed.columns = columns_name
    df_speed.index = df_speed.index.map(lambda x: f'>{x.left:.2f}' if x.right == float('inf')
    else f'{x.left:.2f}-{x.right:.2f}')
    title = config_data['result_speed']
    visualise_result1(df_speed, columns_name, title, 'result_speed')

    df_read_len = pd.concat(prop_read_len_list, axis=1)
    df_read_len.columns = columns_name
    df_read_len.index = df_read_len.index.map(lambda x: f">{x.left / 1000:.1f}k" if x.right == float('inf')
    else f'{x.left / 1000:.1f}-{x.right / 1000:.1f}k')
    title = config_data['result_read_len']
    visualise_result1(df_read_len, columns_name, title, 'result_read_len')

    return df_run_file_dict, df_group_dict, columns_name


def get_result1():
    '''
    对照实验Run指标获取
    '''
    df_Run_info = pd.read_csv('Run_info.csv', encoding='ANSI')
    df_result1 = df_Run_info[['FileName', 'NP',
                              'total_avarage_identity', 'basecall_num', 'total_valid_reads_coverage',
                              'global_median_len', 'global_mean_len', 'average_linker_speed',
                              'ar_t_mean', 'ar_c_mean', 'ar_a_mean', 'ar_g_mean',
                              'dw_t_mean', 'dw_c_mean', 'dw_a_mean', 'dw_g_mean']]
    df_result1.columns = ['FileName', 'NP',
                          'identity', 'basecall_num', 'coverage',
                          'median_len', 'mean_len', 'linker_speed',
                          'ar_t', 'ar_c', 'ar_a', 'ar_g',
                          'dw_t', 'dw_c', 'dw_a', 'dw_g']
    decimal_places_dict = {'identity': 4, 'coverage': 4, 'linker_speed': 4}
    df_result1 = df_result1.apply(
        lambda col: col.round(decimal_places_dict[col.name]) if col.name in decimal_places_dict
        else col.round(0) if pd.api.types.is_numeric_dtype(col) else col)
    df_result1.to_csv('result1.csv', index=False)


def get_result2(config_data):
    _, df_group_dict, columns_name = analysis_Run(config_data)
    weighted_identity_list = []
    average_identity_list = []
    weighted_identity_filtered_list = []
    average_speed_list = []
    average_read_len_list = []
    for key, df in df_group_dict.items():
        df['mul'] = df['average_identity'].mul(df['sub_total_len'])
        weighted_identity = df['mul'].sum() / df['sub_total_len'].sum()
        weighted_identity_list.append(weighted_identity)
        df_more_than_c80_rl1000, df_more_than_c80_LT30 = filter_Run(df)
        identity_mean = df_more_than_c80_rl1000['average_identity'].mean()
        average_identity_list.append(identity_mean)
        weighted_identity_filtered = df_more_than_c80_rl1000['mul'].sum() / df_more_than_c80_rl1000[
            'sub_total_len'].sum()
        weighted_identity_filtered_list.append(weighted_identity_filtered)
        average_speed = df_more_than_c80_LT30['linker_speed'].mean()
        average_speed_list.append(average_speed)
        average_read_len = df_more_than_c80_LT30['read_len'].mean()
        average_read_len_list.append(average_read_len)

    data_result2 = {'酶': columns_name,
                    '未筛选-加权准确率': weighted_identity_list,
                    '平均准确率': average_identity_list,
                    '加权准确率': weighted_identity_filtered_list,
                    '平均速度': average_speed_list,
                    '平均读长': average_read_len_list
                    }
    df_result2 = pd.DataFrame(data_result2)
    df_result2.to_csv('result2.csv', index=False, encoding='ANSI')


# '''错误类型分析'''
def get_result3(config_data):
    df_compare_dict = {}
    compare_info = filter_config(config_data, 'compare_')
    df_run_file_dict = analysis_Run(config_data)[0]
    PN = filter_config(config_data, 'PN_')
    columns_name = PN.values()

    for key, values in compare_info.items():
        df_list = []
        for value in values:
            df = df_run_file_dict[value]
            df_list.append([value, df])
            df_compare_dict[key] = df_list

    df_error_list = []
    for key, df_list in df_compare_dict.items():
        data_error_list = []

        for value, df in df_list:
            df_more_than_c80_rl1000 = filter_Run(df)[0]
            substitution_rate = df_more_than_c80_rl1000['substitution_rate'].mean()
            insertion_rate = df_more_than_c80_rl1000['insertion_rate'].mean()
            deletion_rate = df_more_than_c80_rl1000['deletion_rate'].mean()
            homo_ins_1_rate = df_more_than_c80_rl1000['homo_ins_1_rate'].mean()

            data_error = {'条件': key,
                          'substitution': substitution_rate,
                          'insertion': insertion_rate,
                          'deletion': deletion_rate,
                          'homo_ins_1': homo_ins_1_rate
                          }
            data_error_list.append(data_error)
        df_error = pd.DataFrame(data_error_list)
        df_error_list.append(df_error)

    for df_error in df_error_list:
        filename = df_error['条件'][0]
        df_error = df_error.iloc[:, 1:]
        df_error['PN'] = columns_name
        title = f'{filename}: Error type statistics'
        visualise_result2(df_error, title, filename)
    df_result3 = pd.concat(df_error_list, ignore_index=False)
    df_result3.to_csv('result3.csv', encoding='ANSI', index=False)


def main():
    config_file_path = 'config.yaml'
    config_data = read_config(config_file_path)
    print('\n')
    print('1. 编辑config.yaml，按条件筛选所需要的Run\n')
    print('编辑完成后，按任意键继续')
    input()
    filter_AllRun(config_data)
    print('请核对Run_info.csv')
    input()
    print('2. 下载所需Run文件，将所有Run文件放入 Run_file 文件夹')
    input()
    print('------ 正在处理Run文件 ------\n')
    rename_Run()
    print('已重命名完成Run文件，请核对')
    input()
    print('3. 编辑config.yaml，修改各个分析指标')
    input()
    print('------ 正在生成分析结果 ------\n')
    analysis_Run(config_data)
    get_result1()
    get_result2(config_data)
    get_result3(config_data)
    print('分析结果已生成！\n')


if __name__ == '__main__':
    main()
