import requests
import demjson
import argparse
import sys
import os

print(
'==========================================================================================\n'
'||                                                                                      ||\n'
'||                                                                                      ||\n'
'||  ██       ██                  ████████                                               ||\n'                                          
'|| ░██      ░██  █████  ██████  ██░░░░░░                                       █████    ||\n' 
'|| ░██   █  ░██ ██░░░██░██░░░██░██         █████   █████       ██████  ██████ ██░░░██   ||\n'
'|| ░██  ███ ░██░██  ░██░██  ░██░█████████ ██░░░██ ██░░░██     ██░░░░██░░██░░█░██  ░██   ||\n'
'|| ░██ ██░██░██░░██████░██████ ░░░░░░░░██░███████░██  ░░     ░██   ░██ ░██ ░ ░░██████   ||\n'
'|| ░████ ░░████ ░░░░░██░██░░░         ░██░██░░░░ ░██   ██    ░██   ░██ ░██    ░░░░░██   ||\n'
'|| ░██░   ░░░██  █████ ░██      ████████ ░░██████░░█████  ░██ ░░██████ ░███     █████   ||\n'
'|| ░░       ░░  ░░░░░  ░░      ░░░░░░░░   ░░░░░░  ░░░░░   ░░  ░░░░░░  ░░░     ░░░░░     ||\n'
'||                                                                                      ||\n'
'||                                From www.WgpSec.org                                   ||\n'
'||                           在线信息收集工具 V1.0 By Abao520                              ||\n'
'==========================================================================================\n'
)
# 提示信息
parser = argparse.ArgumentParser()
parser.description=('嗨！你好！\n'
                    '当你看到这里的时候，很高兴你已经成为了我们的一员！\n'
                    '当你第一次运行的时候需要你输入一次你的cookie，方便我们认证，只需要一次哦！')

parser.add_argument("--c", type=str,help="查询的城市")
parser.add_argument("--h", type=str,help="查询的IP")
parser.add_argument("--t", type=str,help="查询网站标题")
parser.add_argument("--p", type=str,help="查询开放特定端口")
args = parser.parse_args()

#判断cookie

path = os.getcwd()
cookie_txt = os.path.exists('cookies.txt')
if cookie_txt == False:
    with open('cookies.txt','w') as f:
        cookies_input = input('你还没有cookie，请先输入你的cookie值：')
        f.write(cookies_input)
        f.close()
else:
    pass

with open('cookies.txt','r+') as f:
    cookies_read = f.read()
    f.close()

class Search(object):

    def __init__(self):
        pass

    # 城市查询
    def city(self,city,pageSize=20):
        api_url = 'https://plat.wgpsec.org/api/v1/ws/search'
        key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
               'subdomainTitle',
               'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "Cookie":cookies_read
        }
        json = {
            "pageNo": 1,
            "pageSize": pageSize,
            "query": "city=%s" %city,
            "type": "web"
        }
        api_reposen = requests.post(api_url, headers=header, json=json)
        api_reposen_json = demjson.decode(api_reposen.text)
        api_data = api_reposen_json['data']  # 提取返回中的data值
        wsPortInfoDtoList = api_data['wsPortInfoDtoList']  # 端口开放情况

        wsSubDomainInfoDtoList = api_data['wsSubDomainInfoDtoList']
        wsSubDomainInfoDtos = wsSubDomainInfoDtoList['wsSubDomainInfoDtos']  # 查询出的域名和子域
        i = 0
        try:
            while i < pageSize:  # 遍历出我们插到的信息
                print('网站标题：：%s\n域名%s' % (wsSubDomainInfoDtos[i][key[9]],wsSubDomainInfoDtos[i][key[1]]))
                print(' ' * 100)
                print(' ' * 100)
                i += 1
        except IndexError:

            print('查询出错')
        finally:
            print('查询成功')
    # 域名查询
    def host(self,host,pageSize=20):
        api_url = 'https://plat.wgpsec.org/api/v1/ws/search'
        key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
               'subdomainTitle',
               'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "Cookie":cookies_read
        }
        json = {
            "pageNo": 1,
            "pageSize": pageSize,
            "query": "ip=%s" %host,
            "type": "web"
        }
        api_reposen = requests.post(api_url, headers=header, json=json)
        api_reposen_json = demjson.decode(api_reposen.text)
        api_data = api_reposen_json['data']  # 提取返回中的data值
        wsPortInfoDtoList = api_data['wsPortInfoDtoList']  # 端口开放情况

        wsSubDomainInfoDtoList = api_data['wsSubDomainInfoDtoList']
        wsSubDomainInfoDtos = wsSubDomainInfoDtoList['wsSubDomainInfoDtos']  # 查询出的域名和子域
        i = 0
        try:
            while i < pageSize:  # 遍历出我们插到的信息
                print('网站标题：：%s\n域名%s' % (wsSubDomainInfoDtos[i][key[9]],wsSubDomainInfoDtos[i][key[1]]))
                print(' ' * 100)
                print(' ' * 100)
                i += 1
        except IndexError:

            print('')
        finally:
            print('查询成功')
    # 标题查询
    def title(self,title,pageSize=20):
        api_url = 'https://plat.wgpsec.org/api/v1/ws/search'
        key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
               'subdomainTitle',
               'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "Cookie":cookies_read
        }
        json = {
            "pageNo": 1,
            "pageSize": pageSize,
            "query": "title=%s" %title,
            "type": "web"
        }
        api_reposen = requests.post(api_url, headers=header, json=json)
        api_reposen_json = demjson.decode(api_reposen.text)
        api_data = api_reposen_json['data']  # 提取返回中的data值
        wsPortInfoDtoList = api_data['wsPortInfoDtoList']  # 端口开放情况
        wsSubDomainInfoDtoList = api_data['wsSubDomainInfoDtoList']
        wsSubDomainInfoDtos = wsSubDomainInfoDtoList['wsSubDomainInfoDtos']  # 查询出的域名和子域
        i = 0
        try:
            while i < pageSize:  # 遍历出我们插到的信息
                print('网站标题：：%s\n域名%s' % (wsSubDomainInfoDtos[i][key[9]], wsSubDomainInfoDtos[i][key[1]]))
                print(' '*100)
                print(' ' * 100)

                i += 1
        except IndexError:

            print('')
        finally:
            print('查询成功')




if args.c:
    city_ = Search()
    city_.city(args.c)
if args.h:
    host_ = Search()
    host_.host(args.h)
if args.t:
    title_ = Search()
    title_.host(args.t)

