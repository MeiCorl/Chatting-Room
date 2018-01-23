# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RoomWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Room(object):
    def setupUi(self, Room):
        Room.setObjectName("Room")
        Room.resize(441, 463)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/main.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Room.setWindowIcon(icon)
        Room.setStyleSheet("")
        self.textEdit = QtWidgets.QTextEdit(Room)
        self.textEdit.setGeometry(QtCore.QRect(0, 370, 321, 101))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.textEdit.setFont(font)
        self.textEdit.setAutoFillBackground(False)
        self.textEdit.setStyleSheet("")
        self.textEdit.setObjectName("textEdit")
        self.sendButton = QtWidgets.QPushButton(Room)
        self.sendButton.setGeometry(QtCore.QRect(330, 390, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.sendButton.setFont(font)
        self.sendButton.setAutoFillBackground(False)
        self.sendButton.setStyleSheet("background-image: url(:/image/e.jpg);")
        self.sendButton.setIconSize(QtCore.QSize(64, 16))
        self.sendButton.setObjectName("sendButton")
        self.message = QtWidgets.QTextEdit(Room)
        self.message.setEnabled(True)
        self.message.setGeometry(QtCore.QRect(0, 0, 441, 371))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.message.sizePolicy().hasHeightForWidth())
        self.message.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.message.setFont(font)
        self.message.setStyleSheet("background-image: url(:/image/c.jpg);")
        self.message.setReadOnly(True)
        self.message.setObjectName("message")
        self.groupBox = QtWidgets.QGroupBox(Room)
        self.groupBox.setGeometry(QtCore.QRect(0, 370, 441, 101))
        self.groupBox.setStyleSheet("background-image: url(:/image/e.jpg);")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.groupBox.raise_()
        self.message.raise_()
        self.textEdit.raise_()
        self.sendButton.raise_()

        self.retranslateUi(Room)
        QtCore.QMetaObject.connectSlotsByName(Room)

    def retranslateUi(self, Room):
        _translate = QtCore.QCoreApplication.translate
        Room.setWindowTitle(_translate("Room", "Dialog"))
        self.sendButton.setText(_translate("Room", "Send"))

import img_rc
