import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from ui import Ui_MainWindow
from csvOperator import *
from register_window import Ui_register
from login_window import Ui_login
from utils import show_dialog


class Mywindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Mywindow, self).__init__()
        self.username = None
        self.password = None
        self.tel = None
        self.email = None
        self.setupUi(self)

    def match(self):
        username_text = self.username_textEdit.toPlainText()
        password_text = self.password_textEdit.toPlainText()
        df_info = read_csv(csv_file='user_info.csv')
        if username_text in df_info['username'].values:
            self.username, self.password, self.tel, self.email = match_username(df_info, username_text)
            if self.password == password_text:
                return True
            else:
                show_dialog(self, '提示', '密码不正确')
        else:
            show_dialog(self, '提示', '用户名不存在')

    def login(self):
        if self.match():
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
