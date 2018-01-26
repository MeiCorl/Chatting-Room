import json

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLineEdit

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

    def register(self):
        if self.password_1.text() != self.password_2.text():
            QMessageBox.information(self, "Error", "password does not match!")
            return
        msg = {"type": 4, "name": self.user_name.text(), "password": self.password_1.text()}
        data = json.dumps(msg).encode()
        self.client_socket.send(data)
        self.close()
