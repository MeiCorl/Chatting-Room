import json
import winsound
from threading import Thread

import time


class ReceiveThread(Thread):
    def __init__(self, client_socket, register_signal, login_signal,
                 update_ChattingHall_signal_1, update_ChattingHall_signal_2,
                 update_message_signal, personal_message_signal,
                 add_new_friend_signal, request_friend_info_signal):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.register_signal = register_signal
        self.login_signal = login_signal
        self.update_ChattingHall_signal_1 = update_ChattingHall_signal_1
        self.update_ChattingHall_signal_2 = update_ChattingHall_signal_2
        self.update_message_signal = update_message_signal
        self.personal_message_signal = personal_message_signal
        self.add_new_friend_signal = add_new_friend_signal
        self.request_friend_info_signal = request_friend_info_signal
        self.isExited = False

    def run(self):
        super().run()
        while not self.isExited:
            try:
                msg = self.client_socket.recv(1024)
                data = json.loads(msg)
                if data["type"] == 0:
                    canLogin = data["body"]
                    self.login_signal.emit(canLogin)
                elif data["type"] == 1:
                    room_id = data["body"]
                    self.update_ChattingHall_signal_1.emit(room_id)
                elif data["type"] == 2:
                    room_id = data["body"]
                    self.update_ChattingHall_signal_2.emit(room_id)
                elif data["type"] == 3:
                    winsound.PlaySound("./audio/msg.wav", winsound.SND_ASYNC)
                    sender_name = data["sender"]
                    self.update_message_signal.emit(sender_name + data["time"])
                    self.update_message_signal.emit(data["body"]+"\n")
                elif data["type"] == 4:
                    self.register_signal.emit(data)
                elif data["type"] == 6:
                    winsound.PlaySound("./audio/msg.wav", winsound.SND_ASYNC)
                    self.personal_message_signal.emit(data["sender"], data["sender"]+data["time"], data["body"])
                elif data["type"] == 7:
                    winsound.PlaySound("./audio/system.wav", winsound.SND_ASYNC)
                    time.sleep(1)
                    self.add_new_friend_signal.emit(data)
                else:  # data["type"] == 8
                    self.request_friend_info_signal.emit(data)
            except ConnectionAbortedError:
                return
