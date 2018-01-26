import json
from threading import Thread
import time
import winsound


class ReceiveThread(Thread):
    def __init__(self, client_socket, register_signal, login_signal, update_ChattingHall_signal_1,
                 update_ChattingHall_signal_2, update_message_signal):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.register_signal = register_signal
        self.login_signal = login_signal
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
                    sender_name = data["name"]
                    self.update_message_signal.emit(sender_name + time.strftime(' %H:%M:%S', time.localtime(time.time())))
                    self.update_message_signal.emit(data["body"])
                else:
                    self.register_signal.emit(data["body"])
            except ConnectionAbortedError:
                return
