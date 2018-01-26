class Message:
    def __init__(self, msg_type, name="", body=""):
        self.type = msg_type    # 消息类型
        self.name = name        # 发消息人
        self.body = body        # 消息内容(当type值为1和2时，body为房间ID)

"""
   发送消息type  -->  0: 登录
                      1: 加入房间
                      2: 退出房间
                      3: 发送新消息
                      4： 注册
                      
   接收消息type  -->  0: 对登录消息的回复
                      1: 有人加入房间，需更新房间人数（+1）
                      2: 有人退出房间，需更新房间人数（-1）
                      3: 收到新消息
                      4: 对注册消息的回复
"""