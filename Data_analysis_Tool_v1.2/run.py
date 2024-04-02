from UI_analysis import Ui_MainWindow
from PdfGenerator import generate_pdf_single_run, generate_pdf_multiple_run
from scipy.stats import mode
import numpy as np
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu, QTableWidgetItem, QGraphicsScene, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import logging
import os

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['font.size'] = 9


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUI()
        self.connectSignals()

    def initUI(self):
        self.initDefaults()
        self.initValueRanges()
        self.initLineEditDefaults()
        self.initVariables()
        self.initComboBoxes()
        self.initScenes()

    def initDefaults(self):
        self.columns_run_info = ['FileName', 'NP', 'Note', 'Buffer', 'trans', 'CYCLE', 'Voltage', 'Aperture',
                                 'total_avarage_identity', 'basecall_num', 'total_sub_len',
                                 'subs_more_than_80_pr', 'subs_more_than_83_pr', 'subs_more_than_85_pr',
                                 'subs_more_than_88_pr', 'subs_more_than_90_pr',
                                 'valid_reads_num', 'invalid_reads_num', 'total_matched_reads_num',
                                 'total_reads_len', 'total_valid_reads_len', 'total_valid_reads_coverage',
                                 'global_min_len', 'global_max_len', 'global_median_len', 'global_mean_len',
                                 'average_linker_speed', 'average_basecall_lifetime',
                                 'single_pore', 'multi_pore', 'suspected', 'appearance']
        self.default_values = ["average_identity", "read_len", "sub_total_len", "linker_speed", 'coverage',
                               "ar_mean", "dw_mean", "cr_mean", 'basecall_life', 'LT']
        self.ui.range_lineEdit.setText('0, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 100')
        self.value = 'average_identity'
        self.range = [0, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 100]
        self.value_x = 'average_identity'
        self.value_y = 'average_identity'

    def initValueRanges(self):
        self.value_range_dict = {
            'average_identity': [0, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 100],
            'read_len': [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, np.inf],
            'sub_total_len': [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, np.inf],
            'linker_speed': [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3.5, np.inf],
            'ar_mean': [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, np.inf],
            'dw_mean': [-1000, -150, -140, -130, -120, -110, -100, -90, -80, -70, -60, -50, 0],
            'cr_mean': [0, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99,
                        1],
            'coverage': [0, 0.65, 0.7, 0.75, 0.8, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 1],
            'basecall_life': [0, 300, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600],
            'LT': [0, 300, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600]
        }

        self.value_index_dict = {
            'average_identity': lambda x: f'{x.left}-{x.right}',
            'read_len': lambda x: f">{x.left / 1000:.1f}k" if x.right == float('inf')
            else f'{x.left / 1000:.1f}-{x.right / 1000:.1f}k',
            'sub_total_len': lambda x: f">{x.left / 1000:.1f}k" if x.right == float('inf')
            else f'{x.left / 1000:.1f}-{x.right / 1000:.1f}k',
            'linker_speed': lambda x: f'>{x.left:.2f}' if x.right == float('inf')
            else f'{x.left:.2f}-{x.right:.2f}',
            'ar_mean': lambda x: f'{x.left}-{x.right}',
            'dw_mean': lambda x: f'{x.left}~{x.right}',
            'cr_mean': lambda x: f'{x.left}-{x.right}',
            'coverage': lambda x: f'{x.left}-{x.right}',
            'basecall_life': lambda x: f'{x.left}-{x.right}',
            'LT': lambda x: f'{x.left}-{x.right}'
        }

    def initLineEditDefaults(self):
        self.coverage_low = 0
        self.coverage_high = float('inf')
        self.ui.coverage_lineEdit.setText('> 0')
        self.read_len_low = 0
        self.read_len_high = float('inf')
        self.ui.read_len_lineEdit.setText('> 0')
        self.LT_low = 0
        self.LT_high = float('inf')
        self.ui.LT_lineEdit.setText('> 0')
        self.identity_low = 0
        self.identity_high = float('inf')
        self.ui.identity_lineEdit.setText('> 0')


    def initVariables(self):
        self.is_display_value = True
        self.barcode_checkBox_state = False
        self.channel_file_list = None
        self.file_type = None
        self.channel_file = None
        self.summary_file = None
        self.fileName = None
        self.df_pore_info = None
        self.df_run_info = None
        self.df_channel_info = None
        self.df_channel_info_list = []
        self.label_info_dict = {}
        self.prop_list = []
        self.error_type_list = []
        self.base_error_list = []
        self.df_base_error_type_dict = {}
        self.csv_error_type_statistics_dict = {}
        self.original_df_channel_info = None
        self.df_prop = None
        self.df_base_error = None
        self.df_error_type = None
        self.df_base_error_type = None
        self.df_error_type_statistics = None
        self.csv_error_type_statistics = None

    def initComboBoxes(self):
        self.ui.value_comboBox.addItems(self.default_values)
        self.ui.value_comboBox.currentIndexChanged.connect(self.valueComboBoxIndexChanged)
        self.ui.valueX_comboBox.addItems(self.default_values)
        self.ui.valueX_comboBox.currentIndexChanged.connect(self.valueXYComboBoxIndexChanged)
        self.ui.valueY_comboBox.addItems(self.default_values)
        self.ui.valueY_comboBox.currentIndexChanged.connect(self.valueXYComboBoxIndexChanged)

    def initScenes(self):
        self.ui.checkBox.setChecked(True)
        self.ui.scrollAreaWidgetContents.setMinimumSize(1920, 1800)
        self.ui.value_comboBox.setEditable(False)
        self.ui.valueX_comboBox.setEditable(False)
        self.ui.valueY_comboBox.setEditable(False)
        self.ui.filename_comboBox.setEditable(False)
        self.ui.filename_comboBox_2.setEditable(False)

        self.prop_chart_scene = QGraphicsScene()
        self.error_type_chart_scene = QGraphicsScene()
        self.base_error_chart_scene = QGraphicsScene()
        self.base_error_type_chart_scene = QGraphicsScene()
        self.correlation_scatter_scene = QGraphicsScene()

    def connectSignals(self):
        self.ui.fileButton.clicked.connect(self.showFileMenu)
        self.ui.exportButton.clicked.connect(self.showExportMenu)
        self.ui.okpushButton.clicked.connect(self.okButtonClicked)
        self.ui.checkBox.stateChanged.connect(self.checkBoxStateChanged)

    def showFileMenu(self):
        options_menu = QMenu()
        import_summary_action = options_menu.addAction("导入Run汇总信息")
        import_channel_action = options_menu.addAction("导入Run通道信息")

        import_summary_action.triggered.connect(lambda: self.openFile(self.loadRunSummaryInfo, "summary"))
        import_channel_action.triggered.connect(lambda: self.openFile(self.loadRunChannelInfo, "channel"))

        options_menu.exec_(self.ui.fileButton.mapToGlobal(self.ui.fileButton.rect().bottomLeft()))

    def showExportMenu(self):
        options_menu = QMenu()
        import_single_action = options_menu.addAction("导出单个Run分析报告")
        import_barcode_action = options_menu.addAction("导出Barcode分析报告")
        import_multiple_action = options_menu.addAction("导出多个Run对比分析报告")

        
        import_single_action.triggered.connect(lambda: self.exportData(self.exportSingleRun))
        import_barcode_action.triggered.connect(lambda: self.exportData(self.exportBarcode))
        import_multiple_action.triggered.connect(lambda: self.exportData(self.exportMultipleRun))

        options_menu.exec_(self.ui.exportButton.mapToGlobal(self.ui.exportButton.rect().bottomLeft()))

    def openFile(self, load_function, file_type):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.file_type = file_type
        if self.file_type == "channel":
            self.channel_file_list, _ = QFileDialog.getOpenFileNames(None, "Open CSV File", "",
                                                                     "CSV Files (*.csv);;All Files (*)",
                                                                     options=options)
            if self.channel_file_list:
                load_function()
                if len(self.channel_file_list) > 1:
                    # 如果大于1，则将 self.ui.barcode_checkBox 设置为不可选中的状态
                    self.ui.barcode_checkBox.setEnabled(False)
                else:
                    # 如果不大于1，则将 self.ui.barcode_checkBox 设置为可选中的状态
                    self.ui.barcode_checkBox.setEnabled(True)
        else:
            self.summary_file, _ = QFileDialog.getOpenFileName(None, "Open CSV File", "",
                                                               "CSV Files (*.csv);;All Files (*)",
                                                               options=options)
            if self.summary_file:
                load_function()

    def loadRunSummaryInfo(self):
        try:
            df_run_info = pd.read_csv(self.summary_file, encoding='ANSI')
            df_run_info = df_run_info[self.columns_run_info]
            self.df_run_info = df_run_info.transpose().copy()
            self.displayRunSummaryInfo(self.df_run_info, self.ui.run_info_Widget)
            pore_info = self.df_run_info.iloc[-4:]
            self.df_pore_info = pore_info.copy()
            self.df_pore_info.loc['单孔信号良率'] = (
                    (self.df_pore_info.loc['appearance'] + self.df_pore_info.loc['suspected'])
                    / (self.df_pore_info.loc['appearance'] + self.df_pore_info.loc['suspected'] + self.df_pore_info.loc[
                'single_pore']))
            self.df_pore_info = self.df_pore_info.apply(pd.to_numeric, errors='coerce')
            for col in self.df_pore_info.columns:
                self.df_pore_info[f'Rate_{col}'] = (self.df_pore_info[col]).round(4)
                self.df_pore_info[f'Num_{col}'] = (self.df_pore_info[col][:-1].astype(float) * 524288).round(0)
                self.df_pore_info.loc['单孔信号良率', f'Num_{col}'] = '-'
                self.df_pore_info.drop(columns=[col], inplace=True)
            self.displayRunSummaryInfo(self.df_pore_info, self.ui.pore_info_Widget)

        except KeyError as e:
            self.showMessageBox(f"请核对所选项与导入文件类型是否一致！")
            logging.error(f"发生异常：{e}")

        except UnicodeDecodeError as e:
            self.showMessageBox(f"请检查文件的编码格式是否为ANSI！")
            logging.error(f"发生异常：{e}")

    @staticmethod
    def displayRunSummaryInfo(df, tableWidget):
        tableWidget.clear()

        tableWidget.setRowCount(df.shape[0] + 1)  # Increment row count to accommodate column names
        tableWidget.setColumnCount(df.shape[1] + 1)

        # Set the first row as column names
        for col_index, col_name in enumerate(df.columns):
            item = QTableWidgetItem(str(col_name))
            tableWidget.setItem(0, col_index + 1, item)

        for row_index, (index, row) in enumerate(df.iterrows()):
            item = QTableWidgetItem(str(index))
            tableWidget.setItem(row_index + 1, 0, item)

            for col_index, (col_name, value) in enumerate(row.items()):
                item = QTableWidgetItem(str(value))
                tableWidget.setItem(row_index + 1, col_index + 1, item)

        for col_index in range(df.shape[1] + 1):
            tableWidget.setColumnWidth(col_index, 200)

        font = QFont()
        font.setBold(True)
        for row_index in range(df.shape[0] + 1):
            item = tableWidget.item(row_index, 0)
            if item is not None:
                item.setFont(font)

        tableWidget.horizontalHeader().setVisible(False)
        tableWidget.verticalHeader().setVisible(False)
        # tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def loadRunChannelInfo(self):
        self.resetRunChannelInfo()
        self.prop_list = []
        self.error_type_list = []
        self.base_error_list = []
        self.df_base_error_type_dict = {}
        self.label_info_dict = {}

        export_message = QMessageBox(self)
        export_message.setWindowTitle("提示")
        export_message.setText("正在分析，请稍候...")
        export_message.show()
        QApplication.processEvents()

        if self.ui.barcode_checkBox.isChecked():
            self.barcode_checkBox_state = True
            df_channel_info = pd.read_csv(self.channel_file, encoding='ANSI')
            grouped = df_channel_info.groupby('Barcode')
            for barcode, df_group in grouped:
                if barcode != '-':
                    self.displayRunChannelInfo(barcode, df_group)
            export_message.close()

        else:
            self.barcode_checkBox_state = False
            for channel_file in self.channel_file_list:
                self.channel_file = channel_file
                df_channel_info = pd.read_csv(channel_file, encoding='ANSI')
                label = os.path.basename(channel_file).split('.')[0]
                self.displayRunChannelInfo(label, df_channel_info)
            export_message.close()

    def resetRunChannelInfo(self):
        # 在这里添加重置 loadRunChannelInfo 中所有绘图的逻辑
        # 例如，清除图形视图等
        self.ui.prop_chart_graphicsView.setScene(None)
        self.ui.base_error_type_graphicsView.setScene(None)
        self.ui.base_error_graphicsView.setScene(None)
        self.ui.error_type_graphicsView.setScene(None)
        self.ui.filename_comboBox.clear()
        self.ui.filename_comboBox_2.clear()

    def displayRunChannelInfo(self, label, df_channel_info):
        try:
            if label not in [self.ui.filename_comboBox.itemText(i) for i in
                             range(self.ui.filename_comboBox.count())]:
                self.ui.filename_comboBox.addItem(label)
                self.ui.filename_comboBox_2.addItem(label)
            df_channel_info_filtered = self.set_filter_condition(df_channel_info)
            self.label_info_dict[label] = df_channel_info_filtered

            self.display_value_prop(df_channel_info_filtered, label)
            self.display_error_statistics_prop(df_channel_info_filtered, label)
            self.display_scatter()

        except KeyError as e:
            self.showMessageBox(f"请核对所选项与导入文件类型是否一致！")
            logging.error(f"发生异常：{e}")

        except UnicodeDecodeError as e:
            self.showMessageBox(f"请检查文件的编码格式是否为ANSI")
            logging.error(f"发生异常：{e}")

    def display_value_prop(self, df_channel_info, label):
        prop = self.get_prop(df_channel_info, self.value, self.range).rename(label)
        self.prop_list.append(prop)
        self.df_prop = pd.concat(self.prop_list, axis=1)
        self.displayBarPlot(self.df_prop, self.prop_chart_scene, self.ui.prop_chart_graphicsView,
                                   is_value=True)

    def display_error_statistics_prop(self, df_channel_info, label):
        self.get_error_statistics(label, df_channel_info)

        error_type = self.df_error_type_statistics.iloc[0, :-1].rename(label)
        self.error_type_list.append(error_type)
        self.df_error_type = pd.concat(self.error_type_list, axis=1)
        self.displayBarPlot(self.df_error_type, self.error_type_chart_scene,
                                   self.ui.error_type_graphicsView)

        base_error = self.df_error_type_statistics.iloc[1:, -1].rename(label)
        self.base_error_list.append(base_error)
        self.df_base_error = pd.concat(self.base_error_list, axis=1)
        self.displayBarPlot(self.df_base_error, self.base_error_chart_scene,
                                   self.ui.base_error_graphicsView)

        self.df_base_error_type = self.df_error_type_statistics.iloc[1:, :-1].T
        self.df_base_error_type_dict[label] = self.df_base_error_type
        self.displayBarPlot(next(iter(self.df_base_error_type_dict.values())),
                                   self.base_error_type_chart_scene,
                                   self.ui.base_error_type_graphicsView)

        self.ui.filename_comboBox.currentIndexChanged.connect(self.filenameComboBoxIndexChanged)

    def display_scatter(self):
        self.displayScatterPlot(next(iter(self.label_info_dict.values())), self.value_x, self.value_y,
                                self.correlation_scatter_scene,
                                self.ui.correlation_scatter_graphicsView)

        self.ui.filename_comboBox_2.currentIndexChanged.connect(self.filenameComboBox2IndexChanged)

    def set_filter_condition(self, df_channel_info):
        condition_coverage = (df_channel_info['coverage'] >= self.coverage_low) & (
                    df_channel_info['coverage'] <= self.coverage_high)
        condition_read_len = (df_channel_info['read_len'] >= self.read_len_low) & (
                    df_channel_info['read_len'] <= self.read_len_high)
        condition_LT = (df_channel_info['LT'] >= self.LT_low) & (df_channel_info['LT'] <= self.LT_high)
        condition_identity = (df_channel_info['average_identity'] >= self.identity_low) & (
                    df_channel_info['average_identity'] <= self.identity_high)
        df_channel_info = df_channel_info[condition_coverage & condition_read_len & condition_LT & condition_identity]
        return df_channel_info

    def okButtonClicked(self):
        try:
            self.coverage_low, self.coverage_high = self.update_condition(self.ui.coverage_lineEdit)
            self.read_len_low, self.read_len_high = self.update_condition(self.ui.read_len_lineEdit)
            self.LT_low, self.LT_high = self.update_condition(self.ui.LT_lineEdit)
            self.identity_low, self.identity_high = self.update_condition(self.ui.identity_lineEdit)

            range_text = self.ui.range_lineEdit.text()
            if range_text:
                self.range = [float(val) for val in range_text.split(", ")]
                if self.value in self.value_range_dict:
                    self.value_range_dict[self.value] = self.range
            else:
                self.range = self.value_range_dict[self.value]

            # self.resetRunChannelInfo()
            self.prop_list = []
            self.error_type_list = []
            self.base_error_list = []
            self.df_base_error_type_dict = {}
            label_info_dict_copy = self.label_info_dict.copy()
            self.label_info_dict = {}

            current_barcode_checkBox_state = self.ui.barcode_checkBox.isChecked()
            if current_barcode_checkBox_state == self.barcode_checkBox_state:
                for label, df_channel_info in label_info_dict_copy.items():
                    self.displayRunChannelInfo(label, df_channel_info)
            else:
                self.loadRunChannelInfo()
                self.barcode_checkBox_state = current_barcode_checkBox_state

        except ValueError as e:
            self.showMessageBox(f"range中各元素的分隔符需为英文逗号加空格，例如：0, 1, 2")
            logging.error(f"发生异常：{e}")
        except Exception as e:
            self.showMessageBox(f"请导入文件！")
            logging.error(f"发生异常：{e}")

    @staticmethod
    def update_condition(condition):
        text = condition.text()

        if text and '>' not in text:
            low, high = map(float, text.split('-'))
            condition.setText(text)
        elif text and '>' in text:
            low = float(text.split('>')[1])
            high = float('inf')
        else:
            low = 0
            high = float('inf')
            condition.setText('> 0')

        return low, high

    def valueComboBoxIndexChanged(self):
        try:
            self.value = self.ui.value_comboBox.currentText()
            self.range = self.value_range_dict.get(self.value)
            range_text = ', '.join(map(str, self.range))
            self.ui.range_lineEdit.setText(range_text)
            # self.loadRunChannelInfo()

            self.prop_list = []
            for label, df_channel_info in self.label_info_dict.items():
                df_channel_info_filtered = self.set_filter_condition(df_channel_info)
                self.label_info_dict[label] = df_channel_info_filtered
                self.display_value_prop(df_channel_info_filtered, label)

        except Exception as e:
            self.showMessageBox(f"请导入文件！")
            logging.error(f"发生异常：{e}")

    def valueXYComboBoxIndexChanged(self):
        self.value_x = self.ui.valueX_comboBox.currentText()
        self.value_y = self.ui.valueY_comboBox.currentText()
        self.display_scatter()

    def filenameComboBoxIndexChanged(self):
        label = self.ui.filename_comboBox.currentText()
        df_base_error_type = self.df_base_error_type_dict.get(label)
        self.displayBarPlot(df_base_error_type, self.base_error_type_chart_scene,
                                   self.ui.base_error_type_graphicsView)

    def filenameComboBox2IndexChanged(self):
        label = self.ui.filename_comboBox_2.currentText()
        df_channel_info = self.label_info_dict.get(label)
        self.displayScatterPlot(df_channel_info, self.value_x, self.value_y, self.correlation_scatter_scene,
                                self.ui.correlation_scatter_graphicsView)

    def checkBoxStateChanged(self, state):
        if state == Qt.Checked:
            self.is_display_value = True
        else:
            self.is_display_value = False

    @staticmethod
    def get_prop(df, value, bins):
        cuts = pd.cut(df[value], bins)
        prop = cuts.value_counts(normalize=True).sort_index()

        return prop

    def get_df_prop(self, df):
        prop_ar_a = self.get_prop(df, 'ar_a_mean', self.value_range_dict['ar_mean'])
        prop_ar_t = self.get_prop(df, 'ar_t_mean', self.value_range_dict['ar_mean'])
        prop_ar_c = self.get_prop(df, 'ar_c_mean', self.value_range_dict['ar_mean'])
        prop_ar_g = self.get_prop(df, 'ar_g_mean', self.value_range_dict['ar_mean'])
        prop_ar_x_list = [prop_ar_a, prop_ar_t, prop_ar_c, prop_ar_g]
        df_prop_ar = pd.concat(prop_ar_x_list, axis=1)
        df_prop_ar.index = df_prop_ar.index.map(lambda x: f'{x.left}-{x.right}')
        df_prop_ar.columns = ['A', 'T', 'C', 'G']

        prop_dw_a = self.get_prop(df, 'dw_a_mean', self.value_range_dict['dw_mean'])
        prop_dw_t = self.get_prop(df, 'dw_t_mean', self.value_range_dict['dw_mean'])
        prop_dw_c = self.get_prop(df, 'dw_c_mean', self.value_range_dict['dw_mean'])
        prop_dw_g = self.get_prop(df, 'dw_g_mean', self.value_range_dict['dw_mean'])
        prop_dw_x_list = [prop_dw_a, prop_dw_t, prop_dw_c, prop_dw_g]
        df_prop_dw = pd.concat(prop_dw_x_list, axis=1)
        df_prop_dw.index = df_prop_dw.index.map(lambda x: f'{x.left}-{x.right}')
        df_prop_dw.columns = ['A', 'T', 'C', 'G']

        prop_cr_a = self.get_prop(df, 'cr_a_mean', self.value_range_dict['cr_mean'])
        prop_cr_t = self.get_prop(df, 'cr_t_mean', self.value_range_dict['cr_mean'])
        prop_cr_c = self.get_prop(df, 'cr_c_mean', self.value_range_dict['cr_mean'])
        prop_cr_g = self.get_prop(df, 'cr_g_mean', self.value_range_dict['cr_mean'])
        prop_cr_x_list = [prop_cr_a, prop_cr_t, prop_cr_c, prop_cr_g]
        df_prop_cr = pd.concat(prop_cr_x_list, axis=1)
        df_prop_cr.index = df_prop_cr.index.map(lambda x: f'{x.left}-{x.right}')
        df_prop_cr.columns = ['A', 'T', 'C', 'G']

        prop_pore_LT = self.get_prop(df, 'LT', self.value_range_dict['LT'])
        prop_basecall_LT = self.get_prop(df, 'basecall_life', self.value_range_dict['basecall_life'])
        df_prop_LT = pd.concat([prop_pore_LT, prop_basecall_LT], axis=1)
        df_prop_LT.index = df_prop_LT.index.map(lambda x: f'{x.left}-{x.right}')
        df_prop_LT.columns = ['pore_LT', 'basecall_LT']

        return df_prop_ar, df_prop_dw, df_prop_cr, df_prop_LT

    def get_error_statistics(self, label, df_channel_info):
        error_type_dict = {}
        error_type_x_dict = {}
        error_type_list = ['substitution_rate', 'insertion_rate', 'deletion_rate']
        type_x = ['a', 't', 'c', 'g']
        df_channel_info_copy = df_channel_info.copy()
        for error_type in error_type_list:
            df_channel_info_copy.loc[:, error_type] = (df_channel_info_copy['read_len']
                                                  * (df_channel_info_copy[error_type])
                                                  * 0.01)
            error_type_counts = df_channel_info_copy[error_type].sum()
            error_type_counts = round(error_type_counts)
            total_read_len = df_channel_info_copy['read_len'].sum()
            prop_error_type = error_type_counts / total_read_len if total_read_len != 0 else 0.0
            prop_error_type = round(prop_error_type * 100, 2)
            error_type_dict[error_type] = [error_type_counts, prop_error_type]

            for x in type_x:
                error_type_x = f'{error_type}_{x}'
                df_channel_info_copy.loc[:, error_type_x] = (df_channel_info_copy['read_len']
                                                        * (df_channel_info_copy[
                                                               error_type_x]
                                                           * 0.01))
                error_type_x_counts = df_channel_info_copy[error_type_x].sum()
                prop_error_type_x = error_type_x_counts / total_read_len if total_read_len != 0 else 0.0
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

        self.df_error_type_statistics = df_error_type_statistics.applymap(lambda x: x[1] * 0.01)
        csv_error_type_statistics = df_error_type_statistics
        csv_error_type_statistics.rename_axis('Base', inplace=True)
        self.csv_error_type_statistics = csv_error_type_statistics.applymap(lambda x: f'{int(x[0])} ({x[1]}%)')
        self.csv_error_type_statistics_dict[label] = self.csv_error_type_statistics

    def displayBarPlot(self, value, scene, graphicsView, is_value=False):
        scene.clear()
        plt.clf()

        if value is None:
            # Display an empty graph
            pixmap = QtGui.QPixmap()  # Create an empty pixmap
            scene.addPixmap(pixmap)
            graphicsView.setScene(scene)
            return

        view_size = graphicsView.size()
        view_width = view_size.width() / 100 - 0.05
        view_height = view_size.height() / 100 - 0.19

        fig, ax = plt.subplots(figsize=(view_width, view_height))
        ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.1%}'))
        if is_value:
            value.index = value.index.map(self.value_index_dict[self.value])
        # value.index = value.index.map(lambda x: f'{x.left}-{x.right}')
        ax = value.plot(kind='bar', figsize=(view_width, view_height), ax=ax, rot=0)
        ax.set_xticklabels(value.index)
        ax.set_xlabel('')  # 不显示横坐标下方的轴名称

        if self.is_display_value:
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.1%}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', xytext=(3, 3), textcoords='offset points')

        # 将 Matplotlib 图表转换为 QPixmap
        canvas = fig.canvas
        canvas.draw()
        width, height = canvas.get_width_height()
        pixmap = QtGui.QPixmap.fromImage(
            QtGui.QImage(canvas.buffer_rgba(), width, height, QtGui.QImage.Format_RGBA8888))
        plt.close(fig)
        scene.addPixmap(pixmap)
        graphicsView.setScene(scene)

    def displayScatterPlot(self, df, x_column, y_column, scene, graphicsView):
        scene.clear()
        plt.clf()

        if df is None:
            # Display an empty graph
            pixmap = QtGui.QPixmap()  # Create an empty pixmap
            scene.addPixmap(pixmap)
            graphicsView.setScene(scene)
            return

        view_size = graphicsView.size()
        view_width = view_size.width() / 100 - 0.05
        view_height = view_size.height() / 100 - 0.19

        fig, ax = plt.subplots(figsize=(view_width, view_height))
        plt.scatter(df[x_column], df[y_column], s=9)
        if self.is_display_value:
            mean_y = np.mean(df[y_column])
            weighted_mean_y = np.average(df[y_column], weights=df[
                'sub_total_len'])  # Replace 'weights_column' with the actual column name
            mode_y = mode(df[y_column], axis=None, keepdims=True).mode[0]

            plt.axhline(weighted_mean_y, color='orange', linestyle='-.', linewidth=1,
                        label=f'Weighted Mean Y: {weighted_mean_y:.2f}')
            plt.axhline(mean_y, color='r', linestyle='--', linewidth=1, label=f'Mean Y: {mean_y:.2f}')
            plt.axhline(mode_y, color='b', linestyle='--', linewidth=1, label=f'Mode Y: {mode_y:.2f}')

            # Plot mean of x-axis
            mean_x = np.mean(df[x_column])
            plt.axvline(mean_x, color='r', linestyle='--', linewidth=1, label=f'Mean X: {mean_x:.2f}')

            fontdict = {'fontsize': 9, 'fontweight': 'bold'}
            offset = 8
            plt.text(mean_x, mean_y, f'Mean = {mean_y:.2f}', color='r', fontdict=fontdict)
            plt.text(mean_x, weighted_mean_y - offset, f'Weighted Mean = {weighted_mean_y:.2f}', color='orange',
                     fontdict=fontdict)
            plt.text(mean_x, mode_y + offset, f'Mode = {mode_y:.2f}', color='b', fontdict=fontdict)
            plt.text(mean_x, 0, f'{mean_x:.2f}', color='r', fontdict=fontdict)

        # plt.xlabel(x_column, fontsize=9)
        # plt.ylabel(y_column, fontsize=9)
        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9)
        plt.grid(True)
        x_lim = df[x_column].max()
        if x_lim < 0:
            x_lim = df[x_column].min()
        y_lim = df[y_column].max()
        if y_lim < 0:
            y_lim = df[y_column].min()
        plt.xlim(0, x_lim)
        plt.ylim(0, y_lim)

        canvas = fig.canvas
        canvas.draw()
        width, height = canvas.get_width_height()
        pixmap = QtGui.QPixmap.fromImage(
            QtGui.QImage(canvas.buffer_rgba(), width, height, QtGui.QImage.Format_RGBA8888))
        plt.close(fig)
        scene.addPixmap(pixmap)
        graphicsView.setScene(scene)

    def exportData(self, export_function):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", "", options=options)
        if directory:
            try:
                export_function(directory)
            except Exception as e:
                self.showMessageBox(f"Error exporting data: {str(e)}")

    def exportSingleRun(self, directory):
        if self.ui.barcode_checkBox.isChecked():
            self.showMessageBox('请关闭barcode选项！')
        else:
            export_message = QMessageBox(self)
            export_message.setWindowTitle("提示")
            export_message.setText("正在导出，请稍候...")
            export_message.show()
            QApplication.processEvents()  # 刷新UI以确保消息窗口显示

            label, df_channel_info = next(iter(self.label_info_dict.items()))
            img_path = directory + f'/imgs_{label}'
            if not os.path.exists(img_path):
                os.mkdir(img_path)

            if self.df_run_info is not None:
                self.visualise_table(self.df_run_info, img_path + '/run_info')
                self.visualise_table(self.df_pore_info, img_path + '/pore_info')

            for value, value_range in self.value_range_dict.items():
                df_channel_info = self.set_filter_condition(df_channel_info)
                cuts = pd.cut(df_channel_info[value], value_range)
                prop = cuts.value_counts(normalize=True).sort_index()
                title = f"{value.capitalize()} 分布占比图"
                prop.index = prop.index.map(self.value_index_dict[value])
                self.visualise_bar_prop(prop, title, f"{img_path}/{value}_distribution", is_value=True)
                df_prop_ar, df_prop_dw, df_prop_cr, df_prop_LT = self.get_df_prop(df_channel_info)
                self.visualise_bar_prop(df_prop_ar, '四种碱基AR占比图', img_path + '/4_base_AR', is_value=True)
                self.visualise_bar_prop(df_prop_dw, '四种碱基DW占比图', img_path + '/4_base_DW', is_value=True)
                self.visualise_bar_prop(df_prop_cr, '四种碱基CR占比图', img_path + '/4_base_CR', is_value=True)
                self.visualise_bar_prop(df_prop_LT, 'Pore-LT与Basecall-LT占比图', img_path + '/Pore_LT-Basecall_LT',
                                        is_value=True)

                self.analyze_correlation(df_channel_info, f'准确率与读长的关系',
                                         img_path + '/correlation_read_len_and_identity')

            self.visualise_bar_prop(self.df_error_type, '总 - 四种错误类型统计', img_path + '/error_type')
            self.visualise_bar_prop(self.df_base_error, '总 - 四种碱基错误统计', img_path + '/base_error')
            self.visualise_bar_prop(self.df_base_error_type, '四种碱基 - 错误类型统计',
                                    img_path + '/base_error_type')
            self.visualise_table(self.csv_error_type_statistics, img_path + '/error_type_statistics')

            generate_pdf_single_run(directory, label)

            export_message.close()
            self.showMessageBox(f"导出成功！")

    def exportMultipleRun(self, directory):
        if self.ui.barcode_checkBox.isChecked():
            self.showMessageBox('请关闭barcode选项！')
        else:
            export_message = QMessageBox(self)
            export_message.setWindowTitle("提示")
            export_message.setText("正在导出，请稍候...")
            export_message.show()
            QApplication.processEvents()  # 刷新UI以确保消息窗口显示

            img_path = directory + '/imgs'
            if not os.path.exists(img_path):
                os.mkdir(img_path)
            if self.df_run_info is not None:
                self.visualise_table(self.df_run_info, img_path + '/run_info')
                self.visualise_table(self.df_pore_info, img_path + '/pore_info')

            for value, value_range in self.value_range_dict.items():
                prop_list = []
                for label, df_channel_info in self.label_info_dict.items():
                    df_channel_info = self.set_filter_condition(df_channel_info)
                    cuts = pd.cut(df_channel_info[value], value_range)
                    prop = cuts.value_counts(normalize=True).sort_index().rename(label)
                    prop.index = prop.index.map(self.value_index_dict[value])
                    prop_list.append(prop)
                    df_prop = pd.concat(prop_list, axis=1)

                    df_prop_ar, df_prop_dw, df_prop_cr, df_prop_LT = self.get_df_prop(df_channel_info)
                    self.visualise_bar_prop(df_prop_ar, f'{label} - 四种碱基AR占比图', img_path + f'/4_base_AR_{label}',
                                            is_value=True)
                    self.visualise_bar_prop(df_prop_dw, f'{label} - 四种碱基DW占比图', img_path + f'/4_base_DW_{label}',
                                            is_value=True)
                    self.visualise_bar_prop(df_prop_cr, f'{label} - 四种碱基CR占比图', img_path + f'/4_base_CR_{label}',
                                            is_value=True)
                    self.visualise_bar_prop(df_prop_LT, f'{label} - Pore-LT与Basecall-LT占比图',
                                            img_path + f'/Pore_LT-Basecall_LT_{label}',
                                            is_value=True)

                    title = f"{value.capitalize()} 分布占比图"
                    self.visualise_bar_prop(df_prop, title, f"{img_path}/{value}_distribution", is_value=True)

                    self.analyze_correlation(df_channel_info, f'{label} - 准确率与读长的关系',
                                             img_path + f'/correlation_read_len_and_identity_{label}')

            self.visualise_bar_prop(self.df_error_type, '总 - 四种错误类型统计', img_path + '/error_type')
            self.visualise_bar_prop(self.df_base_error, '总 - 四种碱基错误统计', img_path + '/base_error')

            label_list = []
            for label, df_base_error_type in self.df_base_error_type_dict.items():
                label_list.append(label)
                self.visualise_bar_prop(df_base_error_type, f'{label} - 四种碱基 - 错误类型统计',
                                        img_path + f'/base_error_type_{label}')
            for label, csv_error_type_statistics in self.csv_error_type_statistics_dict.items():
                self.visualise_table(csv_error_type_statistics, img_path + f'/error_type_statistics_{label}')

            generate_pdf_multiple_run(directory, label_list)

            export_message.close()
            self.showMessageBox(f"导出成功！")

    def exportBarcode(self, directory):
        if not self.ui.barcode_checkBox.isChecked():
            self.showMessageBox('请开启barcode选项！')
        else:
            export_message = QMessageBox(self)
            export_message.setWindowTitle("提示")
            export_message.setText("正在导出，请稍候...")
            export_message.show()
            QApplication.processEvents()  # 刷新UI以确保消息窗口显示

            img_path = directory + '/imgs'
            if not os.path.exists(img_path):
                os.mkdir(img_path)
            if self.df_run_info is not None:
                self.visualise_table(self.df_run_info, img_path + '/run_info')
                self.visualise_table(self.df_pore_info, img_path + '/pore_info')

            for value, value_range in self.value_range_dict.items():
                prop_list = []
                for label, df_group in self.label_info_dict.items():
                    if label != '-':
                        cuts = pd.cut(df_group[value], value_range)
                        prop = cuts.value_counts(normalize=True).sort_index().rename(label)
                        prop.index = prop.index.map(self.value_index_dict[value])
                        prop_list.append(prop)
                        df_prop = pd.concat(prop_list, axis=1)

                        df_prop_ar, df_prop_dw, df_prop_cr, df_prop_LT = self.get_df_prop(df_group)
                        self.visualise_bar_prop(df_prop_ar, f'{label} - 四种碱基AR占比图',
                                                img_path + f'/4_base_AR_{label}',
                                                is_value=True)
                        self.visualise_bar_prop(df_prop_dw, f'{label} - 四种碱基DW占比图',
                                                img_path + f'/4_base_DW_{label}',
                                                is_value=True)
                        self.visualise_bar_prop(df_prop_cr, f'{label} - 四种碱基CR占比图',
                                                img_path + f'/4_base_CR_{label}',
                                                is_value=True)
                        self.visualise_bar_prop(df_prop_LT, f'{label} - Pore-LT与Basecall-LT占比图',
                                                img_path + f'/Pore_LT-Basecall_LT_{label}',
                                                is_value=True)

                        title = f"{value.capitalize()} 分布占比图"
                        self.visualise_bar_prop(df_prop, title, f"{img_path}/{value}_distribution", is_value=True)

                        self.analyze_correlation(df_group, f'{label} - 准确率与读长的关系',
                                                 img_path + f'/correlation_read_len_and_identity_{label}')

            self.visualise_bar_prop(self.df_error_type, '总 - 四种错误类型统计', img_path + '/error_type')
            self.visualise_bar_prop(self.df_base_error, '总 - 四种碱基错误统计', img_path + '/base_error')

            label_list = []
            for label, df_base_error_type in self.df_base_error_type_dict.items():
                label_list.append(label)
                self.visualise_bar_prop(df_base_error_type, f'{label} - 四种碱基 - 错误类型统计',
                                        img_path + f'/base_error_type_{label}')
            for label, csv_error_type_statistics in self.csv_error_type_statistics_dict.items():
                self.visualise_table(csv_error_type_statistics, img_path + f'/error_type_statistics_{label}')

            generate_pdf_multiple_run(directory, label_list)

            export_message.close()
            self.showMessageBox(f"导出成功！")

    def visualise_table(self, df, img_path):
        plt.clf()

        # 计算表格的大小，根据行数和列数来估计
        table_height = int(df.shape[0] * 0.5)  # 行数乘以一个估计的行高度
        table_width = int(df.shape[1] * 1)  # 列数乘以一个估计的列宽度

        fig, ax = plt.subplots(figsize=(min(10, table_width), min(5, table_height)))
        ax.axis('off')

        if 'Index' in df.columns:
            df = df.drop(columns=['Index'])

        df.insert(0, 'Index', df.index)
        table_info = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center',
                              colColours=['#f2f2f2'] * len(df.columns))

        # 调整表格布局
        table_info.auto_set_font_size(False)
        table_info.set_fontsize(10)
        table_info.auto_set_column_width(col=list(range(len(df.columns))))
        table_info.scale(1, 1.5)

        plt.savefig(img_path, bbox_inches='tight', pad_inches=0.5)
        plt.close()

    def visualise_bar_prop(self, df, title, img_path, is_value=False):
        plt.clf()
        ax = df.plot(kind='bar', figsize=(12, 6))
        '''可更改尺寸'''
        ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.1%}'))
        ax.tick_params(axis='y', labelsize=10)
        if is_value:
            ax.set_xticklabels(df.index, rotation=30, fontsize=10)
        else:
            ax.set_xticklabels(df.index, rotation=0, fontsize=10)
        ax.set_xlabel('')  # 不显示横坐标下方的轴名称
        ax.set_title(title, fontsize=14)

        '''柱状图显示值'''
        if self.is_display_value:
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.1%}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', xytext=(0, 10), textcoords='offset points')

        plt.savefig(img_path)
        plt.close()

    def visualise_scatter(self, df, x_column, y_column, x_lim, title, img_path):
        plt.figure(figsize=(12, 6))
        plt.scatter(df[x_column], df[y_column])

        mean_y = np.mean(df[y_column])
        weighted_mean_y = np.average(df[y_column], weights=df[
            'sub_total_len'])  # Replace 'weights_column' with the actual column name
        mode_y = mode(df[y_column], axis=None, keepdims=True).mode[0]

        plt.axhline(weighted_mean_y, color='orange', linestyle='-.', linewidth=2,
                    label=f'Weighted Mean Y: {weighted_mean_y:.2f}')
        plt.axhline(mean_y, color='r', linestyle='--', linewidth=2, label=f'Mean Y: {mean_y:.2f}')
        plt.axhline(mode_y, color='b', linestyle='--', linewidth=2, label=f'Mode Y: {mode_y:.2f}')

        # Plot mean of x-axis
        mean_x = np.mean(df[x_column])
        plt.axvline(mean_x, color='r', linestyle='--', linewidth=2, label=f'Mean X: {mean_x:.2f}')

        fontdict = {'fontsize': 12, 'fontweight': 'bold'}
        offset = 3
        plt.text(mean_x, mean_y, f'Mean = {mean_y:.2f}', color='r', fontdict=fontdict)
        plt.text(mean_x, weighted_mean_y - offset, f'Weighted Mean = {weighted_mean_y:.2f}', color='orange',
                 fontdict=fontdict)
        plt.text(mean_x, mode_y + offset, f'Mode = {mode_y:.2f}', color='b', fontdict=fontdict)
        plt.text(mean_x, 0, f'{mean_x:.2f}', color='r', fontdict=fontdict)

        plt.xlabel(x_column, fontsize=14)
        plt.ylabel(y_column, fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.xlim(0, x_lim)
        plt.ylim(0, 100)
        plt.title(title, fontsize=16)
        plt.grid(True)
        plt.savefig(img_path)
        plt.close()

    def analyze_correlation(self, df, title, img_path):
        read_len = 'read_len'
        average_identity = 'average_identity'
        x_lim = df['read_len'].max()
        self.visualise_scatter(df, read_len, average_identity, x_lim,
                               title, img_path)

    def showMessageBox(self, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(message)
        msgBox.setWindowTitle("提示")
        msgBox.exec_()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
