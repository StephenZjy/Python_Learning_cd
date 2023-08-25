import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton, QFileDialog, \
    QTextEdit, QMessageBox, QDialog, QLineEdit, QInputDialog
import pandas as pd
from pathlib import Path
import shutil
from process import *

class OperationGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('操作界面')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.operation_combobox = QComboBox(self)
        self.operation_combobox.addItems(["Get Components", "Ajust Folder Level", "Rename File"])
        layout.addWidget(self.operation_combobox)

        self.execute_button = QPushButton('执行操作', self)
        self.execute_button.clicked.connect(self.execute_operations)
        layout.addWidget(self.execute_button)

        # self.text_edit = QTextEdit(self)
        # layout.addWidget(self.text_edit)

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        # self.column_order_input = QLineEdit(self)
        # layout.addWidget(self.column_order_input)

    def execute_operations(self):
        selected_operation = self.operation_combobox.currentText()
        dir_path = QFileDialog.getExistingDirectory(self, "选择文件夹")

        file_path_list = get_file_path_list(dir_path)
        path_components_list = []

        for file_path in file_path_list:
            path_components = parse_file_path(dir_path, file_path)
            path_components_list.append(path_components)

        df_components = pd.DataFrame(path_components_list)
        df_components.to_csv('result.csv', index=False)

        if dir_path and selected_operation:
            if selected_operation == "Get Components":
                result_df = get_components(df_components)
                formatted_text = format_dataframe(result_df)
                show_formatted_content(formatted_text)

            elif selected_operation == "Ajust Folder Level":
                result_df = get_components(df_components)
                formatted_text = format_dataframe(result_df)
                show_formatted_content(formatted_text)

                column_order, ok = QInputDialog.getText(self, "输入文件层级定义", "例如：/0/1/2/4_5")
                if ok:
                    ajusted_file_path_list = get_ajusted_file_path(dir_path, df_components, column_order)
                    ajust_folder_level(file_path_list, ajusted_file_path_list)

            elif selected_operation == "Rename File":
                replace_mapping = {
                    'c01': 'c0001'
                }
                rename_file(replace_mapping, dir_path)

    def show_folder_level_input(self):
        column_order, ok = QInputDialog.getText(self, "输入文件层级定义", "例如：/0/1/2/4_5")
        if ok:
            self.execute_folder_level(column_order)

    def execute_folder_level(self, column_order):
        # 执行文件层级操作
        ajusted_file_path_list = get_ajusted_file_path(dir_path, df_components, column_order)
        ajust_folder_level(file_path_list, ajusted_file_path_list)

        # 同时显示格式化内容
        result_df = get_components(df_components)
        formatted_text = format_dataframe(result_df)
        show_formatted_content(formatted_text)
class CustomDialog(QDialog):
    def __init__(self, content):
        super().__init__()
        self.initUI(content)

    def initUI(self, content):
        self.setWindowTitle("Data info")
        self.setGeometry(200, 200, 1200, 600)

        layout = QVBoxLayout()
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText(content)
        layout.addWidget(self.text_edit)

        self.setLayout(layout)


def show_formatted_content(content):
    custom_dialog = CustomDialog(content)
    custom_dialog.exec_()


def format_dataframe(df):
    keyword_to_label = {
        'speck': '设备',
        'mm': '焦距',
        'person': '人员',
        'lux': '光照',
        'clean': '背景',
        'm': '距离',
        'sit': '其他条件',
        'c01': '动作'
    }

    formatted_lines = []
    unique_lines = set()  # 用于跟踪已经出现过的行内容

    for col in df.columns:
        col_values = df[col].explode().unique()
        content = ", ".join(sorted(map(str, col_values)))
        for value in col_values:
            for keyword, label in keyword_to_label.items():
                if keyword in value:
                    line = f"[{col}].{label}： {content}"
                    if line not in unique_lines:  # 只添加不重复的行内容
                        formatted_lines.append(line)
                        unique_lines.add(line)

    formatted_text = '\n'.join(formatted_lines)

    return formatted_text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = OperationGUI()
    gui.show()
    sys.exit(app.exec_())