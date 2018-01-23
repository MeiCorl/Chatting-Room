""""
  @Name: ChatClient.py
  @Author: MeiCorl
  图形界面与逻辑相分离，在这个文件内编写操作函数
"""
import _thread
import json
import sys
from socket import socket

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

from ReceiveThread import ReceiveThread
from Room import Room
from UI.MainWindow import Ui_ChattingRoom


class ChattingHall(QtWidgets.QMainWindow, Ui_ChattingRoom):
    client_socket = None
    server_address = ("172.19.156.2", 1234)
    isConnected = False  # 是否成功连接服务器
    init_progressbar_signal = QtCore.pyqtSignal(list)
    update_ChattingHall_signal_1 = QtCore.pyqtSignal(int)
    update_ChattingHall_signal_2 = QtCore.pyqtSignal(int)
    update_message_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(ChattingHall, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        # 添加信号槽函数
        self.userName.textEdited.connect(self.onEdit)
        self.loginButton.clicked.connect(self.onLogin)
        self.logoutButton.clicked.connect(self.onLogout)
        self.exitButton.clicked.connect(self.close)
        self.init_progressbar_signal.connect(self.__InitProgressbar)
        self.update_ChattingHall_signal_1.connect(self.__increment)
        self.update_ChattingHall_signal_2.connect(self.__decrement)
        self.update_message_signal.connect(self.__updateMessage)

        self.roomList = []
        self.__InitRoom()

    def __InitProgressbar(self, ls):
        self.progressBar_1.setValue(ls[0])
        self.progressBar_2.setValue(ls[1])
        self.progressBar_3.setValue(ls[2])
        self.progressBar_4.setValue(ls[3])
        self.progressBar_5.setValue(ls[4])
        self.progressBar_6.setValue(ls[5])

    def __increment(self, room_id):
        self.roomList[room_id].increment()

    def __decrement(self, room_id):
        self.roomList[room_id].decrement()

    def __updateMessage(self, msg):
        self.roomList[Room.cur_roomId].message.append(msg)

    def __InitRoom(self):
        self.roomList.append(Room(0, self.pushButton_1, 4, self.progressBar_1))
        self.roomList.append(Room(1, self.pushButton_2, 0, self.progressBar_2))
        self.roomList.append(Room(2, self.pushButton_3, 0, self.progressBar_3))
        self.roomList.append(Room(3, self.pushButton_4, 0, self.progressBar_4))
        self.roomList.append(Room(4, self.pushButton_5, 0, self.progressBar_5))
        self.roomList.append(Room(5, self.pushButton_6, 8, self.progressBar_6))
        #   开启新线程连接服务器以免阻塞主界面
        _thread.start_new_thread(self.connectServer, ())

    def connectServer(self):
        ChattingHall.client_socket = socket()
        ChattingHall.client_socket.connect(ChattingHall.server_address)
        ChattingHall.isConnected = True
        room_info_msg = ChattingHall.client_socket.recv(1024)
        ls = json.loads(room_info_msg)
        self.init_progressbar_signal.emit(ls)

        # 同一个client下各个room共用一个socket
        Room.client_socket = ChattingHall.client_socket
        #  启动接受消息的线程
        receive_thread = ReceiveThread(ChattingHall.client_socket, self.update_ChattingHall_signal_1,
                                       self.update_ChattingHall_signal_2, self.update_message_signal)
        receive_thread.start()

    def onEdit(self):
        if self.userName.text() != "":
            self.loginButton.setEnabled(True)
        else:
            self.loginButton.setEnabled(False)

    def onLogin(self):
        if not ChattingHall.isConnected:
            QMessageBox.information(self, "Error", "Unable to connect to sever, please restart the program!")
            return
        self.__setEnabled(True)
        self.userName.setEnabled(False)
        self.loginButton.setEnabled(False)
        self.logoutButton.setEnabled(True)
        Room.user_name = self.userName.text()

    def onLogout(self):
        self.__setEnabled(False)
        self.logoutButton.setEnabled(False)
        self.loginButton.setEnabled(True)
        self.userName.setEnabled(True)

    def __setEnabled(self, enable):
        self.pushButton_1.setEnabled(enable)
        self.pushButton_2.setEnabled(enable)
        self.pushButton_3.setEnabled(enable)
        self.pushButton_4.setEnabled(enable)
        self.pushButton_5.setEnabled(enable)
        self.pushButton_6.setEnabled(enable)
        self.progressBar_1.setEnabled(enable)
        self.progressBar_2.setEnabled(enable)
        self.progressBar_3.setEnabled(enable)
        self.progressBar_4.setEnabled(enable)
        self.progressBar_5.setEnabled(enable)
        self.progressBar_6.setEnabled(enable)

    # 添加主窗口关闭响应函数
    def closeEvent(self, event):
        if Room.isBusy:
            QMessageBox.information(self, "Warning", "You must exit room first!")
            event.ignore()
            return
        elif ChattingHall.isConnected:
            ChattingHall.client_socket.close()
        event.accept()

# 主要函数部分
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # 显示客户端主窗口
    win = ChattingHall()
    win.show()

    sys.exit(app.exec_())
