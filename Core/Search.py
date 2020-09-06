import csv
import os
import configparser
import sys
import time

import requests


class Search(object):

    def __init__(self):
        self.search_api_url = 'https://plat.wgpsec.org/api/v1/ws/search'  # 搜索模块api链接
        self.knowledge_api_url = 'https://plat.wgpsec.org/api/post/queryPlatPost'  # 知识库api链接
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

    def search_data(self, type, input_data):
        data = {
            "pageNo": 1,
            "pageSize": 100,
            "query": input_data,
            "type": type
        }
        return data

    def requests_search_api(self, type, input_data, export_filename):
        search_api_url = self.search_api_url
        user_token = self.get_user_token()
        headers = {
            "authorization": user_token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
        }
        search_data = self.search_data(type=type, input_data=input_data)
        requests_res = requests.post(url=search_api_url, headers=headers, json=search_data).json()
        if requests_res['code'] == 4018:
            print("\033[31m[ERRO]\033[0m " + requests_res['msg'])
            sys.exit(0)
        if type == 'web':
            search_info = requests_res['data']['wsSubDomainInfoDtoList']['wsSubDomainInfoDtos']
            if len(search_info) == 0:
                print('\033[33m[WARN]\033[0m 未查询到信息!')
                sys.exit(0)
            print('\033[32m[SUCC]\033[0m 查询成功')
            self.web_print_data(search_info, export_filename)
        else:
            search_info = requests_res['data']['wsPortInfoDtoList']['wsPortInfoDtos']
            if len(search_info) == 0:
                print('\033[33m[WARN]\033[0m 未查询到信息!')
                sys.exit(0)
            print('\033[32m[SUCC]\033[0m 查询成功')

            self.host_print_data(search_info, export_filename)
        # print(search_info)

    def web_print_data(self, search_info, export_filename):
        for i in range(0, len(search_info)):
            if search_info[i]['subdomainTitle'] == None:
                search_info[i]['subdomainTitle'] = 'Unknow'
            if search_info[i]['subdomainBanner'] == None:
                search_info[i]['subdomainBanner'] = 'Unknow'
            print('\033[34m[INFO] \033[0m' +
                  '\033[33mTitle:\033[0m[' + search_info[i]['subdomainTitle'] + ']',
                  '\033[33mSubdomain:\033[0m[' + search_info[i]['subdomain'] + ']',
                  '\033[33mIPADDR:\033[0m[' + search_info[i]['ipAdd'] + ']',
                  '\033[33mWeb servers:\033[0m[' + search_info[i]['subdomainBanner'] + ']')
        if export_filename != '':
            print('\033[33m[INFO]\033[0m 查询结果保存至: %s' % ('./Output/' + export_filename))
            with open('Output/%s' % export_filename, 'a', newline='') as csvfile:
                fieldnames = ['网站标题', '域名', 'IP地址', 'Web容器']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(0, len(search_info)):
                    if search_info[i]['subdomainTitle'] == None:
                        search_info[i]['subdomainTitle'] = 'Unknow'
                    if search_info[i]['subdomainBanner'] == None:
                        search_info[i]['subdomainBanner'] = 'Unknow'
                    result = {
                        '网站标题': search_info[i]['subdomainTitle'],
                        '域名': search_info[i]['subdomain'],
                        'IP地址': search_info[i]['ipAdd'],
                        'Web容器': search_info[i]['subdomainBanner']
                    }
                    writer.writerow(result)
            csvfile.close()

    def host_print_data(self, search_info, export_filename):
        for i in range(0, len(search_info)):
            if search_info[i]['product'] == '':
                search_info[i]['product'] = 'Unknow'
            print('\033[34m[INFO] \033[0m' +
                  '\033[33mSubdomain:\033[0m[' + search_info[i]['subdomain'] + ']',
                  '\033[33mIPADDR:\033[0m[' + search_info[i]['ipAdd'] + ']',
                  '\033[33mPort:\033[0m[' + str(search_info[i]['port']) + ']',  # type: int
                  '\033[33mService:\033[0m[' + search_info[i]['service'] + ']',
                  '\033[33mProduct:\033[0m[' + search_info[i]['product'] + ']')
        if export_filename != '':
            print('\033[33m[INFO]\033[0m 查询结果保存至: %s' % ('./Output/' + export_filename))
            with open('Output/%s' % export_filename, 'a', newline='') as csvfile:
                fieldnames = ['域名', 'IP地址', '端口', '服务', '产品']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(0, len(search_info)):
                    if search_info[i]['product'] == '':
                        search_info[i]['product'] = 'Unknow'
                    result = {
                        '域名': search_info[i]['subdomain'],
                        'IP地址': search_info[i]['ipAdd'],
                        '端口': search_info[i]['port'],
                        '服务': str(search_info[i]['service']),
                        '产品': search_info[i]['product']
                    }
                    writer.writerow(result)
            csvfile.close()

    def kownledge_search(self, keyword):
        data = {
            "pageNo": 1,
            "pageSize": 12,
            "platPostDto": {
                "postTitle": keyword,
                "categoryId": ""
            }
        }
        return data

    def requests_kownledge_search_api(self, keyword):
        print('\033[34m[KEYW]\33[0m 关键字: %s' % keyword)
        knowledge_api_url = self.knowledge_api_url
        knowledge_data = self.kownledge_search(keyword)
        user_token = self.get_user_token()
        headers = {
            "authorization": user_token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
        }
        knowledge_api_res = requests.post(knowledge_api_url, headers=headers, json=knowledge_data)
        try:
            print('\033[32m[SUCC]\033[0m 查询成功')
            knowledge_api_res_json = knowledge_api_res.json()
            knowledge_info = knowledge_api_res_json['data']['platPostSVos']
            for i in range(0, len(knowledge_info)):
                link = 'https://plat.wgpsec.org/knowledge/view/%s' % knowledge_info[i]['postId']
                print('\033[34m[INFO]\033[0m ' + '\033[33mTitle:\033[0m[' + knowledge_info[i]['postTitle'] + ']', '\033[33mLink:\033[0m[' + link + ']')
        except:
            knowledge_api_res_json = knowledge_api_res.json()
            print('\033[31m[ERRO]\033[0m ' + knowledge_api_res_json['msg'])
