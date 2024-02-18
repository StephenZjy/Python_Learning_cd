import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib as mpl
import os
import shutil
import re
import csv
from scipy.stats import mode

from ConfigOperator import read_config, filter_config

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['font.size'] = 10


class RunOperator:
    def __init__(self):
        self.config_data = read_config('config.yaml')
        self.run_file_dir = './run_file'
        self.result_file_dir = './result'

        self.run_name = None
        self.run_file_dict = {}
        self.group_dict = {}
        self.condition_coverage_LT = None
        self.condition_coverage_read_len = None

        self.prop_identity_list = []
        self.prop_speed_list = []
        self.prop_read_len_list = []
        self.prop_error_type_list = []
        self.prop_ar_mean_list = []
        self.prop_dw_mean_list = []
        self.prop_cr_mean_list = []
        self.ISR_data_list = []
        self.df_pore_info_list = []

    def filter(self):
        self.config_data = read_config('config.yaml')
        AllRun_file = self.config_data['AllRun_file']
        keyword_FileName = self.config_data['keyword_FileName']
        keyword_NP = self.config_data['keyword_NP']

        df_AllRun = pd.read_csv(AllRun_file, encoding='ANSI')
        df_AllRun = df_AllRun[df_AllRun['FileName'].str.contains(keyword_FileName)
                              & df_AllRun['NP'].apply(lambda x: any(item in x for item in keyword_NP))]
        keyword_columns = self.config_data['keyword_columns']
        df_filtered = df_AllRun[keyword_columns]
        if not os.path.exists('run_info.csv'):
            df_filtered.to_csv('run_info.csv', encoding='ANSI', index=False)

    def rename(self):
        run_file_list = os.listdir(self.run_file_dir)
        for run_file in run_file_list:
            if run_file:
                run_file_path = os.path.join(self.run_file_dir, run_file)
                df_run_file = pd.read_csv(run_file_path, encoding='ANSI')
                NP = df_run_file['NP'].values[0]
                filename = re.sub(r'[^\w-]', '-', NP)
                new_run_file_path = f'{filename}.csv'
                if not os.path.exists(new_run_file_path):
                    shutil.copy(run_file_path, new_run_file_path)

    def slice(self):
        run_file_list = os.listdir(self.run_file_dir)
        df_run_file_list = []
        for run_file in run_file_list:
            run_file_path = os.path.join(self.run_file_dir, run_file)
            df_run_file = pd.read_csv(run_file_path, low_memory=False, encoding='ANSI')
            df_run_file_list.append(df_run_file)

        df_all = pd.concat(df_run_file_list)
        df_all.reset_index(drop=True, inplace=True)
        grouped = df_all.groupby('Barcode')
        for filename, df_group in grouped:
            if not os.path.exists(f'{filename}.csv'):
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

    def get_data(self):
        average_identity = self.condition_coverage_read_len['average_identity']
        linker_speed = self.condition_coverage_LT['linker_speed']
        read_len = self.condition_coverage_LT['read_len']
        ar_a = self.condition_coverage_LT['ar_a_mean']
        ar_t = self.condition_coverage_LT['ar_t_mean']
        ar_c = self.condition_coverage_LT['ar_c_mean']
        ar_g = self.condition_coverage_LT['ar_g_mean']
        ar_x_list = [ar_a, ar_t, ar_c, ar_g]
        ar_mean = self.condition_coverage_LT['ar_mean']
        dw_a = abs(self.condition_coverage_LT['dw_a_mean'])
        dw_t = abs(self.condition_coverage_LT['dw_t_mean'])
        dw_c = abs(self.condition_coverage_LT['dw_c_mean'])
        dw_g = abs(self.condition_coverage_LT['dw_g_mean'])
        dw_x_list = [dw_a, dw_t, dw_c, dw_g]
        dw_mean = abs(self.condition_coverage_LT['dw_mean'])
        cr_a = abs(self.condition_coverage_LT['cr_a_mean'])
        cr_t = abs(self.condition_coverage_LT['cr_t_mean'])
        cr_c = abs(self.condition_coverage_LT['cr_c_mean'])
        cr_g = abs(self.condition_coverage_LT['cr_g_mean'])
        cr_x_list = [cr_a, cr_t, cr_c, cr_g]
        cr_mean = abs(self.condition_coverage_LT['cr_mean'])
        pore_LT = self.condition_coverage_LT['LT'] / 60
        basecall_LT = self.condition_coverage_LT['basecall_life'] / 60
        sub_len = self.condition_coverage_read_len['sub_total_len']
        coverage = self.condition_coverage_LT['coverage']

        return locals()

    @staticmethod
    def get_bins_prop(value, bins):
        cuts = pd.cut(value, bins)
        counts = cuts.value_counts().sort_index()
        prop = counts / len(value)

        return prop

    def get_bins_props(self):
        data = self.get_data()
        bins_identity = np.concatenate(([0], np.arange(80, 90), [100]))
        prop_identity = self.get_bins_prop(data['average_identity'], bins_identity)

        bins_speed = np.concatenate(([0], np.arange(0.5, 3.75, 0.25)))
        bins_speed = np.append(bins_speed, np.inf)
        prop_speed = self.get_bins_prop(data['linker_speed'], bins_speed)

        bins_read_len = np.arange(0, 12500, 500)
        bins_read_len = np.append(bins_read_len, np.inf)
        prop_read_len = self.get_bins_prop(data['read_len'], bins_read_len)

        prop_ar_x_list = []
        for ar_x in data['ar_x_list']:
            bins_ar_x = np.concatenate(([0], np.arange(200, 1000, 100)))
            bins_ar_x = np.append(bins_ar_x, np.inf)
            prop_ar_x = self.get_bins_prop(ar_x, bins_ar_x)
            prop_ar_x_list.append(prop_ar_x)

        bins_ar_mean = np.concatenate(([0], np.arange(200, 1000, 100)))
        bins_ar_mean = np.append(bins_ar_mean, np.inf)
        prop_ar_mean = self.get_bins_prop(data['ar_mean'], bins_ar_mean)

        prop_dw_x_list = []
        for dw_x in data['dw_x_list']:
            bins_dw_x = np.concatenate(([0], np.arange(90, 135, 5)))
            bins_dw_x = np.append(bins_dw_x, np.inf)
            prop_dw_x = self.get_bins_prop(dw_x, bins_dw_x)
            prop_dw_x_list.append(prop_dw_x)

        bins_dw_mean = np.concatenate(([0], np.arange(90, 135, 5)))
        bins_dw_mean = np.append(bins_dw_mean, np.inf)
        prop_dw_mean = self.get_bins_prop(data['dw_mean'], bins_dw_mean)

        prop_cr_x_list = []
        for cr_x in data['cr_x_list']:
            bins_cr_x = np.concatenate(([0], np.arange(0.6, 1, 0.05)))
            bins_cr_x = np.append(bins_cr_x, np.inf)
            prop_cr_x = self.get_bins_prop(cr_x, bins_cr_x)
            prop_cr_x_list.append(prop_cr_x)

        bins_cr_mean = np.concatenate(([0], np.arange(0.6, 1, 0.05)))
        bins_cr_mean = np.append(bins_cr_mean, np.inf)
        prop_cr_mean = self.get_bins_prop(data['cr_mean'], bins_cr_mean)

        bins_pore_LT = np.arange(0, 65, 5)
        prop_pore_LT = self.get_bins_prop(data['pore_LT'], bins_pore_LT)

        bins_basecall_LT = np.arange(0, 65, 5)
        prop_basecall_LT = self.get_bins_prop(data['basecall_LT'], bins_basecall_LT)

        return (prop_identity, prop_speed, prop_read_len,
                prop_ar_x_list, prop_ar_mean, prop_dw_x_list, prop_dw_mean, prop_cr_x_list, prop_cr_mean,
                prop_pore_LT, prop_basecall_LT)

    def get_run_file_dict(self):
        self.config_data = read_config('config.yaml')
        run_file_info = filter_config(self.config_data, 'run_file_')
        for _, PN_file in run_file_info.items():
            if PN_file:
                PN = PN_file[0]
                df_run_file = pd.read_csv(PN_file[1], encoding='ANSI')
                if PN in self.run_file_dict:
                    self.run_file_dict[PN].append(df_run_file)
                    df_run_file_list = self.run_file_dict[PN]
                    df_run_file_concat = pd.concat(df_run_file_list)
                    self.run_file_dict[PN] = [df_run_file_concat]
                else:
                    self.run_file_dict[PN] = [df_run_file]

    def get_group_dict(self):
        group_info = filter_config(self.config_data, 'group_')
        for _, PN_list in group_info.items():
            if PN_list:
                label = PN_list[0]
                run_file_list = PN_list[1:]

                for run_file in run_file_list:
                    PN_file = self.config_data[run_file]
                    PN = PN_file[0]
                    df_run_file = pd.read_csv(PN_file[1], encoding='ANSI')
                    if label in self.group_dict:
                        self.group_dict[label].append([PN, df_run_file])
                    else:
                        self.group_dict[label] = [[PN, df_run_file]]

    def visualise_bar_prop(self, df, title, img_name):
        plt.clf()
        ax = df.plot(kind='bar', figsize=(12, 8))
        '''可更改尺寸'''
        ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.1%}'))
        ax.set_xticklabels(df.index, rotation=30, ha='right')
        ax.set_title(title)

        '''柱状图显示值'''
        # for p in ax.patches:
        #     ax.annotate(f'{p.get_height():.1%}', (p.get_x() + p.get_width() / 2., p.get_height()),
        #                 ha='center', va='center', xytext=(0, 10), textcoords='offset points')

        label = self.config_data['label']
        if label:
            label_dir = os.path.join(self.result_file_dir, label, 'imgs')
            os.makedirs(label_dir, exist_ok=True)
            plt.savefig(os.path.join(label_dir, img_name))
        else:
            img_dir = os.path.join(self.result_file_dir, 'imgs')
            os.makedirs(img_dir, exist_ok=True)
            img_path = os.path.join(img_dir, img_name)
            plt.savefig(img_path)
        print(img_name)
        plt.close()

    def visualise_scatter(self, df, x_column, y_column, x_lim, title, img_name):
        plt.figure(figsize=(12, 8))
        plt.scatter(df[x_column], df[y_column])

        mean_y = np.mean(df[y_column])
        weighted_mean_y = np.average(df[y_column], weights=df['sub_total_len'])  # Replace 'weights_column' with the actual column name
        mode_y = mode(df[y_column], axis=None, keepdims=True).mode[0]

        plt.axhline(weighted_mean_y, color='orange', linestyle='-.', linewidth=2, label=f'Weighted Mean Y: {weighted_mean_y:.2f}')
        plt.axhline(mean_y, color='r', linestyle='--', linewidth=2, label=f'Mean Y: {mean_y:.2f}')
        plt.axhline(mode_y, color='b', linestyle='--', linewidth=2, label=f'Mode Y: {mode_y:.2f}')

        # Plot mean of x-axis
        mean_x = np.mean(df[x_column])
        plt.axvline(mean_x, color='r', linestyle='--', linewidth=2, label=f'Mean X: {mean_x:.2f}')

        fontdict = {'fontsize': 12, 'fontweight': 'bold'}
        offset = 3
        plt.text(mean_x, mean_y, f'Mean = {mean_y:.2f}', color='r', fontdict=fontdict)
        plt.text(mean_x, weighted_mean_y - offset, f'Weighted Mean = {weighted_mean_y:.2f}', color='orange', fontdict=fontdict)
        plt.text(mean_x, mode_y + offset, f'Mode = {mode_y:.2f}', color='b', fontdict=fontdict)
        plt.text(mean_x, 0, f'{mean_x:.2f}', color='r', fontdict=fontdict)

        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.xlim(0, x_lim)
        plt.ylim(0, 100)
        plt.title(title)
        plt.grid(True)

        label = self.config_data['label']
        if label:
            label_dir = os.path.join(self.result_file_dir, label, 'imgs')
            os.makedirs(label_dir, exist_ok=True)
            plt.savefig(os.path.join(label_dir, img_name))
        else:
            img_dir = os.path.join(self.result_file_dir, 'imgs')
            os.makedirs(img_dir, exist_ok=True)
            img_path = os.path.join(img_dir, img_name)
            plt.savefig(img_path)
        print(img_name)

    def error_type_statistics(self, PN):
        error_type_dict = {}
        error_type_x_dict = {}
        error_type_list = ['substitution_rate', 'insertion_rate', 'deletion_rate']
        type_x = ['a', 't', 'c', 'g']

        for error_type in error_type_list:
            self.condition_coverage_read_len.loc[:, error_type] = (self.condition_coverage_read_len['read_len']
                                                                   * (self.condition_coverage_read_len[error_type])
                                                                   * 0.01)
            error_type_counts = self.condition_coverage_read_len[error_type].sum()
            error_type_counts = round(error_type_counts)
            total_read_len = self.condition_coverage_read_len['read_len'].sum()
            prop_error_type = error_type_counts / total_read_len
            prop_error_type = round(prop_error_type * 100, 2)
            error_type_dict[error_type] = [error_type_counts, prop_error_type]
            for x in type_x:
                error_type_x = f'{error_type}_{x}'
                self.condition_coverage_read_len.loc[:, error_type_x] = (self.condition_coverage_read_len['read_len']
                                                                         * (self.condition_coverage_read_len[error_type_x]
                                                                            * 0.01))
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
        csv_error_type_statistics = df_error_type_statistics
        csv_error_type_statistics.rename_axis('Base', inplace=True)
        csv_error_type_statistics = csv_error_type_statistics.applymap(lambda x: f'{x[0]}({x[1]}%)')
        label = self.config_data['label']
        if label:
            label_dir = os.path.join(self.result_file_dir, label, 'tables')
            os.makedirs(label_dir, exist_ok=True)
            csv_file_path = os.path.join(label_dir, f'error_type_statistics_{PN}.csv')
            csv_error_type_statistics.to_csv(csv_file_path)
            self.get_img_error_type_statistics(csv_file_path, PN)
        else:
            table_dir = os.path.join(self.result_file_dir, 'tables')
            os.makedirs(table_dir, exist_ok=True)
            csv_file_path = os.path.join(table_dir, f'error_type_statistics_{PN}.csv')
            csv_error_type_statistics.to_csv(csv_file_path)
            self.get_img_error_type_statistics(csv_file_path, PN)

        return df_error_type_statistics

    def analyze_proportion_single(self, PN):
        coverage = self.config_data['coverage']
        read_len = self.config_data['read_len']
        LT = self.config_data['LT']

        (prop_identity, prop_speed, prop_read_len,
         prop_ar_x_list, prop_ar_mean, prop_dw_x_list, prop_dw_mean, prop_cr_x_list, prop_cr_mean,
         prop_pore_LT, prop_basecall_LT) = self.get_bins_props()

        self.prop_identity_list.append(prop_identity)
        self.prop_speed_list.append(prop_speed)
        self.prop_read_len_list.append(prop_read_len)
        self.prop_ar_mean_list.append(prop_ar_mean)
        self.prop_dw_mean_list.append(prop_dw_mean)
        self.prop_cr_mean_list.append(prop_cr_mean)

        df_error_type_statistics = self.error_type_statistics(PN)
        df_error_type = df_error_type_statistics.applymap(lambda x: x[1] * 0.01)
        self.prop_error_type_list.append(df_error_type)

        '''
        单元素分析
        '''
        df_identity_single = pd.DataFrame(prop_identity)
        df_identity_single.columns = [PN]
        df_identity_single.index = df_identity_single.index.map(lambda x: f'{x.left}-{x.right}')
        title = f'Identity Distribution -coverage >{coverage}, read len >{read_len}'
        self.visualise_bar_prop(df_identity_single, title, f'proportion_identity_{PN}')

        df_speed_single = pd.DataFrame(prop_speed)
        df_speed_single.columns = [PN]
        df_speed_single.index = df_speed_single.index.map(lambda x: f'>{x.left:.2f}' if x.right == float('inf')
                                                          else f'{x.left:.2f}-{x.right:.2f}')
        title = f'Speed Distribution -coverage >{coverage}, LT >{LT}'
        self.visualise_bar_prop(df_speed_single, title, f'proportion_speed_{PN}')

        df_read_len_single = pd.DataFrame(prop_read_len)
        df_read_len_single.columns = [PN]
        df_read_len_single.index = df_read_len_single.index.map(lambda x: f">{x.left / 1000:.1f}k" if x.right == float('inf')
                                                                else f'{x.left / 1000:.1f}-{x.right / 1000:.1f}k')
        title = f'Read len Distribution -coverage >{coverage}, LT >{LT}'
        self.visualise_bar_prop(df_read_len_single, title, f'proportion_read_len_{PN}')

        self.visualise_bar_prop(df_error_type.iloc[0, :-1], 'total error type', f'total_error_type_{PN}')
        self.visualise_bar_prop(df_error_type.iloc[1:, -1], '4 base - error type', f'4_base_error_type_{PN}')
        self.visualise_bar_prop(df_error_type.iloc[1:, :-1].T, f'{PN} - 4 Base - Error type Statistics',
                                f'error_type_statistics_{PN}')

        prop_ar_mean.index = prop_ar_mean.index.map(lambda x: f'{x.left}-{x.right}')
        self.visualise_bar_prop(prop_ar_mean, 'AR prop', f'AR_prop_{PN}')
        df_ar_single = pd.concat(prop_ar_x_list, axis=1)
        df_ar_single.columns = ['A', 'T', 'C', 'G']
        df_ar_single.index = df_ar_single.index.map(lambda x: f'{x.left}-{x.right}')
        self.visualise_bar_prop(df_ar_single, f'{PN} - 4 Base - AR',
                                f'4_Base_AR_{PN}')

        prop_dw_mean.index = prop_dw_mean.index.map(lambda x: f'{x.left}-{x.right}')
        self.visualise_bar_prop(prop_dw_mean, 'DW prop', f'DW_prop_{PN}')
        df_dw_single = pd.concat(prop_dw_x_list, axis=1)
        df_dw_single.columns = ['A', 'T', 'C', 'G']
        df_dw_single.index = df_dw_single.index.map(lambda x: f'{x.left}-{x.right}')
        self.visualise_bar_prop(df_dw_single, f'{PN} - 4 Base - DW',
                                f'4_Base_DW_{PN}')

        prop_cr_mean.index = prop_cr_mean.index.map(lambda x: f'{x.left}-{x.right}')
        self.visualise_bar_prop(prop_cr_mean, 'CR prop', f'CR_prop_{PN}')
        df_cr_single = pd.concat(prop_cr_x_list, axis=1)
        df_cr_single.columns = ['A', 'T', 'C', 'G']
        df_cr_single.index = df_cr_single.index.map(lambda x: f'{x.left}-{x.right}')
        self.visualise_bar_prop(df_cr_single, f'{PN} - 4 Base - CR',
                                f'4_Base_CR_{PN}')

        df_LT = pd.concat([prop_pore_LT, prop_basecall_LT], axis=1)
        df_LT.columns = ['pore_LT', 'basecall_LT']
        df_LT.index = df_LT.index.map(lambda x: f'{x.left}-{x.right}')
        self.visualise_bar_prop(df_LT, f'{PN} -  Proportion of Pore_LT and Basecall_LT', f'Pore_LT-Basecall_LT_{PN}')

    def analyze_proportion_multiple(self, columns_name):
        coverage = self.config_data['coverage']
        read_len = self.config_data['read_len']
        LT = self.config_data['coverage']
        '''
        多元素分析
        '''
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

        df_type_error = pd.concat([prop_error_type.iloc[0] for prop_error_type in self.prop_error_type_list],
                                  axis=1)
        df_type_error.columns = columns_name
        df_total_error = df_type_error.tail(1)
        self.visualise_bar_prop(df_total_error, 'total error', 'total_error')
        self.visualise_bar_prop(df_type_error.iloc[:-1], 'total error type', 'total_error_type')

        df_type_error_x = pd.concat([prop_error_type['IDS_count'] for prop_error_type in self.prop_error_type_list],
                                    axis=1)
        df_type_error_x.columns = columns_name
        self.visualise_bar_prop(df_type_error_x.iloc[1:], '4 base - error type', '4_base_error_type')

        df_ar = pd.concat(self.prop_ar_mean_list, axis=1)
        df_ar.columns = columns_name
        self.visualise_bar_prop(df_ar, 'AR prop', 'AR_prop')

        df_dw = pd.concat(self.prop_dw_mean_list, axis=1)
        df_dw.columns = columns_name
        self.visualise_bar_prop(df_dw, 'DW prop', 'DW_prop')

        df_cr = pd.concat(self.prop_cr_mean_list, axis=1)
        df_cr.columns = columns_name
        self.visualise_bar_prop(df_cr, 'CR prop', 'CR_prop')

    def analyze_correlation(self, PN):
        read_len = 'read_len'
        average_identity = 'average_identity'
        x_lim = self.condition_coverage_read_len['read_len'].max()
        self.visualise_scatter(self.condition_coverage_read_len, read_len, average_identity, x_lim,
                               f'{PN} -  Scatter Plot for Correlation between Read length and Identity',
                               f'correlation_read_len_and_identity_{PN}')

    def analyze_variance(self, df):
        df = pd.read_csv(df)
        channel_counts = len(df['channel'])

    def get_table_identity_speed_readlen(self, PN):
        data = self.get_data()
        identity = data['average_identity']
        average_identity = identity.mean()
        sub_len = data['sub_len']
        weighted_identity = (identity.mul(sub_len)).sum() / (sub_len.sum())
        speed = data['linker_speed']
        average_speed = speed.mean()
        read_len = data['read_len']
        average_read_len = read_len.mean()

        coverage = data['coverage']
        average_coverage = coverage.mean()
        basecall_LT = data['basecall_LT']
        average_basecall_LT = basecall_LT.mean()
        num = len(identity)

        data_ISR = [PN, weighted_identity, num, average_read_len, average_coverage, average_speed, average_basecall_LT]
        label = self.config_data['label']
        header = ['PN', 'identity', 'num', 'average_read_len', 'coverage', 'speed', 'basecall_LT']
        if label:
            label_dir = os.path.join(self.result_file_dir, label, 'tables')
            os.makedirs(label_dir, exist_ok=True)
            table_ISR_path = os.path.join(label_dir, f'{label}_average_identity_speed_readlen.csv')
            if not os.path.exists(table_ISR_path):
                with open(table_ISR_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerow(data_ISR)
            else:
                with open(table_ISR_path, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(data_ISR)
        else:
            table_ISR_path = os.path.join(self.result_file_dir, 'tables', f'{label}_average_identity_speed_readlen.csv')
            if not os.path.exists(table_ISR_path):
                with open(table_ISR_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerow(data_ISR)
            else:
                with open(table_ISR_path, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(data_ISR)

    def visualise_table(self, df, df_name):
        plt.clf()
        plt.rcParams['font.sans-serif'] = ['SimHei']

        # 计算表格的大小，根据行数和列数来估计
        table_height = int(df.shape[0] * 0.5)  # 行数乘以一个估计的行高度
        table_width = int(df.shape[1] * 1)  # 列数乘以一个估计的列宽度

        fig, ax = plt.subplots(figsize=(min(10, table_width), min(8, table_height)))
        ax.axis('off')
        table_info = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center',
                                  colColours=['#f2f2f2'] * len(df.columns))

        # 调整表格布局
        table_info.auto_set_font_size(False)
        table_info.set_fontsize(10)
        table_info.auto_set_column_width(col=list(range(len(df.columns))))
        table_info.scale(1, 1.5)

        label = self.config_data['label']
        if label:
            label_dir = os.path.join(self.result_file_dir, label, 'imgs')
            os.makedirs(label_dir, exist_ok=True)
            plt.savefig(os.path.join(label_dir, f'table_{df_name}.png'), bbox_inches='tight', pad_inches=0.5)
        else:
            img_dir = os.path.join(self.result_file_dir, 'imgs')
            os.makedirs(img_dir, exist_ok=True)
            img_path = os.path.join(img_dir, f'table_{df_name}.png')
            plt.savefig(img_path, bbox_inches='tight', pad_inches=0.5)
        plt.close()

    def get_img_run_info(self):
        df_runs_info = pd.read_csv('run_info.csv', header=None, encoding='ANSI')
        df_runs_info = df_runs_info.transpose()
        self.visualise_table(df_runs_info, 'run_info')

        first_column = df_runs_info.iloc[:, 0]
        df_run_info_list = [pd.concat([first_column, df_runs_info[col]], axis=1)
                            for col in df_runs_info.iloc[:, 1:].columns]
        pore_info_list = []
        for df_run_info in df_run_info_list:
            self.run_name = df_run_info.iloc[0, 1]
            self.run_name = self.run_name.split('.')[0]
            df_run_info.columns = ['Key', 'Rate']
            df_pore_info = df_run_info.iloc[-4:]
            pore_info = df_pore_info.copy()
            pore_info.loc[:, 'Num'] = df_pore_info['Rate'].astype(float) * 524288
            run_info = df_run_info.iloc[:-4].reset_index(drop=True)
            self.visualise_table(pore_info, f'{self.run_name}_pore_info')
            self.visualise_table(run_info, f'{self.run_name}_run_info')

            pore_info_list.append(pore_info.iloc[:, 1:])

        column_pore = first_column[-4:]
        df_pore_info_list = pd.concat(pore_info_list, axis=1)
        df_pore_info_list.insert(0, 'Key', column_pore)
        self.visualise_table(df_pore_info_list, 'pore_info')

    def get_img_error_type_statistics(self, csv_file, PN):
        error_type_statistics = pd.read_csv(csv_file, encoding='ANSI')
        self.visualise_table(error_type_statistics, f'error_type_statistics_{PN}')
