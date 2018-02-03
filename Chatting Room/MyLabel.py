from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QMessageBox

from FriendWind import FriendWind


class MyLabel(QWidget):
    """ a widget contains a picture and two line of text """
    def __init__(self, title, subtitle, icon_path):
        """
        :param title: str title
        :param subtitle: str subtitle
        :param icon_path: path of picture
        """
        super(MyLabel, self).__init__()
        self.lb_title = QLabel(title)
        self.lb_title.setFont(QFont("Arial", 16, QFont.Bold))
        self.lb_subtitle = QLabel(subtitle)
        self.lb_subtitle.setFont(QFont("Arial", 12, QFont.StyleItalic))
        self.lb_icon = QLabel()
        self.lb_icon.setFixedSize(45, 45)
        pixMap = QPixmap(icon_path).scaled(self.lb_icon.width(), self.lb_icon.height())
        self.lb_icon.setPixmap(pixMap)
        self.init_ui()

        self.friend = FriendWind(self.lb_title.text(), self.lb_subtitle.text(), icon_path)

    def mouseDoubleClickEvent(self, QMouseEvent):
        super().mouseDoubleClickEvent(QMouseEvent)
        self.friend.show()

    def addMessage(self, sender_time, msg):
        self.friend.addMessage(sender_time, msg)

    def init_ui(self):
        """handle layout"""
        ly_main = QHBoxLayout()
        ly_right = QVBoxLayout()
        ly_right.addWidget(self.lb_title)
        ly_right.addWidget(self.lb_subtitle)
        ly_right.setAlignment(Qt.AlignVCenter)
        ly_main.addWidget(self.lb_icon)
        ly_main.addLayout(ly_right)
        self.setLayout(ly_main)
        self.resize(90, 85)

    def get_lb_title(self):
        return self.lb_title.text()

    def get_lb_subtitle(self):
        return self.lb_subtitle.text()

    def closeWindow(self):
        self.friend.close()
