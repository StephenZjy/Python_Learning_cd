import time
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QMutexLocker

from utils import *


class ReadThread(QtCore.QThread):
    send_events_signal = QtCore.pyqtSignal()

    def __init__(self, ppg_buf, acc_buf, mutex, filename='', is_recording=False):
        super(ReadThread, self).__init__()
        self.ppg_buf = ppg_buf
        self.acc_buf = acc_buf
        self.is_recording = is_recording
        self.filename = filename
        self.mutex = mutex

    def run(self):
        while 1:
            # data_list = ['FIFO:',
            #              '28234 28214 28227 28238 28245 28239 28298 28314 28273 28277 28242 28252 28299 28292 28299',
            #              'Acc x,y,z:',
            #              '-137 28 -161 -137 23 -158 -134 21 -156 -139 22 -159 -140 24 -159 -138 24 -159 -137 25 -160 -136 29 -160 -133 25 -159 -133 28 -160 -133 25 -162 -128 21 -159 -129 21 -159 -128 16 -158 -128 16 -160']

            with open('c05_0005.txt', 'r+') as f:
                data_list = f.readlines()
            print(data_list)
            current_data_type = None

            while True:
                with QMutexLocker(self.mutex):
                    for data in data_list:
                        data = data.strip()
                        if data == 'FIFO:':
                            current_data_type = 'PPG'
                        elif data == 'Acc x,y,z:':
                            current_data_type = 'Acceleration'
                        else:
                            values = [int(val) for val in data.split()]
                            if current_data_type == 'PPG':
                                self.ppg_buf.extend(values)
                            elif current_data_type == 'Acceleration':
                                self.acc_buf.extend(values)

                        if self.is_recording == False:
                            # print(self.ppg_buf, self.acc_buf)
                            continue
                        save_data(data, self.filename)
                time.sleep(0.6)


class PlotThread(QtCore.QThread):
    def __init__(self, ppg_buf, acc_buf, mutex, plot_func=None):
        super(PlotThread, self).__init__()
        self.ppg_buf = ppg_buf
        self.acc_buf = acc_buf
        self.ppg_data = []
        self.accX_data = []
        self.accY_data = []
        self.accZ_data = []
        self.plot_func = plot_func
        self.mutex = mutex

    def run(self):
        while 1:
            if self.ppg_buf and self.acc_buf:
                with QMutexLocker(self.mutex):
                    if len(self.ppg_data) < 15:
                        self.ppg_data.append(self.ppg_buf.pop(0))
                        self.accX_data.append(self.acc_buf.pop(0))
                        self.accY_data.append(self.acc_buf.pop(0))
                        self.accZ_data.append(self.acc_buf.pop(0))
                    else:
                        self.ppg_data.pop(0)
                        self.accX_data.pop(0)
                        self.accY_data.pop(0)
                        self.accZ_data.pop(0)
                        self.ppg_data.append(self.ppg_buf.pop(0))
                        self.accX_data.append(self.acc_buf.pop(0))
                        self.accY_data.append(self.acc_buf.pop(0))
                        self.accZ_data.append(self.acc_buf.pop(0))

                    self.plot_func(self.ppg_data, self.accX_data, self.accY_data, self.accZ_data)
                time.sleep(0.04)
