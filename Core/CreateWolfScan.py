import requests

class WolfCoin(object):
    def __init__(self):
        self.get_user_info_api = "https://plat.wgpsec.org/api/user/getUserInfo"
        self.headers = {
            "authorization": "69a95054d2ef850742bb4a7e63d219f5-20200906093015900-707077"
        }

    def requests_get_user_info_api(self):
        get_user_info_res = requests.get(url=self.get_user_info_api, headers=self.headers).json()
        print(get_user_info_res['data']['wolfCoin'])


a = WolfCoin()
a.requests_get_user_info_api()

class CreatWolfScan(object):
    def __init__(self):
        self.create_wolf_scan_api = "https://plat.wgpsec.org/api/wscan/saveUserWsJob"
        self.headers = {

        }