import requests
import os


#上传文件到服务器
file = {'file': open('image/雪女.jpg','rb')}
r = requests.post('http://172.19.156.2:8000/upload', files=file)
print(r.text)