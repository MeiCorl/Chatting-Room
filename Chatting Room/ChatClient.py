""""
  @Name: ChatClient.py
  @Author: MeiCorl
  图形界面与逻辑相分离，在这个文件内编写操作函数
"""
import _thread
import json
import sys
import socket

import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QListWidgetItem, QLabel

from FriendWind import FriendWind
from MyLabel import MyLabel
from ReceiveThread import ReceiveThread
from RegisterWind import RegisterWind
from Room import Room
from UI.MainWindow import Ui_ChattingRoom
from ftp import Ftp


class ChattingHall(QtWidgets.QMainWindow, Ui_ChattingRoom):
    client_socket = None
    server_address = ("172.19.156.2", 1234)
    isConnected = False  # 是否成功连接服务器
    init_progressbar_signal = QtCore.pyqtSignal(list)
    update_ChattingHall_signal_1 = QtCore.pyqtSignal(int)
    update_ChattingHall_signal_2 = QtCore.pyqtSignal(int)
    update_message_signal = QtCore.pyqtSignal(str)
    login_signal = QtCore.pyqtSignal(int)
    register_signal = QtCore.pyqtSignal(dict)
    personal_message_signal = QtCore.pyqtSignal(str, str, str)
    add_new_friend_signal = QtCore.pyqtSignal(dict)
    request_friend_info_signal = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(ChattingHall, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        # 关闭状态栏显示
        self.statusbar.close()
        # 设置密码属性
        self.passWord.setEchoMode(QLineEdit.Password)

        # 添加信号槽函数
        self.userName.textEdited.connect(self.onEdit)
        self.loginButton.clicked.connect(self.onLogin)
        self.logoutButton.clicked.connect(self.onLogout)
        self.exitButton.clicked.connect(self.close)
        self.registerButton.clicked.connect(self.__register)
        self.addFriendButton.clicked.connect(self.searchFriend)

        # 添加自定义信号响应函数
        self.init_progressbar_signal.connect(self.__InitProgressbar)
        self.update_ChattingHall_signal_1.connect(self.__increment)
        self.update_ChattingHall_signal_2.connect(self.__decrement)
        self.update_message_signal.connect(self.__updateMessage)
        self.login_signal.connect(self.login)
        self.register_signal.connect(self.onRegister)
        self.personal_message_signal.connect(self.addMessage)
        self.add_new_friend_signal.connect(self.addNewFriend)
        self.request_friend_info_signal.connect(self.updateFriendList)

        self.roomList = []
        self.friendList = {}
        self.__InitRoom()
        #   开启新线程连接服务器以免阻塞主界面
        _thread.start_new_thread(self.connectServer, ())

    def __InitRoom(self):
        self.roomList.append(Room(0, self.pushButton_1, 4, self.progressBar_1))
        self.roomList.append(Room(1, self.pushButton_2, 0, self.progressBar_2))
        self.roomList.append(Room(2, self.pushButton_3, 0, self.progressBar_3))
        self.roomList.append(Room(3, self.pushButton_4, 0, self.progressBar_4))
        self.roomList.append(Room(4, self.pushButton_5, 0, self.progressBar_5))
        self.roomList.append(Room(5, self.pushButton_6, 8, self.progressBar_6))

    def __InitFriendList(self):
        #   初始化好友列表
        self.list.clear()
        self.friendList.clear()
        friendListPath = "./user/" + self.userName.text() + "/friend_list.txt"
        # 如果本地好友列表丢失，则从服务器拉取好友列表
        if not os.path.exists(friendListPath):
            ftp = Ftp()
            ftp.downloadfile("/home/meicorl/ChatServer/user/" + self.userName.text() + "/friend_list.txt",
                             friendListPath)
            ftp.quit()
        if os.path.exists(friendListPath):
            file = open(friendListPath, encoding='UTF-8')
            while 1:
                line = file.readline()
                if not line:
                    break
                friend = json.loads(line)
                self.addFriend(friend["name"], friend["signature"], friend["portrait"])
            file.close()

    def addFriend(self, name, signature, pic_path):
        item_widget = QListWidgetItem()
        item_widget.setSizeHint(QSize(90, 65))
        self.list.addItem(item_widget)
        label = MyLabel(name, signature, pic_path)
        self.friendList[name] = label
        self.list.setItemWidget(item_widget, label)

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

    def addMessage(self, sender_name, sender_time, msg):
        self.friendList[sender_name].addMessage(sender_time, msg)

    def connectServer(self):
        ChattingHall.client_socket = socket.socket()
        ChattingHall.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ChattingHall.client_socket.connect(ChattingHall.server_address)
        ChattingHall.isConnected = True
        room_info_msg = ChattingHall.client_socket.recv(1024)
        ls = json.loads(room_info_msg)
        self.init_progressbar_signal.emit(ls)

        # 同一个client下各个room共用一个socket
        Room.client_socket = ChattingHall.client_socket
        FriendWind.client_socket = ChattingHall.client_socket

        #  启动接受消息的线程
        receive_thread = ReceiveThread(ChattingHall.client_socket, self.register_signal, self.login_signal,
                                       self.update_ChattingHall_signal_1, self.update_ChattingHall_signal_2,
                                       self.update_message_signal, self.personal_message_signal,
                                       self.add_new_friend_signal, self.request_friend_info_signal)
        receive_thread.start()

    def onEdit(self):
        if self.userName.text() != "":
            self.loginButton.setEnabled(True)
        else:
            self.loginButton.setEnabled(False)

    def onRegister(self, response):
        if response["body"] == 1:
            QMessageBox.information(self, "Error", "user name already existed, please change another name!")
        else:
            # 注册成功，上传头像信息
            QMessageBox.information(self, "Congratulations", "Register successfully, go back to login now!")
            ftp = Ftp()
            ftp.uploadfile("/home/meicorl/ChatServer/image/" + os.path.basename(response["portrait"]), response["portrait"])
            # 在本地创建用户目录
            os.mkdir("user/" + response["name"])

    def onLogin(self):
        if not ChattingHall.isConnected:
            QMessageBox.information(self, "Error", "Unable to connect to sever, please restart the program!")
            return
        # 发送“登录”的消息
        msg = {"type": 0, "name": self.userName.text(), "password": self.passWord.text()}
        data = json.dumps(msg).encode()
        ChattingHall.client_socket.send(data)

    def login(self, can_login):
        if can_login == 0:
            self.__login()
        elif can_login == 1:
            reply = QMessageBox.question(self, "Warning", "You have not register yet, please register first!",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.__register()
            else:
                return
        else:
            QMessageBox.information(self, "Error", "incorrect password!")

    def __login(self):
        self.__setEnabled(True)
        Room.user_name = self.userName.text()
        FriendWind.user_name = self.userName.text()
        # 更新窗口标题和Icon
        home_path = "user/" + self.userName.text() + "/self_info.txt"
        if not os.path.exists(home_path):
            ftp = Ftp()
            ftp.downloadfile("/home/meicorl/ChatServer/user/" + self.userName.text() + "/self_info.txt", home_path)
            ftp.quit()
        file = open(home_path, encoding='UTF-8')
        line = file.readline()
        file.close()
        self_info = json.loads(line)
        self.setWindowTitle(self_info["name"] + "(" + self_info["signature"] + ")")
        self.setWindowIcon(QIcon(self_info["portrait"]))
        # 初始化好友列表
        self.list.setEnabled(True)
        self.__InitFriendList()

    def __register(self):
        if not ChattingHall.isConnected:
            QMessageBox.information(self, "Error", "Unable to connect to sever, please restart the program!")
            return
        self.register_win = RegisterWind(ChattingHall.client_socket)
        self.register_win.show()

    def searchFriend(self):
        self_name = self.userName.text()
        friend_name = self.Search_Friend.text()
        msg = {"type": 7, "isResponse": False, "self_name": self_name, "friend_name": friend_name}
        ChattingHall.client_socket.send(json.dumps(msg).encode())
    #   QMessageBox.information(self, "", "The request has been sent. Please wait for confirmation.")
        self.Search_Friend.clear()

    def addNewFriend(self, msg):
        if msg["isResponse"]:  # 加好友应答
            if msg["body"] == -1:
                QMessageBox.information(self, "Error", "User:" + msg["friend_name"] + " does not exist!")
            elif msg["body"] == 0:
                QMessageBox.information(self, "Oh no",
                                        "It's so pity that " + msg["friend_name"] + " refuse to become your friend!")
            else:
                QMessageBox.information(self, "Congratulations", " Now " + msg["friend_name"] + " is your friend!")
                self.requestFriendInfo(msg["friend_name"])
        else:  # 加好友请求
            msg["isResponse"] = True
            box = QMessageBox(QMessageBox.Warning, "Message", msg["self_name"] + " requests to add you as a friend!")
            yes = box.addButton("Accept", QMessageBox.YesRole)
            no = box.addButton("Refuse", QMessageBox.NoRole)
            box.exec()
            if box.clickedButton() == yes:
                msg["body"] = 1
                self.requestFriendInfo(msg["self_name"])
            else:
                msg["body"] = 0
            ChattingHall.client_socket.send(json.dumps(msg).encode())

    def requestFriendInfo(self, friend_name):
        msg = {"type": 8, "friend_name": friend_name}
        ChattingHall.client_socket.send(json.dumps(msg).encode())

    def updateFriendList(self, friendDict):
        # 拉取好友头像
        friend = json.loads(friendDict["friend_info"])
        ftp = Ftp()
        ftp.downloadfile("/home/meicorl/ChatServer/" + friend["portrait"], friend["portrait"])
        ftp.quit()
        self.addFriend(friend["name"], friend["signature"], friend["portrait"])
        #  将新添加的好友信息存入本地文件
        file = open("user/"+self.userName.text()+"/friend_list.txt", "a", encoding="UTF-8")
        file.write(json.dumps(friend))
        file.close()

    def onLogout(self):
        # 关闭好友聊天窗口
        for friend_name in self.friendList:
            self.friendList[friend_name].closeWindow()
        # 更新窗口标题和Icon
        self.setWindowTitle("JJ")
        self.setWindowIcon(QIcon("image/main.jpg"))
        self.__setEnabled(False)
        # 发送“登出”的消息
        msg = {"type": 5, "name": ""}
        data = json.dumps(msg).encode()
        ChattingHall.client_socket.send(data)
        # 更新好友列表
        self.list.setEnabled(False)
        self.list.clear()

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

        self.userName.setEnabled(not enable)
        self.passWord.setEnabled(not enable)
        self.loginButton.setEnabled(not enable)
        self.logoutButton.setEnabled(True)
        self.Search_Friend.setEnabled(enable)
        self.addFriendButton.setEnabled(enable)

    # 添加主窗口关闭响应函数
    def closeEvent(self, event):
        if Room.isBusy:
            QMessageBox.information(self, "Warning", "You must exit room first!")
            event.ignore()
            return
        elif ChattingHall.isConnected:
            ChattingHall.client_socket.close()
            # 关闭好友聊天窗口
            for friend_name in self.friendList:
                self.friendList[friend_name].closeWindow()
        event.accept()


# 主要函数部分
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # 显示客户端主窗口
    win = ChattingHall()
    win.show()

    sys.exit(app.exec_())
