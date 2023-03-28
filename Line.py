# !/usr/bin/python
# coding:utf-8

# !/usr/bin/python
# coding:utf-8

import smbus
import time
import requests
from ctypes import c_short


def lineNotifyMessage(token, msg):
  headers = { "Authorization": "Bearer " + token,"Content-Type" : "application/x-www-form-urlencoded" }
  payload = {'message': msg}
  r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
  return r.status_code

def main():


  # 傳送訊息字串
  message = "\n溫度 : "+ str(1)+ " ℃\n壓力 : "+ str(2)+ " mbar\n高度 : "+str(3)+ " m"

  # 修改成你的Token字串
  token = 'Xjjz5IfLXKnoOzOwRnu3pnpQvVCN6fQsFL44Zy6Bv51'
  lineNotifyMessage(token, message)
# time.sleep(2)

if __name__=="__main__":
  main()
  time.sleep(2)
