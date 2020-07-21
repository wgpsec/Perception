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
'||                                在线信息收集工具 V1.1                                    ||\n'
'==========================================================================================\n'
)
# 提示信息以及外部参数的接收
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
        Search_api_url = 'https://plat.wgpsec.org/api/v1/ws/search' # 搜索模块api链接
        knowledge_api_url = 'https://plat.wgpsec.org/api/post/queryPlatPost' # 知识库api链接
        key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
               'subdomainTitle',
               'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "Cookie":cookies_read
        }
        Search_json = {
            "pageNo": 1,
            "pageSize": pageSize,
            "query": "city=%s" %city,
            "type": "web"
                        }


        Search_api_return = requests.post(Search_api_url, headers=header, json=Search_json)
        Search_api_return_json = demjson.decode(Search_api_return.text)

        # json 返回值里面会有3个key分别是：code、msg、data
        Search_api_data = Search_api_return_json['data']  # 提取返回中的data值

        # data下面有wsDomainInfoDto、wsSubDomainInfoDtoList、wsPortInfoDtoList、wsUrlsInfoDtoList 目前只有wsSubDomainInfoDtoList存在可用信息，其他返回值为null，所以其他的参数不写

        # wsPortInfoDtoList = api_data['wsPortInfoDtoList']

        wsSubDomainInfoDtoList = Search_api_data['wsSubDomainInfoDtoList']

        # wsSubDomainInfoDtoList中有5个key，分别是wsSubDomainInfoDtos、pageSize、totalCount、pageNo、pages。所有的域名信息都在wsSubDomainInfoDtos里面，包括子域名
        wsSubDomainInfoDtos = wsSubDomainInfoDtoList['wsSubDomainInfoDtos']  # 查询出的域名和子域，列表的形式出来的，所以下方使用下标
        i = 0
        try:
            while i < pageSize:  # 遍历出我们插到的信息
                if wsSubDomainInfoDtos[i]['subdomainTitle'] == 'Not Found':
                    print('无法访问\n'
                          '域名： %s' % wsSubDomainInfoDtos[i]['subdomain'])
                    i += 1
                    print('\n\n')

                elif wsSubDomainInfoDtos[i]['subdomainTitle'] == None:
                    print('网站标题无法获取，但是存在，可手动查看是否能能够访问！\n'
                          '域名：%s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomain'],
                                                               wsSubDomainInfoDtos[i]['ipAdd'],
                                                                wsSubDomainInfoDtos[i]['subdomainBanner']
                                                              )
                          )
                    if wsSubDomainInfoDtos[i]['subdomainBanner'] == None:
                        print('该网站服务未找到')
                    else:
                        key_word = wsSubDomainInfoDtos[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]
                            Knowledge_json = {
                                "pageNo": 1,
                                "pageSize": 12,
                                "platPostDto": {
                                    "postTitle":new_word,
                                "categoryId": ""
                            }
                            }
                            Knowledge_api_return = requests.post(knowledge_api_url,headers=header,json=Knowledge_json)
                            Knowledge_api_return_json = demjson.decode(Knowledge_api_return.text)
                            Knowledge_api_data = Knowledge_api_return_json['data']
                            platPostSVos = Knowledge_api_data['platPostSVos'] # 取的返回值的文章详情页面
                            knowledge_size = len(platPostSVos)
                            n = 0
                            while n < knowledge_size:
                                knowledge_id = platPostSVos[n]['postId'] # 取出文章ID
                                print('相关文章链接''https://plat.wgpsec.org/knowledge/view/%s' %(knowledge_id))
                                n += 1
                            if n ==0 :
                                print('暂时没有相关文章！QAQ')

                    print('\n\n')
                    i += 1

                else:
                    print('网站标题：%s\n域名: %s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomainTitle'],
                                                                 wsSubDomainInfoDtos[i]['subdomain'],
                                                                 wsSubDomainInfoDtos[i]['ipAdd'],
                                                                 wsSubDomainInfoDtos[i]['subdomainBanner']
                                                                 )
                          ) # 这里我用的是下标，可以优化一下

                    # 将搜索出来的subdomainBanner值作为知识库搜索的参数传入。
                    if wsSubDomainInfoDtos[i]['subdomainBanner'] == None or wsSubDomainInfoDtos[i]['subdomainBanner']=='':
                        print('该网站服务未找到')
                    else:
                        key_word = wsSubDomainInfoDtos[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]
                            Knowledge_json = {
                                "pageNo": 1,
                                "pageSize": 12,
                                "platPostDto": {
                                    "postTitle":new_word,
                                "categoryId": ""
                            }
                            }
                            Knowledge_api_return = requests.post(knowledge_api_url,headers=header,json=Knowledge_json)
                            Knowledge_api_return_json = demjson.decode(Knowledge_api_return.text)
                            Knowledge_api_data = Knowledge_api_return_json['data']
                            platPostSVos = Knowledge_api_data['platPostSVos'] # 取的返回值的文章详情页面
                            knowledge_size = len(platPostSVos)
                            n = 0
                            while n < knowledge_size:
                                knowledge_id = platPostSVos[n]['postId'] # 取出文章ID
                                print('相关文章链接''https://plat.wgpsec.org/knowledge/view/%s' %(knowledge_id))
                                n += 1
                            if n ==0 :
                                print('暂时没有相关文章！QAQ')
                    print('\n\n')
                    i += 1
        except IndexError:

            print('查询出错')
        finally:
            print('查询成功')

    # 域名查询
    def host(self,host,pageSize=20):
        Search_api_url = 'https://plat.wgpsec.org/api/v1/ws/search' # 搜索模块api链接
        knowledge_api_url = 'https://plat.wgpsec.org/api/post/queryPlatPost' # 知识库api链接
        key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
               'subdomainTitle',
               'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "Cookie":cookies_read
        }
        Search_json = {
            "pageNo": 1,
            "pageSize": pageSize,
            "query": "ip=%s" %host,
            "type": "web"
                        }


        Search_api_return = requests.post(Search_api_url, headers=header, json=Search_json)
        Search_api_return_json = demjson.decode(Search_api_return.text)

        # json 返回值里面会有3个key分别是：code、msg、data
        Search_api_data = Search_api_return_json['data']  # 提取返回中的data值

        # data下面有wsDomainInfoDto、wsSubDomainInfoDtoList、wsPortInfoDtoList、wsUrlsInfoDtoList 目前只有wsSubDomainInfoDtoList存在可用信息，其他返回值为null，所以其他的参数不写

        # wsPortInfoDtoList = api_data['wsPortInfoDtoList']

        wsSubDomainInfoDtoList = Search_api_data['wsSubDomainInfoDtoList']

        # wsSubDomainInfoDtoList中有5个key，分别是wsSubDomainInfoDtos、pageSize、totalCount、pageNo、pages。所有的域名信息都在wsSubDomainInfoDtos里面，包括子域名
        wsSubDomainInfoDtos = wsSubDomainInfoDtoList['wsSubDomainInfoDtos']  # 查询出的域名和子域，列表的形式出来的，所以下方使用下标
        i = 0
        try:
            while i < pageSize:  # 遍历出我们插到的信息
                if wsSubDomainInfoDtos[i]['subdomainTitle'] == 'Not Found':
                    print('无法访问\n'
                          '域名： %s' % wsSubDomainInfoDtos[i]['subdomain'])
                    i += 1
                    print('\n\n')

                elif wsSubDomainInfoDtos[i]['subdomainTitle'] == None:
                    print('网站标题无法获取，但是存在，可手动查看是否能能够访问！\n'
                          '域名：%s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomain'],
                                                               wsSubDomainInfoDtos[i]['ipAdd'],
                                                                wsSubDomainInfoDtos[i]['subdomainBanner']
                                                              )
                          )
                    if wsSubDomainInfoDtos[i]['subdomainBanner'] == None:
                        print('该网站服务未找到')
                    else:
                        key_word = wsSubDomainInfoDtos[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]
                            Knowledge_json = {
                                "pageNo": 1,
                                "pageSize": 12,
                                "platPostDto": {
                                    "postTitle":new_word,
                                "categoryId": ""
                            }
                            }
                            Knowledge_api_return = requests.post(knowledge_api_url,headers=header,json=Knowledge_json)
                            Knowledge_api_return_json = demjson.decode(Knowledge_api_return.text)
                            Knowledge_api_data = Knowledge_api_return_json['data']
                            platPostSVos = Knowledge_api_data['platPostSVos'] # 取的返回值的文章详情页面
                            knowledge_size = len(platPostSVos)
                            n = 0
                            while n < knowledge_size:
                                knowledge_id = platPostSVos[n]['postId'] # 取出文章ID
                                print('相关文章链接''https://plat.wgpsec.org/knowledge/view/%s' %(knowledge_id))
                                n += 1
                            if n ==0 :
                                print('暂时没有相关文章！QAQ')

                    print('\n\n')
                    i += 1

                else:
                    print('网站标题：%s\n域名: %s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomainTitle'],
                                                                 wsSubDomainInfoDtos[i]['subdomain'],
                                                                 wsSubDomainInfoDtos[i]['ipAdd'],
                                                                 wsSubDomainInfoDtos[i]['subdomainBanner']
                                                                 )
                          ) # 这里我用的是下标，可以优化一下

                    # 将搜索出来的subdomainBanner值作为知识库搜索的参数传入。
                    if wsSubDomainInfoDtos[i]['subdomainBanner'] == None or wsSubDomainInfoDtos[i]['subdomainBanner']=='':
                        print('该网站服务未找到')
                    else:
                        key_word = wsSubDomainInfoDtos[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]
                            Knowledge_json = {
                                "pageNo": 1,
                                "pageSize": 12,
                                "platPostDto": {
                                    "postTitle":new_word,
                                "categoryId": ""
                            }
                            }
                            Knowledge_api_return = requests.post(knowledge_api_url,headers=header,json=Knowledge_json)
                            Knowledge_api_return_json = demjson.decode(Knowledge_api_return.text)
                            Knowledge_api_data = Knowledge_api_return_json['data']
                            platPostSVos = Knowledge_api_data['platPostSVos'] # 取的返回值的文章详情页面
                            knowledge_size = len(platPostSVos)
                            n = 0
                            while n < knowledge_size:
                                knowledge_id = platPostSVos[n]['postId'] # 取出文章ID
                                print('相关文章链接''https://plat.wgpsec.org/knowledge/view/%s' %(knowledge_id))
                                n += 1
                            if n ==0 :
                                print('暂时没有相关文章！QAQ')
                    print('\n\n')
                    i += 1
        except IndexError:

            print('查询出错')
        finally:
            print('查询成功')    # 标题查询

    def title(self,title,pageSize=20):
        Search_api_url = 'https://plat.wgpsec.org/api/v1/ws/search' # 搜索模块api链接
        knowledge_api_url = 'https://plat.wgpsec.org/api/post/queryPlatPost' # 知识库api链接
        key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
               'subdomainTitle',
               'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "Cookie":cookies_read
        }
        Search_json = {
            "pageNo": 1,
            "pageSize": pageSize,
            "query": "title=%s" %title,
            "type": "web"
                        }


        Search_api_return = requests.post(Search_api_url, headers=header, json=Search_json)
        Search_api_return_json = demjson.decode(Search_api_return.text)

        # json 返回值里面会有3个key分别是：code、msg、data
        Search_api_data = Search_api_return_json['data']  # 提取返回中的data值

        # data下面有wsDomainInfoDto、wsSubDomainInfoDtoList、wsPortInfoDtoList、wsUrlsInfoDtoList 目前只有wsSubDomainInfoDtoList存在可用信息，其他返回值为null，所以其他的参数不写

        # wsPortInfoDtoList = api_data['wsPortInfoDtoList']

        wsSubDomainInfoDtoList = Search_api_data['wsSubDomainInfoDtoList']

        # wsSubDomainInfoDtoList中有5个key，分别是wsSubDomainInfoDtos、pageSize、totalCount、pageNo、pages。所有的域名信息都在wsSubDomainInfoDtos里面，包括子域名
        wsSubDomainInfoDtos = wsSubDomainInfoDtoList['wsSubDomainInfoDtos']  # 查询出的域名和子域，列表的形式出来的，所以下方使用下标
        i = 0
        try:
            while i < pageSize:  # 遍历出我们插到的信息
                if wsSubDomainInfoDtos[i]['subdomainTitle'] == 'Not Found':
                    print('无法访问\n'
                          '域名： %s' % wsSubDomainInfoDtos[i]['subdomain'])
                    i += 1
                    print('\n\n')

                elif wsSubDomainInfoDtos[i]['subdomainTitle'] == None:
                    print('网站标题无法获取，但是存在，可手动查看是否能能够访问！\n'
                          '域名：%s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomain'],
                                                               wsSubDomainInfoDtos[i]['ipAdd'],
                                                                wsSubDomainInfoDtos[i]['subdomainBanner']
                                                              )
                          )
                    if wsSubDomainInfoDtos[i]['subdomainBanner'] == None:
                        print('该网站服务未找到')
                    else:
                        key_word = wsSubDomainInfoDtos[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]
                            Knowledge_json = {
                                "pageNo": 1,
                                "pageSize": 12,
                                "platPostDto": {
                                    "postTitle":new_word,
                                "categoryId": ""
                            }
                            }
                            Knowledge_api_return = requests.post(knowledge_api_url,headers=header,json=Knowledge_json)
                            Knowledge_api_return_json = demjson.decode(Knowledge_api_return.text)
                            Knowledge_api_data = Knowledge_api_return_json['data']
                            platPostSVos = Knowledge_api_data['platPostSVos'] # 取的返回值的文章详情页面
                            knowledge_size = len(platPostSVos)
                            n = 0
                            while n < knowledge_size:
                                knowledge_id = platPostSVos[n]['postId'] # 取出文章ID
                                print('相关文章链接''https://plat.wgpsec.org/knowledge/view/%s' %(knowledge_id))
                                n += 1
                            if n ==0 :
                                print('暂时没有相关文章！QAQ')

                    print('\n\n')
                    i += 1

                else:
                    print('网站标题：%s\n域名: %s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomainTitle'],
                                                                 wsSubDomainInfoDtos[i]['subdomain'],
                                                                 wsSubDomainInfoDtos[i]['ipAdd'],
                                                                 wsSubDomainInfoDtos[i]['subdomainBanner']
                                                                 )
                          ) # 这里我用的是下标，可以优化一下

                    # 将搜索出来的subdomainBanner值作为知识库搜索的参数传入。
                    if wsSubDomainInfoDtos[i]['subdomainBanner'] == None or wsSubDomainInfoDtos[i]['subdomainBanner']=='':
                        print('该网站服务未找到')
                    else:
                        key_word = wsSubDomainInfoDtos[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]
                            Knowledge_json = {
                                "pageNo": 1,
                                "pageSize": 12,
                                "platPostDto": {
                                    "postTitle":new_word,
                                "categoryId": ""
                            }
                            }
                            Knowledge_api_return = requests.post(knowledge_api_url,headers=header,json=Knowledge_json)
                            Knowledge_api_return_json = demjson.decode(Knowledge_api_return.text)
                            Knowledge_api_data = Knowledge_api_return_json['data']
                            platPostSVos = Knowledge_api_data['platPostSVos'] # 取的返回值的文章详情页面
                            knowledge_size = len(platPostSVos)
                            n = 0
                            while n < knowledge_size:
                                knowledge_id = platPostSVos[n]['postId'] # 取出文章ID
                                print('相关文章链接''https://plat.wgpsec.org/knowledge/view/%s' %(knowledge_id))
                                n += 1
                            if n ==0 :
                                print('暂时没有相关文章！QAQ')
                    print('\n\n')
                    i += 1
        except IndexError:

            print('查询出错')
        finally:
            print('查询成功')

    def port(self,port,pageSize=20):
        Search_api_url = 'https://plat.wgpsec.org/api/v1/ws/search' # 搜索模块api链接
        knowledge_api_url = 'https://plat.wgpsec.org/api/post/queryPlatPost' # 知识库api链接
        key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
               'subdomainTitle',
               'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "Cookie":cookies_read
        }
        Search_json = {
            "pageNo": 1,
            "pageSize": pageSize,
            "query": "port=%s" %port,
            "type": "web"
                        }


        Search_api_return = requests.post(Search_api_url, headers=header, json=Search_json)
        Search_api_return_json = demjson.decode(Search_api_return.text)

        # json 返回值里面会有3个key分别是：code、msg、data
        Search_api_data = Search_api_return_json['data']  # 提取返回中的data值

        # data下面有wsDomainInfoDto、wsSubDomainInfoDtoList、wsPortInfoDtoList、wsUrlsInfoDtoList 目前只有wsSubDomainInfoDtoList存在可用信息，其他返回值为null，所以其他的参数不写

        # wsPortInfoDtoList = api_data['wsPortInfoDtoList']

        wsSubDomainInfoDtoList = Search_api_data['wsSubDomainInfoDtoList']

        # wsSubDomainInfoDtoList中有5个key，分别是wsSubDomainInfoDtos、pageSize、totalCount、pageNo、pages。所有的域名信息都在wsSubDomainInfoDtos里面，包括子域名
        wsSubDomainInfoDtos = wsSubDomainInfoDtoList['wsSubDomainInfoDtos']  # 查询出的域名和子域，列表的形式出来的，所以下方使用下标
        i = 0
        try:
            while i < pageSize:  # 遍历出我们插到的信息
                if wsSubDomainInfoDtos[i]['subdomainTitle'] == 'Not Found':
                    print('无法访问\n'
                          '域名： %s' % wsSubDomainInfoDtos[i]['subdomain'])
                    i += 1
                    print('\n\n')

                elif wsSubDomainInfoDtos[i]['subdomainTitle'] == None:
                    print('网站标题无法获取，但是存在，可手动查看是否能能够访问！\n'
                          '域名：%s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomain'],
                                                               wsSubDomainInfoDtos[i]['ipAdd'],
                                                                wsSubDomainInfoDtos[i]['subdomainBanner']
                                                              )
                          )
                    if wsSubDomainInfoDtos[i]['subdomainBanner'] == None:
                        print('该网站服务未找到')
                    else:
                        key_word = wsSubDomainInfoDtos[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]
                            Knowledge_json = {
                                "pageNo": 1,
                                "pageSize": 12,
                                "platPostDto": {
                                    "postTitle":new_word,
                                "categoryId": ""
                            }
                            }
                            Knowledge_api_return = requests.post(knowledge_api_url,headers=header,json=Knowledge_json)
                            Knowledge_api_return_json = demjson.decode(Knowledge_api_return.text)
                            Knowledge_api_data = Knowledge_api_return_json['data']
                            platPostSVos = Knowledge_api_data['platPostSVos'] # 取的返回值的文章详情页面
                            knowledge_size = len(platPostSVos)
                            n = 0
                            while n < knowledge_size:
                                knowledge_id = platPostSVos[n]['postId'] # 取出文章ID
                                print('相关文章链接''https://plat.wgpsec.org/knowledge/view/%s' %(knowledge_id))
                                n += 1
                            if n ==0 :
                                print('暂时没有相关文章！QAQ')

                    print('\n\n')
                    i += 1

                else:
                    print('网站标题：%s\n域名: %s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomainTitle'],
                                                                 wsSubDomainInfoDtos[i]['subdomain'],
                                                                 wsSubDomainInfoDtos[i]['ipAdd'],
                                                                 wsSubDomainInfoDtos[i]['subdomainBanner']
                                                                 )
                          ) # 这里我用的是下标，可以优化一下

                    # 将搜索出来的subdomainBanner值作为知识库搜索的参数传入。
                    if wsSubDomainInfoDtos[i]['subdomainBanner'] == None or wsSubDomainInfoDtos[i]['subdomainBanner']=='':
                        print('该网站服务未找到')
                    else:
                        key_word = wsSubDomainInfoDtos[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]
                            Knowledge_json = {
                                "pageNo": 1,
                                "pageSize": 12,
                                "platPostDto": {
                                    "postTitle":new_word,
                                "categoryId": ""
                            }
                            }
                            Knowledge_api_return = requests.post(knowledge_api_url,headers=header,json=Knowledge_json)
                            Knowledge_api_return_json = demjson.decode(Knowledge_api_return.text)
                            Knowledge_api_data = Knowledge_api_return_json['data']
                            platPostSVos = Knowledge_api_data['platPostSVos'] # 取的返回值的文章详情页面
                            knowledge_size = len(platPostSVos)
                            n = 0
                            while n < knowledge_size:
                                knowledge_id = platPostSVos[n]['postId'] # 取出文章ID
                                print('相关文章链接''https://plat.wgpsec.org/knowledge/view/%s' %(knowledge_id))
                                n += 1
                            if n ==0 :
                                print('暂时没有相关文章！QAQ')
                    print('\n\n')
                    i += 1
        except IndexError:

            print('查询出错')
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
    title_.title(args.t)
if args.p:
    port_ = Search()
    port_.port(args.p)