from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QHBoxLayout, QAction, QPushButton, QMenu, QMenuBar

from csvOperator import *
from utils import *


class Ui_login(QtWidgets.QDialog):
    def __init__(self, mywindow_instance):
        super().__init__()
        self.mywindow = mywindow_instance
        self.current_username = None
        self.row_num = 0
        self.username = self.mywindow.username
        self.password = self.mywindow.password
        self.tel = self.mywindow.tel
        self.email = self.mywindow.email
        self.setupUi(self)
        self.load_info()

    def setupUi(self, login):
        login.setObjectName("login")
        login.resize(458, 785)
        self.photo_label = QtWidgets.QLabel(login)
        self.photo_label.setGeometry(QtCore.QRect(40, 40, 130, 150))
        self.photo_label.setObjectName("photo")
        self.username_label = QtWidgets.QLabel(login)
        self.username_label.setGeometry(QtCore.QRect(230, 40, 111, 41))
        self.username_label.setObjectName("username")
        self.username_textEdit = QtWidgets.QLineEdit(login)
        self.username_textEdit.setGeometry(QtCore.QRect(230, 40, 111, 41))
        self.username_textEdit.setObjectName("username")
        self.username_textEdit.setVisible(False)
        self.tel_label = QtWidgets.QLabel(login)
        self.tel_label.setGeometry(QtCore.QRect(230, 90, 111, 41))
        self.tel_label.setObjectName("tel")
        self.tel_textEdit = QtWidgets.QLineEdit(login)
        self.tel_textEdit.setGeometry(QtCore.QRect(230, 90, 111, 41))
        self.tel_textEdit.setObjectName("tel")
        self.tel_textEdit.setVisible(False)
        self.email_label = QtWidgets.QLabel(login)
        self.email_label.setGeometry(QtCore.QRect(230, 140, 111, 41))
        self.email_label.setObjectName("email")
        self.email_textEdit = QtWidgets.QLineEdit(login)
        self.email_textEdit.setGeometry(QtCore.QRect(230, 140, 111, 41))
        self.email_textEdit.setObjectName("email")
        self.email_textEdit.setVisible(False)

        self.editButton = QtWidgets.QPushButton(login)
        self.editButton.setGeometry(QtCore.QRect(350, 40, 50, 30))
        self.editButton.setObjectName("editButton")
        self.editButton.setText("编辑")
        self.editButton.clicked.connect(self.toggle_edit_mode)
        self.changePasswdButton = QtWidgets.QPushButton(login)
        self.changePasswdButton.setGeometry(QtCore.QRect(350, 70, 80, 30))
        self.changePasswdButton.setObjectName("editButton")
        self.changePasswdButton.setText("修改密码")
        self.changePasswdButton.clicked.connect(self.show_change_password_window)

        self.tableWidget = QtWidgets.QTableWidget(login)
        self.tableWidget.setGeometry(QtCore.QRect(40, 210, 391, 551))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnWidth(0, 110)
        self.tableWidget.setColumnWidth(1, 260)
        self.tableWidget.verticalHeader().setDefaultSectionSize(100)
        self.tableWidget.setIconSize(QSize(100, 120))
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)

        photo_item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, photo_item)
        username_item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, username_item)
        self.tableWidget.doubleClicked.connect(self.show_user_window)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.itemClicked.connect(self.on_tableWidget_Clicked)

        self.photo_label.raise_()
        self.username_label.raise_()
        self.tableWidget.raise_()

        self.retranslateUi(login)
        QtCore.QMetaObject.connectSlotsByName(login)

    def retranslateUi(self, login):
        _translate = QtCore.QCoreApplication.translate
        login.setWindowTitle(_translate("login", "login"))
        self.photo_label.setText(_translate("login", "photo"))
        self.username_label.setText(_translate("login", self.username))
        self.tel_label.setText(_translate("login", self.tel))
        self.email_label.setText(_translate("login", self.email))
        self.username_textEdit.setText(_translate("login", self.username))
        self.tel_textEdit.setText(_translate("login", self.tel))
        self.email_textEdit.setText(_translate("login", self.email))
        photo_item = self.tableWidget.horizontalHeaderItem(0)
        photo_item.setText(_translate("login", "照片"))
        username_item = self.tableWidget.horizontalHeaderItem(1)
        username_item.setText(_translate("login", "姓名"))

        photo_path = self.get_photo_path('user_photo', self.username)
        if not photo_path:
            photo_path = 'user_photo/default.png'
        pixmap = QPixmap(photo_path)
        self.photo_label.setPixmap(pixmap)
        self.photo_label.setScaledContents(True)

    def toggle_edit_mode(self):
        if self.username_label.isVisible():
            self.username_label.setVisible(False)
            self.tel_label.setVisible(False)
            self.email_label.setVisible(False)
            self.username_textEdit.setVisible(True)
            self.tel_textEdit.setVisible(True)
            self.email_textEdit.setVisible(True)
            self.editButton.setText("保存")  # 切换按钮文本
        else:
            df_info = read_csv(csv_file='user_info.csv')
            if (self.username_textEdit.text() != self.username_label.text()
                    and (df_info['username'] == self.username_textEdit.text()).any()):
                show_dialog(self, '提示', '用户名已存在')
            else:
                update_csv(self.username_label.text(), self.username_textEdit.text(), self.tel_textEdit.text(),
                           self.email_textEdit.text(),
                           new_password=None)
                self.update_info()
                self.username_label.setVisible(True)
                self.tel_label.setVisible(True)
                self.email_label.setVisible(True)
                self.username_textEdit.setVisible(False)
                self.tel_textEdit.setVisible(False)
                self.email_textEdit.setVisible(False)
                self.editButton.setText("编辑")

    def update_info(self):
        photo_path = self.get_photo_path('user_photo', self.username_label.text())
        new_photo_path = photo_path.replace(self.username_label.text(), self.username_textEdit.text())
        os.rename(photo_path, new_photo_path)
        self.username_label.setText(self.username_textEdit.text())
        self.tel_label.setText(self.tel_textEdit.text())
        self.email_label.setText(self.email_textEdit.text())
        self.username_textEdit.setText(self.username_textEdit.text())
        self.tel_textEdit.setText(self.tel_textEdit.text())
        self.email_textEdit.setText(self.email_textEdit.text())

    def set_row_data(self, row, username, photo_path):
        photo_item = QTableWidgetItem()
        icon = QIcon(photo_path)
        pixmap = QPixmap(icon.pixmap(100, 120))
        scaled_pixmap = pixmap.scaled(100, 120)
        scaled_icon = QIcon(scaled_pixmap)
        photo_item.setIcon(scaled_icon)
        username_item = QTableWidgetItem(username)
        photo_item.setTextAlignment(QtCore.Qt.AlignCenter)
        username_item.setTextAlignment(QtCore.Qt.AlignCenter)

        self.tableWidget.setItem(row, 0, photo_item)
        self.tableWidget.setItem(row, 1, username_item)

    def get_user_info(self):
        df_info = read_csv(csv_file='user_info.csv')
        username, password, tel, email = match_username(df_info, self.current_username)

        return username, tel, email

    def load_info(self, csv_file='user_info.csv'):
        df_info = read_csv(csv_file)

        for row, (_, data) in enumerate(df_info.iterrows()):
            username = data['username']
            photo_path = self.get_photo_path('user_photo', username)
            if username != self.username_label.text():
                self.row_num = self.tableWidget.rowCount()
                self.tableWidget.setRowCount(self.row_num + 1)
                if photo_path:
                    self.set_row_data(self.row_num, username, photo_path)
                else:
                    self.set_row_data(self.row_num, username, 'user_photo/default.png')
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def get_photo_path(self, file_dir, target_string):
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if target_string in file:
                    photo_path = os.path.join(root, file)
                    return photo_path

    def on_tableWidget_Clicked(self, item):
        item = self.tableWidget.item(item.row(), 1)
        if item is not None:
            self.current_username = item.text()

    def show_change_password_window(self):
        change_password_window = Ui_change_password(self)
        result = change_password_window.exec_()
        if result == QtWidgets.QDialog.Accepted:
            show_dialog(self, "提示", "密码已修改，请重新登录")
            self.close()
            self.mywindow.show()

    def show_user_window(self):
        user_window = Ui_user_window(self)
        x, y = self.x(), self.y()
        # 调整 x 和 y 以适应您的需求，例如在右侧
        x += self.width() + 10
        # 更新 Ui_user_window 的位置
        self.user_window.set_position(x, y)
        user_window.show()
        user_window.exec_()


class Ui_change_password(QtWidgets.QDialog):
    def __init__(self, login_instance):
        super().__init__()
        self.login_instance = login_instance
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("修改密码")
        parent_x = self.login_instance.x()
        parent_y = self.login_instance.y()
        self.setGeometry(parent_x + self.login_instance.width() + 20, parent_y, 400, 200)

        self.old_password_label = QtWidgets.QLabel("原密码:", self)
        self.old_password_label.setGeometry(50, 30, 100, 20)
        self.old_password_input = QtWidgets.QLineEdit(self)
        self.old_password_input.setGeometry(200, 30, 150, 20)

        self.new_password_label = QtWidgets.QLabel("新密码:", self)
        self.new_password_label.setGeometry(50, 60, 100, 20)
        self.new_password_input = QtWidgets.QLineEdit(self)
        self.new_password_input.setGeometry(200, 60, 150, 20)

        self.confirm_password_label = QtWidgets.QLabel("确认密码:", self)
        self.confirm_password_label.setGeometry(50, 90, 150, 20)
        self.confirm_password_input = QtWidgets.QLineEdit(self)
        self.confirm_password_input.setGeometry(200, 90, 150, 20)

        self.confirm_button = QtWidgets.QPushButton("提交", self)
        self.confirm_button.setGeometry(200, 120, 100, 30)
        self.confirm_button.clicked.connect(self.check_input)

    def check_input(self):
        old_password = self.old_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if old_password != self.login_instance.password:
            show_dialog(self, "提示", "原密码不正确")
        elif new_password != confirm_password:
            show_dialog(self, '提示', '密码和确认密码不匹配，请重新输入')
            self.old_password_input.clear()
            self.new_password_input.clear()
            self.confirm_password_input.clear()
        else:
            update_csv(self.login_instance.username, new_username=None, new_tel=None, new_email=None, new_password=new_password,
                       is_change_password=True)
            show_dialog(self, "提示", "密码已成功更新")
            self.accept()


class Ui_user_window(QtWidgets.QDialog):
    def __init__(self, login_instance):
        super().__init__()
        self.login_instance = login_instance
        self.setupUi(self)

    def setupUi(self, user_window):
        user_window.setObjectName("user_window")
        self.photo = QtWidgets.QLabel(user_window)
        self.photo.setGeometry(QtCore.QRect(40, 60, 131, 191))
        self.photo.setText("")
        self.photo.setObjectName("photo")
        self.personal_info = QtWidgets.QLabel(user_window)
        self.personal_info.setGeometry(QtCore.QRect(250, 10, 67, 17))
        self.personal_info.setObjectName("personal_info")
        self.username_label = QtWidgets.QLabel(user_window)
        self.username_label.setGeometry(QtCore.QRect(190, 60, 67, 17))
        self.username_label.setObjectName("username")
        self.tel_label = QtWidgets.QLabel(user_window)
        self.tel_label.setGeometry(QtCore.QRect(190, 140, 67, 17))
        self.tel_label.setObjectName("tel")
        self.email_label = QtWidgets.QLabel(user_window)
        self.email_label.setGeometry(QtCore.QRect(190, 220, 67, 17))
        self.email_label.setObjectName("email")
        self.exitButton = QtWidgets.QPushButton(user_window)
        self.exitButton.setGeometry(QtCore.QRect(390, 310, 89, 25))
        self.exitButton.setObjectName("exitButton")
        self.get_username = QtWidgets.QLabel(user_window)
        self.get_username.setGeometry(QtCore.QRect(270, 60, 111, 21))
        self.get_username.setObjectName("get_name")
        self.get_tel = QtWidgets.QLabel(user_window)
        self.get_tel.setGeometry(QtCore.QRect(270, 140, 111, 21))
        self.get_tel.setObjectName("get_tel")
        self.get_email = QtWidgets.QLabel(user_window)
        self.get_email.setGeometry(QtCore.QRect(270, 220, 111, 21))
        self.get_email.setObjectName("get_email")

        self.exitButton.clicked.connect(self.close)
        self.retranslateUi(user_window)
        QtCore.QMetaObject.connectSlotsByName(user_window)

    def retranslateUi(self, user_window):
        _translate = QtCore.QCoreApplication.translate
        username, tel, email = self.login_instance.get_user_info()
        user_window.setWindowTitle(_translate("user_window", "user"))
        self.personal_info.setText(_translate("user_window", "个人信息"))
        self.username_label.setText(_translate("user_window", "姓名"))
        self.tel_label.setText(_translate("user_window", "电话"))
        self.email_label.setText(_translate("user_window", "邮箱"))
        self.exitButton.setText(_translate("user_window", "关闭"))
        self.get_username.setText(_translate("user_window", username))
        self.get_tel.setText(_translate("user_window", tel))
        self.get_email.setText(_translate("user_window", email))

        photo_path = os.path.join("user_photo", f"{username}.jpg")
        pixmap = QPixmap(photo_path)
        self.photo.setPixmap(pixmap)
        self.photo.setScaledContents(True)

    def set_position(self, x, y):
        self.setGeometry(x, y, 561, 532)