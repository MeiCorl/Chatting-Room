import json
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from UI.RoomWindow import Ui_Room


class Room(QtWidgets.QMainWindow, Ui_Room):
    style1 = """
                    QProgressBar {
                        border: 2px solid gray;
                        border-radius: 5px;
                        text-align: center;
                    }
                    QProgressBar::chunk {
                        width: 20px;
                    }
                """
    style2 = """
                    QProgressBar {
                        border: 2px solid gray;
                        border-radius: 5px;
                        text-align: center;
                    }
                    QProgressBar::chunk {
                        background-color: red;
                        width: 20px;
                    }
            """
    client_socket = None
    user_name = ""
    isBusy = False   # 是否已经加入房间
    cur_roomId = -1  # 当前加入房间的ID

    def __init__(self, roomId, btn, size, progressBar):
        super(Room, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        self.roomId = roomId
        self.btn = btn
        self.size = size
        self.progressBar = progressBar
        self.progressBar.setValue(size)
        if size < 7:
            self.progressBar.setStyleSheet(Room.style1)
        else:
            self.progressBar.setStyleSheet(Room.style2)

        # 添加进度条值变化响应函数
        self.progressBar.valueChanged.connect(self.onProgressChanged)
        self.btn.clicked.connect(self.onJoinRoom)
        self.sendButton.clicked.connect(self.sendMessage)

    def onJoinRoom(self):
        if Room.isBusy:
            QMessageBox.information(self.btn, "Warning",
                                    "You should exit Room" + str(Room.cur_roomId + 1) + " first!")
            return
        if self.size >= 10:
            QMessageBox.information(self.btn, "Warning", "This room is full!")
        else:
            Room.isBusy = True
            Room.cur_roomId = self.roomId
            self.setWindowTitle("Welcome to Room" + str(self.roomId + 1))
            self.show()
            self.increment()
            # 发送“加入房间”的消息
            msg = {"type": 1, "name": "", "body": Room.cur_roomId}
            data = json.dumps(msg).encode()
            Room.client_socket.send(data)

    def closeEvent(self, *args, **kwargs):
        super().closeEvent(*args, **kwargs)
        Room.isBusy = False
        self.decrement()
        # 发送“退出房间信息”
        msg = {"type": 2, "name": "", "body": Room.cur_roomId}
        data = json.dumps(msg).encode()
        Room.client_socket.send(data)
        Room.cur_roomId = -1

    def sendMessage(self):
        text = self.textEdit.toPlainText()
        if text == "":
            QMessageBox.information(None, "Warning", "Can not send null message!")
            return
        Time = time.strftime(' %Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        self.message.append(Room.user_name + Time)
        self.message.append(text + "\n")

        # 发送消息
        msg = {"type": 3, "sender": Room.user_name, "time": Time, "body": text}
        data = json.dumps(msg).encode()
        Room.client_socket.send(data)
        self.textEdit.clear()

    def onProgressChanged(self):
        self.size = self.progressBar.value()
        if self.size < 3:
            self.progressBar.setStyleSheet(Room.style1)
        else:
            self.progressBar.setStyleSheet(Room.style2)

    def increment(self):
        self.size += 1
        self.progressBar.setValue(self.size)

    def decrement(self):
        self.size -= 1
        self.progressBar.setValue(self.size)

