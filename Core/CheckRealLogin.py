import sys

import requests
import configparser
import os


class Check(object):
    def __init__(self):
        self.requests_api = 'https://plat.wgpsec.org/api/v1/ws/search'
        self.config_file = 'config.conf'
        self.data = {
            "pageNo": 1,
            "pageSize": 100,
            "query": "city=武汉",
            "type": "web"
        }

    def get_user_token(self):
        user_token = ''
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)
            try:
                user_token = config['token']['token']
            except:
                return
        return user_token

    def run(self):
        user_token = self.get_user_token()
        if user_token == None:
            return False
        else:
            headers = {
                "authorization": user_token,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
            }
            res = requests.post(self.requests_api, json=self.data, headers=headers).json()
            if res['code'] == 4018:
                return False
            else:
                print('\033[33m[WARN]\033[0m 您已登陆，无须继续登陆')
                return True


# a = Check()
# a.run()