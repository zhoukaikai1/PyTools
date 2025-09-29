import requests
import time
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
import datetime

# 艺术字签名
print("""
[周]  星河璀璨
███████╗ ██████╗ ██╗   ██╗██╗   ██╗███████╗
██╔════╝██╔═══██╗██║   ██║██║   ██║██╔════╝
█████╗  ██║   ██║██║   ██║██║   ██║███████╗
██╔══╝  ██║   ██║╚██╗ ██╔╝██║   ██║╚════██║
██║     ╚██████╔╝ ╚████╔╝ ╚██████╔╝███████║
╚═╝      ╚═════╝   ╚═══╝   ╚═════╝ ╚══════╝
""",
      "=============================="
      "搞了这么久，属个名可以吧"
      "==============================")


# 工具函数
def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def encrypt_password(password, key_hex="4b316e67626173654032303234303031"):
    key = binascii.unhexlify(key_hex)
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(password.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return encrypted.hex()
def random_sleep(min_sec=30, max_sec=90):
    wait_time = random.randint(min_sec, max_sec)
    print(f"[{get_timestamp()}] 随机等待 {wait_time} 秒...")
    for remaining in range(wait_time, 0, -1):
        print(f"\r剩余等待时间: {remaining}秒", end="")
        time.sleep(1)
    print("\n")


class KingbaseSigner:
    def __init__(self, username, password):
        self.username = username
        self.password = encrypt_password(password)
        self.session = requests.Session()
        self.token = None
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://bbs.kingbase.com.cn",
            "referer": "https://bbs.kingbase.com.cn/login",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0"
        }
    def login(self):
        url = 'https://bbs.kingbase.com.cn/web-api/web/system/user/loginWeb'
        data = {
            "username": self.username,
            "password": self.password,
            "code": None,
            "loginMethod": "account",
            "phoneNumber": None,
            "email": None
        }
        response = self.session.post(url=url, headers=self.headers, json=data)
        if response.status_code == 200:
            self.token = response.json().get('data')
            return True
        return False
    def get_user_info(self):
        url = 'https://bbs.kingbase.com.cn/web-api/web/system/user/getCurrRankInfo'
        headers = self.headers.copy()
        headers["authorization"] = f"Bearer {self.token}"
        response = self.session.get(url=url, headers=headers)
        if response.status_code == 200:
            data = response.json().get('data', {})
            return {
                'username': data.get('userName'),
                'experience': data.get('experience'),
                'level': data.get('userLevelDesc'),
                'integral': data.get('integral')
            }
        return None
    def sign_in(self):
        url = 'https://bbs.kingbase.com.cn/web-api/web/system/user/getSignData'
        headers = self.headers.copy()
        headers["authorization"] = f"Bearer {self.token}"
        response = self.session.get(url=url, headers=headers)
        if response.status_code == 200:
            data = response.json().get('data', {})
            return {
                'sign_times': data.get('signTimes'),
                'change_integral': data.get('changeIntegral')
            }
        return None
    def post_comment(self):
        url = 'https://bbs.kingbase.com.cn/web-api/web/forum/comment'
        data = {
            "articleId": "01da3c543af10276fd650b89c9ed2774",
            "commentContent": "<p><img src=\"/UEditorPlus/dialogs/emotion/./custom_emotion/emotion_02.png\"></p>"
        }
        headers = self.headers.copy()
        headers["authorization"] = f"Bearer {self.token}"
        response = self.session.post(url=url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        return None
def main():
    print("""
        - 遇到敏感词，会签到失败，请调整后，重新签到；
        - 每天建议启动5次，可以获得五次积分
    """)

    username = input('请输入用户名：')
    password = input("请输入密码：")

    signer = KingbaseSigner(username, password)

    if not signer.login():
        print(f"[{get_timestamp()}] 登录失败，请检查网络或账号信息")
        return

    # 获取用户信息
    user_info = signer.get_user_info()
    if user_info:
        print(
            f"[{get_timestamp()}] 账户 {user_info['username']}，经验 {user_info['experience']}，等级 {user_info['level']}")
    sign_info = signer.sign_in()
    if sign_info:
        print(
            f"[{get_timestamp()}] 签到第 {sign_info['sign_times']} 天，积分 +{sign_info['change_integral']}，总积分 {user_info['integral']}")
    for a in range(4):
        comment_result = signer.post_comment()
        if comment_result:
            msg = comment_result.get('msg', '')
            data = comment_result.get('data', {})
            print(
                f"[{get_timestamp()}] 今日社区打卡 {msg}，时间：{data.get('createTime', '')}，敏感词：{data.get('remark', '无')}")
        # 如果不是最后一次循环，则等待随机时间
        if a < 5:
            random_sleep(30, 90)  # 30-90秒随机等待
    print(
        f"[{get_timestamp()}] ，总积分 {user_info['integral']}")
    print("\n===== 所有任务完成 =====")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[{get_timestamp()}] 发生错误: {str(e)}")
