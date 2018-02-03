import json

import time
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

from UI.RoomWindow import Ui_Room


class FriendWind(QtWidgets.QMainWindow, Ui_Room):
    user_name = ""
    client_socket = None

    def __init__(self, friend, signature, icon_path):
        super(FriendWind, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle(friend + "(" + signature + ")")
        self.setWindowIcon(QIcon(icon_path))
        self.friend = friend
        self.signature = signature
        self.sendButton.clicked.connect(self.sendMessage)

    def sendMessage(self):
        text = self.textEdit.toPlainText()
        if text == "":
            QMessageBox.information(None, "Warning", "Can not send null message!")
            return
        Time = time.strftime(' %Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        self.addMessage(FriendWind.user_name + Time, text)

        # 发送消息
        msg = {"type": 6, "sender": FriendWind.user_name, "time": Time, "receiver": self.friend, "body": text}
        data = json.dumps(msg).encode()
        FriendWind.client_socket.send(data)
        self.textEdit.clear()

    def addMessage(self, sender_time, msg):
        self.message.append(sender_time)
        self.message.append(msg+"\n")
