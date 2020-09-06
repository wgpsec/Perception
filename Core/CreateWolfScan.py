import os
import sys
import configparser
import requests


class WolfScan(object):
    def __init__(self):
        self.get_user_info_api = "https://plat.wgpsec.org/api/user/getUserInfo"
        self.create_wolfscan_api = "https://plat.wgpsec.org/api/wscan/saveUserWsJob"
        self.query_productlist_api = "https://plat.wgpsec.org/api/shop/queryProductList"
        self.take_order_api = "https://plat.wgpsec.org/api/shop/takeOrder"
        self.order_pay_api = "https://plat.wgpsec.org/api/shop/orderPay"
        self.config_file = 'config.conf'

    def get_user_token(self):
        user_token = ''
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)
            try:
                user_token = config['token']['token']
            except:
                sys.exit(0)
        return user_token

    def requests_get_user_info_api(self):
        headers = {
            "authorization": self.get_user_token()
        }
        get_user_info_res = requests.get(url=self.get_user_info_api, headers=headers).json()
        # print(get_user_info_res)
        if get_user_info_res['code'] == 2000:
            print('\033[34m[INFO]\033[0m 您的狼币数量为: ' + str(get_user_info_res['data']['wolfCoin']))
            return get_user_info_res['data']['wolfCoin']
        elif get_user_info_res['code'] == 4018:
            print('\033[33m[WARN]\033[0m ' + get_user_info_res['msg'])
        else:
            print('\033[31m[ERRO]\033[0m')

    def requests_create_wolfscan_api(self, detected_url):
        if self.requests_get_user_info_api() == 0.0:
            print('\033[34m[INFO]\033[0m 您的狼币已经使用完了哦，请投稿高质量文章获取哦!')
            sys.exit(0)
        headers = {
            "authorization": self.get_user_token()
        }
        data = {
            "domain": detected_url,
            "area": "cn",
            "domainOption": "0"
        }
        create_wolfscan_api_res = requests.post(url=self.create_wolfscan_api, headers=headers, json=data).json()
        # print(create_wolfscan_api_res)  # debug
        if create_wolfscan_api_res['code'] == 2000:
            print('\033[32m[SUCC] 任务添加完成!\033[0m')
        elif create_wolfscan_api_res['code'] == 4018:
            print('\033[33m[WARN]\033[0m 登陆过期，请重新登陆')
            sys.exit(0)
        elif create_wolfscan_api_res['code'] == 5001:
            if create_wolfscan_api_res['msg'] == '无法添加已经存在的任务！':
                print('\033[33m[WARN]\033[0m ' + create_wolfscan_api_res['msg'])
                print('\033[34m[INFO]\033[0m 感谢您的使用!')
                sys.exit(0)
            print('\033[33m[WARN]\033[0m ' + create_wolfscan_api_res['msg'])
            YorNPurchase = str(input('\033[34m[INFO]\033[0m 是否需要激活或购买次数? [\033[32mY\033[0m/\033[31mN\033[0m] '))
            if YorNPurchase == 'Y' or YorNPurchase == 'y':
                self.purchase_scans()
            else:
                print('\033[34m[INFO]\033[0m 感谢您的使用!')
                sys.exit(0)

    def purchase_scans(self):
        headers = {
            "authorization": self.get_user_token()
        }
        take_order_data = {
            "num":"1",
            "orderRemark": "",
            "productId": "wPlatP-wolfscan"
        }
        take_order_res = requests.post(url=self.take_order_api, headers=headers, json=take_order_data).json()
        if take_order_res['code'] == 4018:
            print('\033[33m[WARN]\033[0m ' + take_order_res['msg'])
            sys.exit(0)
        elif take_order_res['code'] == 5001:
            print('\033[33m[WARN]\033[0m ' + take_order_res['msg'])
            sys.exit(0)
        order_pay_data = {
            "orderId": take_order_res['data']['orderId']
        }
        order_pay_res = requests.post(url=self.order_pay_api, headers=headers, json=order_pay_data).json()
        # print(order_pay_res)
        if order_pay_res['code'] == 2000:
            print('\033[032m[SUCC]\033[0m wolfscan扫描器服务购买成功!')
        query_productlist_data = {
            "pageNo": "1",
            "pageSize": "12",
            "product": {
            }
        }
        query_productlist_res = requests.post(url=self.query_productlist_api,
                                              headers=headers,
                                              json=query_productlist_data).json()
        if query_productlist_res['code'] == 4018:
            print('\033[33m[WARN]\033[0m ' + query_productlist_res['msg'])
            sys.exit(0)
        for data in query_productlist_res['data']['productVoList']:
            if data['productId'] == 'wPlatP-wolfscan':
                print('\033[34m[INFO]\033[0m wolfscan扫描器服务库存还有: ' + str(data['productSize']))  # wolfscan扫描服务的库存数量

