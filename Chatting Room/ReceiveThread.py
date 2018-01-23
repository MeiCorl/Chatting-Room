import json
from threading import Thread

import time


class ReceiveThread(Thread):
    def __init__(self, client_socket, update_ChattingHall_signal_1,
                 update_ChattingHall_signal_2, update_message_signal):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.update_ChattingHall_signal_1 = update_ChattingHall_signal_1
        self.update_ChattingHall_signal_2 = update_ChattingHall_signal_2
        self.update_message_signal = update_message_signal
        self.isExited = False

    def run(self):
        super().run()
        while not self.isExited:
            try:
                msg = self.client_socket.recv(1024)
                data = json.loads(msg)
                if data["type"] == 1:
                    room_id = data["body"]
                    self.update_ChattingHall_signal_1.emit(room_id)
                elif data["type"] == 2:
                    room_id = data["body"]
                    self.update_ChattingHall_signal_2.emit(room_id)
                else:
                    sender_name = data["name"]
                    self.update_message_signal.emit(sender_name + time.strftime(' %H:%M:%S', time.localtime(time.time())))
                    self.update_message_signal.emit(data["body"] + "\n")
            except ConnectionAbortedError:
                return
