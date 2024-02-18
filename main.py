from RunOperator import RunOperator
from ReportOperator import *


class DataAnalysis():
    def __init__(self):
        self.run_operation = RunOperator()
        self.PN_list = []
        self.run_name_list = []

    def main(self):
        analysis_file_type = self.run_operation.config_data['analysis_file_type']

        print('\n1. 编辑config.yaml，按条件筛选所需要的Run ---(输入pass，可跳过此步骤)')
        if input() != 'pass':
            print('编辑完成后，按任意键继续')
            input()
            self.run_operation.filter()
            print('请核对Run_info.csv')
            input()
            print('正在获取run_info......\n')
            self.run_operation.get_img_run_info()
        print('2. 下载所需Run文件，将所有Run文件放入 Run_file 文件夹 ---(输入pass，可跳过此步骤)')
        if input() != 'pass':
            print('正在处理Run文件......\n')
            if analysis_file_type == 'Barcode':
                self.run_operation.slice()
            else:
                self.run_operation.rename()
            print('已重命名完成Run文件，请核对')
            input()
        print('3. 编辑config.yaml，修改各个分析指标')
        input()
        print('正在生成分析结果......\n')

        self.run_operation.get_run_file_dict()
        label = self.run_operation.config_data['label']
        for PN, df_run_file in self.run_operation.run_file_dict.items():
            self.PN_list.append(PN)
            self.run_name_list.append(self.run_operation.run_name)

            self.run_operation.set_filter_condition(df_run_file[0])
            self.run_operation.analyze_proportion_single(PN)
            self.run_operation.analyze_correlation(PN)
            self.run_operation.get_table_identity_speed_readlen(PN)
            if analysis_file_type != 'Barcode':
                generate_single_run_md_file(label, PN, self.run_operation.run_name)
        columns_name = self.PN_list
        if len(columns_name) > 1:
            self.run_operation.analyze_proportion_multiple(columns_name)
        if len(self.run_operation.run_file_dict) > 1:
            self.run_name_list = list(set(self.run_name_list))
            generate_multiple_run_md_file(self.run_name_list, self.PN_list, label)

        print('分析结果已生成')
        input()


if __name__ == '__main__':
    data_analysis = DataAnalysis()
    data_analysis.main()
