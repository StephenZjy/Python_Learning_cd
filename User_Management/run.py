import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui import Ui_MainWindow
from csvOperator import *
from register_window import Ui_register
from login_window import Ui_login


class Mywindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Mywindow, self).__init__()
        self.setupUi(self)

    def match_info(self):
        username_text = self.username_textEdit.toPlainText()
        password_text = self.password_textEdit.toPlainText()

        pd_info = read_csv(csv_file='user_info.csv')
        if username_text in pd_info['username'].values:
            user_info = pd_info[pd_info['username'] == username_text]
            username = str(user_info['username'].values[0])
            password = str(user_info['password'].values[0])
            tel = str(user_info['tel'].values[0])
            email = str(user_info['email'].values[0])
            if password == password_text:
                return username, tel, email
            else:
                self.show_dialog('提示', '密码不正确')
        else:
            self.show_dialog('提示', '用户名不存在')

    def show_dialog(self, title, text):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()

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
    -
    sys.exit(app.exec_())