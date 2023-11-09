import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui import Ui_MainWindow
from register_window import Ui_register
from login_window import Ui_login
from SqlOperation import SqlOperation
from utils import *


class Mywindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Mywindow, self).__init__()
        self.setupUi(self)
        self.sqlOperation = SqlOperation()
        self.username = None
        self.password = None
        self.tel = None
        self.email = None

    def match_info(self):
        username_text = self.username_textEdit.toPlainText()
        password_text = self.password_textEdit.toPlainText()

        info = self.sqlOperation.select_username(username_text)
        if info:
            self.username = info[1]
            self.password = info[2]
            self.tel = info[3]
            self.email = info[4]

            if password_text == self.password:
                return True
            else:
                show_dialog(self, '提示', '密码不正确')
        else:
            show_dialog(self, '提示', '用户名不存在')

    def login(self):
        if self.match_info():
            login_window = Ui_login(self)
            login_window.show()
            self.close()
            login_window.exec_()

    def register(self):
        register_window = Ui_register(self)
        register_window.show()
        self.hide()
        register_window.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Mywindow()
    window.show()
    sys.exit(app.exec_())
