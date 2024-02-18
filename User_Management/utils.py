from PyQt5.QtWidgets import QMessageBox


def show_dialog(window, title, text):
    msg = QMessageBox(window)
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.exec_()