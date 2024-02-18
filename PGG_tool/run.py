import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QMutex
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from mythread import ReadThread, PlotThread
from ui import Ui_Record_window
from utils import *


class Mywindow(QMainWindow, Ui_Record_window):
    def __init__(self):
        super(Mywindow, self).__init__()
        self.setupUi(self)
        self.file_path = ""
        self.ppg_buf = []
        self.acc_buf = []
        self.mutex = QMutex()
        self.start_read_buf()
        self.start_plot_thread()
        self.select_Button.clicked.connect(self.select_file_path)
        self.record_Button.clicked.connect(self.toggle_recording)

    def toggle_recording(self):
        filename = self.filename_lineEdit.text()
        if len(filename) == 0:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please input filename")
            return
        if not self.thread_read.is_recording:
            self.record_Button.setText("Stop")
            filename = self.file_path + filename
            self.thread_read.filename = filename
            self.thread_read.is_recording = True
            self.filename_lineEdit.setDisabled(True)  # Disable the input field
            self.start_timer()
        else:
            self.record_Button.setText("Record")
            self.thread_read.is_recording = False
            self.filename_lineEdit.setDisabled(False)
            self.filename_lineEdit.setText(next_filename(filename))
            self.stop_timer()  # Call a method to stop the timer if needed

    def select_file_path(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Choose folder", options=options)
        if folder_path:
            self.file_path = folder_path + '/'
            self.foldername_label.setText(f"{folder_path}")

    def start_read_buf(self):
        self.thread_read = ReadThread(ppg_buf=self.ppg_buf, acc_buf=self.acc_buf, mutex=self.mutex, is_recording=False)
        self.thread_read.start()

    def start_plot_thread(self):
        self.thread_plot = PlotThread(ppg_buf=self.ppg_buf, acc_buf=self.acc_buf, mutex=self.mutex, plot_func=self.plot_data)
        self.thread_plot.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Mywindow()
    window.show()
    sys.exit(app.exec_())