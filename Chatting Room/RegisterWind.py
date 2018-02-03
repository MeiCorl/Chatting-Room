import json

import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QFileDialog

from UI.RegisterWind import Ui_RegitserDialog


class RegisterWind(QtWidgets.QMainWindow, Ui_RegitserDialog):
    def __init__(self, client_socket):
        super(RegisterWind, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        # 设置密码显示
        self.password_1.setEchoMode(QLineEdit.Password)
        self.password_2.setEchoMode(QLineEdit.Password)

        self.client_socket = client_socket
        self.registerButton.clicked.connect(self.register)
        self.cancelButton.clicked.connect(self.close)
        self.iconButton.clicked.connect(self.chooseIcon)
        self.icon_path = ""

    def register(self):
        if self.password_1.text() != self.password_2.text():
            QMessageBox.information(self, "Error", "password does not match!")
            return
        # 发送注册消息
        msg = {"type": 4, "name": self.user_name.text(), "password": self.password_1.text(), "signature": self.signature.text(), "portrait": self.icon_path}
        self.client_socket.send(json.dumps(msg).encode())
        self.close()

    def chooseIcon(self):
        icon_path, _ = QFileDialog.getOpenFileName(self, " select a icon", "./image", "Txt files(*.jpg)")
        icon_name = os.path.basename(os.path.realpath(icon_path))
        pixMap = QPixmap(icon_path).scaled(self.head_icon.width(), self.head_icon.height())
        self.head_icon.setPixmap(pixMap)

        self.icon_path = "image/"+icon_name

        if self.getRelativePath(icon_path) != self.icon_path:
            src_icon = open(icon_path, 'rb')
            dst_icon = open(self.icon_path, 'wb')
            while 1:
                line = src_icon.readline()
                if not line:
                    break
                dst_icon.write(line)

    def getRelativePath(self, absolute_path):
        cur_path = QDir('.')
        relative_path = cur_path.relativeFilePath(absolute_path)
        return relative_path

