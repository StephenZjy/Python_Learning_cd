from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTimer, QTime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Ui_Record_window(object):
    def setupUi(self, Record_window):
        Record_window.setObjectName("Record_window")
        Record_window.resize(846, 626)
        self.graphicsView = QtWidgets.QGraphicsView(Record_window)
        self.graphicsView.setGeometry(QtCore.QRect(25, 21, 791, 371))
        self.graphicsView.setObjectName("graphicsView")
        self.record_Button = QtWidgets.QPushButton(Record_window)
        self.record_Button.setGeometry(QtCore.QRect(230, 460, 361, 51))
        self.record_Button.setObjectName("record_Button")
        self.filename_lineEdit = QtWidgets.QLineEdit(Record_window)
        self.filename_lineEdit.setGeometry(QtCore.QRect(230, 540, 261, 41))
        self.filename_lineEdit.setObjectName("filename_lineEdit")
        self.select_Button = QtWidgets.QPushButton(Record_window)
        self.select_Button.setGeometry(QtCore.QRect(500, 544, 91, 31))
        self.select_Button.setObjectName("select_Button")
        self.foldername_label = QtWidgets.QLabel(Record_window)
        self.foldername_label.setGeometry(QtCore.QRect(230, 590, 561, 21))
        self.foldername_label.setObjectName("foldername_label")
        self.time_label = QtWidgets.QLabel(Record_window)
        self.time_label.setGeometry(QtCore.QRect(330, 410, 171, 21))
        self.time_label.setObjectName("time_label")
        self.time_label.setStyleSheet("font: bold 18pt 'Arial Black'; color: black;")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_time = QTime(0, 0)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QtWidgets.QVBoxLayout(self.graphicsView)
        self.layout.addWidget(self.canvas)

        self.retranslateUi(Record_window)
        QtCore.QMetaObject.connectSlotsByName(Record_window)

    def retranslateUi(self, Record_window):
        _translate = QtCore.QCoreApplication.translate
        Record_window.setWindowTitle(_translate("Record_window", "PPG_Recorder"))
        self.record_Button.setText(_translate("Record_window", "Record"))
        self.select_Button.setText(_translate("Record_window", "Choose"))
        self.foldername_label.setText(_translate("Record_window", ""))
        self.time_label.setText(_translate("Record_window", "00:00:00.000"))

    def update_timer(self):
        self.elapsed_time = self.elapsed_time.addMSecs(1)  # 每秒更新计时器
        time_str = self.elapsed_time.toString("hh:mm:ss.zzz")  # 格式化时间
        self.time_label.setText(time_str)

    def start_timer(self):
        self.elapsed_time = QTime(0, 0)
        self.timer.start(1)  # 每秒触发一次计时器
        self.time_label.setText("00:00:00.000")  # 初始值

    def stop_timer(self):
        self.timer.stop()

    def plot_data(self, ppg_data, accX_data, accY_data, accZ_data):
        self.figure.clear()

        time = range(len(ppg_data))
        ax1 = self.figure.add_subplot(211)
        ax1.plot(time, ppg_data, label='PPG', color='yellow')
        ax1.set_title('PPG Data')
        ax1.set_ylabel('PPG Value')
        ax1.set_ylim(0, 35000)  # 设置纵坐标范围
        ax1.set_yticks(range(0, 40000, 5000))
        ax1.legend(['PPG'], loc='upper right')

        # 在绘图区域中绘制ACC数据
        ax2 = self.figure.add_subplot(212)
        ax2.plot(time, accX_data, label='ACC_X', color='red')
        ax2.plot(time, accY_data, label='ACC_Y', color='green')
        ax2.plot(time, accZ_data, label='ACC_Z', color='blue')
        ax2.set_title('ACC Data')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('ACC Value')
        ax2.set_ylim(-300, 300)  # 设置纵坐标范围
        ax2.set_yticks(range(-300, 300, 100))
        ax2.legend(['ACC_X', 'ACC_Y', 'ACC_Z'], loc='upper right')

        self.figure.subplots_adjust(hspace=0.5)

        # 刷新绘图区域
        self.canvas.draw()
