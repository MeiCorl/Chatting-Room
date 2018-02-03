from ftplib import FTP


class Ftp:
    host = "172.19.156.2"
    username = "meicorl"
    password = "756614"

    def __init__(self):
        self.ftp = FTP()
        self.ftp.encoding = 'UTF-8'
        self.ftp.connect(Ftp.host, 21)
        self.ftp.login(Ftp.username, Ftp.password)

    # 从ftp下载文件
    def downloadfile(self, remotepath, localpath):
        bufsize = 1024
        fp = open(localpath, 'wb')
        self.ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
        self.ftp.set_debuglevel(0)
        fp.close()

    # 从本地上传文件到ftp
    def uploadfile(self, remotepath, localpath):
        bufsize = 1024
        fp = open(localpath, 'rb')
        self.ftp.storbinary('STOR ' + remotepath, fp, bufsize)
        self.ftp.set_debuglevel(0)
        fp.close()

    def quit(self):
        self.ftp.quit()

"""
    uploadfile(ftp, "/home/meicorl/ChatServer/image/b.jpg", "./image/b.jpg")
    downloadfile(ftp, "/home/meicorl/ChatServer/image/xiaoxiao.png", "./xiaoxiao.png")
"""
