from RunOperator import RunOperator


class DataAnalysis():
    def __init__(self):
        self.run_operation = RunOperator()

    def main(self):
        self.run_operation.get_run_file_dict()
        self.run_operation.get_group_dict()

        for PN, df_run_file in self.run_operation.run_file_dict.items():
            self.run_operation.set_filter_condition(df_run_file)
            # self.run_operation.analyze_prop(PN)
            # self.run_operation.analyze_corr()
            self.run_operation.error_type_statistics()


if __name__ == '__main__':
    data_analysis = DataAnalysis()
    data_analysis.main()
