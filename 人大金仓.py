
print("""
[周]  星河璀璨
███████╗ ██████╗ ██╗   ██╗██╗   ██╗███████╗
██╔════╝██╔═══██╗██║   ██║██║   ██║██╔════╝
█████╗  ██║   ██║██║   ██║██║   ██║███████╗
██╔══╝  ██║   ██║╚██╗ ██╔╝██║   ██║╚════██║
██║     ╚██████╔╝ ╚████╔╝ ╚██████╔╝███████║
╚═╝      ╚═════╝   ╚═══╝   ╚═════╝ ╚══════╝
""")

import requests
# -*- coding: utf-8 -*-
# Author: James Zhou
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
print(
    "#############################"
    "搞了这么久，属个名可以吧"
    "#############################"

)

def encrypt_password(password, key_hex="4b316e67626173654032303234303031"):
    key = binascii.unhexlify(key_hex)
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(password.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return encrypted.hex()

username = input('请输入用户名：')
passwd = input("请输入密码：")
passwd = encrypt_password(passwd)
# username = "James zhou" # OceanBase社区，金仓社区同名
print(username,passwd)

url1 = 'https://bbs.kingbase.com.cn/web-api/web/system/user/loginWeb'
data1 = {
  "username": username,
  "password": passwd,
  "code": None,
  "loginMethod": "account",
  "phoneNumber": None,
  "email": None
}
headers1 = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN",
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://bbs.kingbase.com.cn",
    "referer": "https://bbs.kingbase.com.cn/login",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0"
}
session = requests.session()
response = session.post(url=url1, headers=headers1, json=data1)
response.encoding = 'utf-8'
# print(response.status_code)
if response.status_code != 200:
    print("检测网络")
else:
    msg = response.json()['msg']
    print("网络连接成功，签到{}".format(msg))
    # print(response.text)
    token = response.json()['data']
    url2 = 'https://bbs.kingbase.com.cn/web-api/web/system/user/getCurrRankInfo'
    header2 = {
        "accept": "application/json, text/plain, */*",
        "authorization": f"Bearer {token}",  # 必须添加的认证头
        "referer": "https://bbs.kingbase.com.cn/vipcenter",
        "user-agent": headers1["user-agent"]
    }


    response2 = session.get(url=url2, headers=header2, timeout=10)
    # print(response2.text)
    username = response2.json()['data']['userName']
    experience = response2.json()['data']['experience']
    userLevelDesc = response2.json()['data']['userLevelDesc']
    integral = response2.json()['data']['integral']

    print("账户{}，经验{}，等级{}".format(username,experience, userLevelDesc))

    url3 = 'https://bbs.kingbase.com.cn/web-api/web/system/user/getSignData'
    response3 = session.get(url=url3, headers=header2.copy(), timeout=10)
    # print(response3.text)
    signTimes = response3.json()['data']['signTimes']
    changeIntegral = response3.json()['data']['changeIntegral']
    print("签到第{}天， 积分+{}， 总积分{}".format(signTimes,changeIntegral,integral))




