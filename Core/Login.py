import requests
import random
import sys
import configparser
import getpass
import re
from .CheckRealLogin import Check
from getpass import getpass


class Login(object):
    def __init__(self):
        self.login_api = "https://plat.wgpsec.org/api/user/passwordLogin"
        self.config_file = 'config.conf'

    def verify(self, username):
        if not Check().run():  # 登陆就为True
            if username == None:
                print('\033[33m[WARN]\033[0m 请使用-l参数进行登陆!')
                sys.exit(0)


        login_api = self.login_api
        config = configparser.ConfigParser()
        requests_type = 0
        # username = str(input('\033[34m[INFO]\033[0m 请输入您的账号: '))
        # print(username)
        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', username):
            requests_type = 1
        else:
            pass
        password = getpass('\033[34m[INFO]\033[0m 请输入账号密码(Tips:不可见): ')
        if password == '':
            print('\033[33m[WARN]\033[0m 密码不能为空!')
            sys.exit(0)
        login_data = {
            "userName": username,
            "userPassword": password,
            "captcha": random.randint(0, 65535),
            "type": requests_type
        }
        login_api_res = requests.post(login_api, json=login_data).json()
        login_res_code = int(login_api_res['code'])  # 返回状态码
        if login_res_code == 5001:
            print('\033[31m[ERRO]\033[0m 密码或用户名错误，请重新登录!')
            sys.exit(0)
        login_token = login_api_res['data']['token']
        if login_res_code == 2000:
            print('\033[032m[SUCC]\033[0m 登陆成功!')
            config['token'] = {'token': login_token}
            with open('config.conf', 'w') as config_file:
                config.write(config_file)

