#!/usr/bin/python3

"""
WgpSec Plat Tool
"""

import os
from getpass import getpass
import argparse
import requests
import search

WGPSEC_BANNER = """
==========================================================================================
||                                                                                      ||
||                                                                                      ||
||  ██       ██                  ████████                                               ||                     
|| ░██      ░██  █████  ██████  ██░░░░░░                                       █████    ||
|| ░██   █  ░██ ██░░░██░██░░░██░██         █████   █████       ██████  ██████ ██░░░██   ||
|| ░██  ███ ░██░██  ░██░██  ░██░█████████ ██░░░██ ██░░░██     ██░░░░██░░██░░█░██  ░██   ||
|| ░██ ██░██░██░░██████░██████ ░░░░░░░░██░███████░██  ░░     ░██   ░██ ░██ ░ ░░██████   ||
|| ░████ ░░████ ░░░░░██░██░░░         ░██░██░░░░ ░██   ██    ░██   ░██ ░██    ░░░░░██   ||
|| ░██░   ░░░██  █████ ░██      ████████ ░░██████░░█████  ░██ ░░██████ ░███     █████   ||
|| ░░       ░░  ░░░░░  ░░      ░░░░░░░░   ░░░░░░  ░░░░░   ░░  ░░░░░░  ░░░     ░░░░░     ||
||                                                                                      ||
||                                From www.WgpSec.org                                   ||
||                                在线信息收集工具 V1.1                                    ||
==========================================================================================
"""

def login():
    #  创建用户token存放
    if not os.path.exists('.user_token'):
        with open('.user_token', 'w') as f:
            f.close()
    _user_cookie = None
    # 判断cookie是否生效
    with open('.user_token', 'r+') as f:
        _user_cookie = f.read()
        f.close()
    
    # validate cookie
    validate = requests.post(
        'https://plat.wgpsec.org/api/v1/ws/search',
        headers = {
            'Authorization': _user_cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
        },
        json = {
            'pageNo': 1,
            'pageSize': 20,
            'query': 'city=上海',
            'type': 'web'
        }
    )
    yz_return = validate.json()
    if yz_return['code'] == '2000':
        print('Token 验证成功')
    else:
        if int(yz_return['code']) == 4001 or int(yz_return['code'] == 4018):
            print('未登录或者登录超时，请重新登录！')
            user_name = input('输入你的账号：')
            user_passwd = getpass()
            # 登录获取token
            login_json = {
                "userName": user_name,
                "userPassword": user_passwd,
                "captcha": "dqdq",
                "type": 0
            }
            login_api = 'https://plat.wgpsec.org/api/user/passwordLogin'
            login_api_return_json = requests.post(login_api, json=login_json).json()
            login_token = login_api_return_json['data']['token']

            if int(login_api_return_json['code']) == 5001:
                print('密码或用户名错误，重新登录')
                return None
            elif int(login_api_return_json['code']) == 2000:
                # 写入cookie
                print('Token 验证成功！')
                with open('.user_token', 'w') as f:
                    f.write(login_token)
                    f.close()
                    return login_token
        else:
            print('Token 验证成功！')

    return _user_cookie

def main():
    print(WGPSEC_BANNER)

    user_cookie = login()
    if user_cookie is None:
        return
    
    page_size = 10
    # settings: page size
    if not os.path.exists('pageSize.cfg'):
        with open('pageSize.cfg', 'w') as f:
            page_size = input('输入你想查询的默认条数：')
            f.write(page_size)
            f.close()
    else:
        # print('token验证成功')
        with open('pageSize.txt', 'r+') as f:
            page_size = int(f.read())
            f.close()
        if int(page_size) > 99:
            print('查询的条数超过100，请手动修改pageSize.cfg文件，建议改为99，避免出错')
            return

    parser = argparse.ArgumentParser()
    parser.description = ('嗨！你好！\n'
                          '当你看到这里的时候，很高兴你已经成为了我们的一员！\n'
                          '当你第一次运行的时候需要你输入一次你的cookie，方便我们认证，只需要一次哦！')
    arg_group = parser.add_mutually_exclusive_group()
    arg_group.add_argument('-c', '--city', type=str, help="查询的城市")
    arg_group.add_argument('-i', '--ip', type=str, help="查询的IP")
    arg_group.add_argument('-t', '--title', type=str, help="查询网站标题")
    parser.add_argument("-p", '--port', type=int, help="查询开放特定端口")

    args = parser.parse_args()

    se = search.Search(user_cookie, page_size)
    if args.city:
        se.city(args.c)
    elif args.ip:
        if args.ip == '127.0.0.1':
            print('输入的是局域网地址，无法查询')
            return
        else:
            if args.port:
                se.ip_port(args.h, args.p)
            else:
                se.host(args.h)
    elif args.title:
        se.title(args.t)
    elif args.port:
        if int(args.p) > 65535 or int(args.p) < 0:
            print('输入的端口范围不正确')
            return
        else:
            se.port(args.p)

if __name__ == '__main__':
    main()
