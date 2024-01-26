import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os
import shutil
import re

from ConfigOperator import read_config, filter_config


class RunOperator:
    def __init__(self):
        self.config_data = read_config('config.yaml')
        self.run_file_dir = './run_file'
        self.run_file_dict = {}
        self.group_dict = {}
        self.condition_coverage_LT = None
        self.condition_coverage_read_len = None
        self.prop_identity_list = []
        self.prop_speed_list = []
        self.prop_read_len_list = []

    def filter(self):
        AllRun_file = self.config_data['AllRun_file']
        keyword_FileName = self.config_data['keyword_FileName']
        keyword_NP = self.config_data['keyword_NP']
        keyword_columns = self.config_data['keyword_columns']

        df_AllRun = pd.read_csv(AllRun_file, encoding='ANSI')
        df_AllRun = df_AllRun[df_AllRun['FileName'].str.contains(keyword_FileName)
                              & df_AllRun['NP'].apply(lambda x: any(item in x for item in keyword_NP))]
        df_filtered = df_AllRun[keyword_columns]
        df_filtered.to_csv('run_info.csv', index=False, encoding='ANSI')

    def rename(self):
        run_file_list = os.listdir(self.run_file_dir)
        for run_file in run_file_list:
            run_file_path = os.path.join(self.run_file_dir, run_file)
            df_run_file = pd.read_csv(run_file_path)
            NP = df_run_file['NP'].values[0]
            filename = re.sub(r'[^\w-]', '-', NP)
            new_run_file_path = f'./{filename}.csv'
            shutil.move(run_file_path, new_run_file_path)

    def slice(self):
        run_file_list = os.listdir(self.run_file_dir)
        df_run_file_list = []
        for run_file in run_file_list:
            run_file_path = os.path.join(self.run_file_dir, run_file)
            df_run_file = pd.read_csv(run_file_path, encoding='ANSI', low_memory=False)
            df_run_file_list.append(df_run_file)

        df_all = pd.concat(df_run_file_list)
        df_all.reset_index(drop=True, inplace=True)
        grouped = df_all.groupby('Barcode')
        for filename, df_group in grouped:
            df_group.to_csv(f'{filename}.csv', index=False, encoding='ANSI')

    def set_filter_condition(self, df):
        coverage = self.config_data['coverage']
        coverage = float(coverage.rstrip('%')) / 100
        read_len = self.config_data['read_len']
        read_len = int(read_len.replace('K', '')) * 1000
        LT = self.config_data['LT']
        LT = int(LT.replace('min', '')) * 60 - 2

        condition_coverage = df['coverage'] >= coverage
        condition_read_len = df['read_len'] >= read_len
        condition_LT = df['LT'] >= LT
        self.condition_coverage_read_len = df[condition_coverage & condition_read_len]
        self.condition_coverage_LT = df[condition_coverage & condition_LT]

    @staticmethod
    def get_bins_prop(value, bins):
        cuts = pd.cut(value, bins)
        counts = cuts.value_counts().sort_index()
        prop = counts / len(value)

        return prop

    def get_bins_props(self):
        average_identity = self.condition_coverage_read_len['average_identity']
        linker_speed = self.condition_coverage_LT['linker_speed']
        read_len = self.condition_coverage_LT['read_len']

        '''
        可添加分析指标和更改bins_，调整可视化图片的横坐标间隔
        '''
        bins_identity = np.concatenate(([0], np.arange(75, 91), [100]))
        prop_identity = self.get_bins_prop(average_identity, bins_identity)

        bins_speed = np.array([0]) + np.arange(0.5, 3.75, 0.25)
        bins_speed = np.append(bins_speed, np.inf)
        prop_speed = self.get_bins_prop(linker_speed, bins_speed)

        bins_read_len = np.arange(0, 12500, 500)
        bins_read_len = np.append(bins_read_len, np.inf)
        prop_read_len = self.get_bins_prop(read_len, bins_read_len)

        return prop_identity, prop_speed, prop_read_len

    def get_run_file_dict(self):
        run_file_info = filter_config(self.config_data, 'run_file_')
        for _, PN_file in run_file_info.items():
            PN = PN_file[0]
            df_run_file = pd.read_csv(PN_file[1], encoding='ANSI')
            self.run_file_dict[PN] = df_run_file

    def get_group_dict(self):
        group_info = filter_config(self.config_data, 'group_')
        for group_id, PN_list in group_info.items():
            if PN_list:
                run_file_list = []
                for PN in PN_list:
                    run_file = self.run_file_dict[PN]
                    run_file_list.append(run_file)
                group = pd.concat(run_file_list)
                group.reset_index(drop=True, inplace=True)
                self.group_dict[group_id] = group

    @staticmethod
    def visualise_bar_prop(df, title, img_name):
        ax = df.plot(kind='bar', figsize=(12, 8))
        '''可更改尺寸'''
        ax.set_xticklabels(df.index, rotation=45, ha='right')
        ax.set_title(title)
        plt.savefig(img_name)

    @staticmethod
    def visualise_scatter(df, x_column, y_column, x_lim, title, img_name):
        plt.figure(figsize=(12, 8))
        plt.scatter(df[x_column], df[y_column])
        plt.title(title)
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.xlim(0, x_lim)
        plt.ylim(0, 100)
        plt.grid(True)
        plt.savefig(img_name)

    def analyze_prop(self, PN):
        PN_list = []
        PN_list.append(PN)

        coverage = self.config_data['coverage']
        read_len = self.config_data['read_len']
        LT = self.config_data['coverage']

        prop_identity, prop_speed, prop_read_len = self.get_bins_props()
        self.prop_identity_list.append(prop_identity)
        self.prop_speed_list.append(prop_speed)
        self.prop_read_len_list.append(prop_read_len)

        '''
        单元素分析
        '''
        df_identity_single = pd.DataFrame(prop_identity)
        df_identity_single.columns = [PN]
        df_identity_single.index = df_identity_single.index.map(lambda x: f'{x.left}-{x.right}')
        title = f'Identity Distribution -coverage >{coverage}, read len >{read_len}'
        self.visualise_bar_prop(df_identity_single, title, f'proportion_identity_{PN}')

        '''
        多元素分析
        '''
        columns_name = PN_list
        if len(columns_name) > 1:
            df_identity = pd.concat(self.prop_identity_list, axis=1)
            df_identity.columns = columns_name
            df_identity.index = df_identity.index.map(lambda x: f'{x.left}-{x.right}')
            title = f'Identity Distribution -coverage >{coverage}, read len >{read_len}'
            self.visualise_bar_prop(df_identity, title, 'proportion_identity')

            df_speed = pd.concat(self.prop_speed_list, axis=1)
            df_speed.columns = columns_name
            df_speed.index = df_speed.index.map(lambda x: f'>{x.left:.2f}' if x.right == float('inf')
            else f'{x.left:.2f}-{x.right:.2f}')
            title = f'Speed Distribution -coverage >{coverage}, LT >{LT}'
            self.visualise_bar_prop(df_speed, title, 'proportion_speed')

            df_read_len = pd.concat(self.prop_read_len_list, axis=1)
            df_read_len.columns = columns_name
            df_read_len.index = df_read_len.index.map(lambda x: f">{x.left / 1000:.1f}k" if x.right == float('inf')
            else f'{x.left / 1000:.1f}-{x.right / 1000:.1f}k')
            title = f'Read len Distribution -coverage >{coverage}, LT >{LT}'
            self.visualise_bar_prop(df_read_len, title, 'proportion_read_len')

    def analyze_corr(self):
        read_len = 'read_len'
        average_identity = 'average_identity'
        x_lim = self.condition_coverage_read_len['read_len'].max()
        self.visualise_scatter(self.condition_coverage_read_len, read_len, average_identity, x_lim,
                               '"Scatter Plot for Correlation between Read length and Identity',
                               'Correlation_read_len_and_identity')

    def error_type_statistics(self):
        error_type_dict = {}
        error_type_x_dict = {}
        error_type_list = ['substitution_rate', 'insertion_rate', 'deletion_rate']
        type_x = ['a', 't', 'c', 'g']

        for error_type in error_type_list:
            self.condition_coverage_read_len.loc[:, error_type] = (self.condition_coverage_read_len['read_len']
                                                                   * (
                                                                   self.condition_coverage_read_len[error_type]) * 0.01)
            error_type_counts = self.condition_coverage_read_len[error_type].sum()
            error_type_counts = round(error_type_counts)
            total_read_len = self.condition_coverage_read_len['read_len'].sum()
            prop_error_type = error_type_counts / total_read_len
            prop_error_type = round(prop_error_type * 100, 2)
            error_type_dict[error_type] = [error_type_counts, prop_error_type]
            for x in type_x:
                error_type_x = f'{error_type}_{x}'
                self.condition_coverage_read_len.loc[:, error_type_x] = (self.condition_coverage_read_len['read_len']
                                                                         * (self.condition_coverage_read_len[
                                                                                error_type_x] * 0.01))
                error_type_x_counts = self.condition_coverage_read_len[error_type_x].sum()
                error_type_x_counts = round(error_type_x_counts)
                prop_error_type_x = error_type_x_counts / total_read_len
                prop_error_type_x = round(prop_error_type_x * 100, 2)
                error_type_x_dict[error_type_x] = [error_type_x_counts, prop_error_type_x]

        df_error_type = pd.DataFrame([error_type_dict], index=['X'])
        df_error_type_x = pd.DataFrame([error_type_x_dict])
        indexes = ['A', 'T', 'C', 'G']
        new_df = pd.DataFrame(index=indexes, columns=error_type_list)
        for index in indexes:
            for error_type in error_type_list:
                new_df.loc[index, error_type] = df_error_type_x[f'{error_type}_{index.lower()}'].iloc[0]
        df_error_type_x = new_df
        df_error_type_statistics = pd.concat([df_error_type, df_error_type_x])

        df_error_type_statistics.columns = [error_type.split('_')[0].capitalize() for error_type in error_type_list]
        df_error_type_statistics['IDS_count'] = df_error_type_statistics.sum(axis=1)

        rows = df_error_type_statistics['IDS_count'].iloc[:]
        new_rows = []
        for row in rows:
            sum_counts = sum([row[i] for i in range(0, len(row), 2)])
            sum_prop = sum([row[i] for i in range(1, len(row), 2)])
            sum_prop = round(sum_prop, 2)
            row = [sum_counts, sum_prop]
            new_rows.append(row)
        df_error_type_statistics['IDS_count'] = new_rows

        print(df_error_type_statistics)




