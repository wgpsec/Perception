import requests
import demjson
import argparse
import sys
import os
import xlwt
import datetime

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
# 获取当前时间
now_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')

# 表格
wb = xlwt.Workbook()
ws = wb.add_sheet('查询结果')


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

# 获取当前路径
path = os.getcwd()
user_token_txt = os.path.exists('user_token.txt')
pageSize_txt = os.path.exists('pageSize.txt')

#  创建用户token存放
if user_token_txt == False:
    with open('user_token.txt','w') as f:
        f.close()
else:
    pass

# 判断cookie是否生效
with open('user_token.txt','r+') as f:
    cookies_read = f.read()
    f.close()
# 请求头
header = {
    "authorization": cookies_read,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
    }
yz_json = {
"pageNo": 1,
"pageSize": 20,
"query": "city=上海",
"type": "web"
}
yz = requests.post('https://plat.wgpsec.org/api/v1/ws/search', headers=header,json=yz_json)
yz_return = demjson.decode(yz.text)
# 开始验证
if int(yz_return['code']) == 2000:
    print('token验证成功')
else:
    if int(yz_return['code']) == 4001 or int(yz_return['code'] == 4018):
        print('未登录或者登录超时，请重新登录！')
        user_name = input('输入你的账号：')
        user_passwd = input('输入你的密码：')
        # 登录获取token
        login_json = {
            "userName": user_name,
            "userPassword": user_passwd,
            "captcha": "dqdq",
            "type": 0
        }
        login_api = 'https://plat.wgpsec.org/api/user/passwordLogin'
        login_api_return = requests.post(login_api,json=login_json)
        login_api_return_json = demjson.decode(login_api_return.text)
        login_token = login_api_return_json['data']['token']

        if int(login_api_return_json['code']) == 5001:
            print('密码或用户名错误，重新登录')
        elif int(login_api_return_json['code']) == 2000:
            # 写入cookie
            print('token验证成功！')
            with open('user_token.txt', 'w') as f:
                f.write(login_token)
                f.close()
    else:
        print('token验证成功！')

# 设置查询条数
if pageSize_txt == False:
    with open('pageSize.txt','w') as f:
        setting_input = input('输入你想查询的默认条数：')
        f.write(setting_input)
        f.close()
else:
    print('token验证成功')
    with open('pageSiza.txt', 'r+') as f:
        pageSize = int(f.read())
        f.close()
    if int(pageSize) > 99:
        print('查询的条数超过100，请手动修改setting.txt文件，建议改为99，避免出错')
        sys.exit()
    else:
        print('success!')

# 读取cookies文件
with open('user_token.txt','r+') as f:
    cookies_read = f.read()
    f.close()

# 读取配置文件
with open('pageSize.txt','r+') as f:
    pageSize = int(f.read())
    f.close()

# 主要程序
class Search(object):

    def __init__(self):
        pass

    # 城市查询
    def city(self,city):
        search_api_url = 'https://plat.wgpsec.org/api/v1/ws/search' # 搜索模块api链接
        knowledge_api_url = 'https://plat.wgpsec.org/api/post/queryPlatPost' # 知识库api链接
        key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
               'subdomainTitle',
               'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "authorization":cookies_read,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
        }
        search_json = {
            "pageNo": 1,
            "pageSize": pageSize,
            "query": "city=%s" %city,
            "type": "web"
                        }


        search_api_return = requests.post(search_api_url, headers=header, json=search_json)
        search_api_return_json = demjson.decode(search_api_return.text)

        # json 返回值里面会有3个key分别是：code、msg、data
        search_api_data = search_api_return_json['data']  # 提取返回中的data值

        # data下面有wsDomainInfoDto、wsSubDomainInfoDtoList、wsPortInfoDtoList、wsUrlsInfoDtoList 目前只有wsSubDomainInfoDtoList存在可用信息，其他返回值为null，所以其他的参数不写

        # wsPortInfoDtoList = api_data['wsPortInfoDtoList']

        wsSubDomainInfoDtoList = search_api_data['wsSubDomainInfoDtoList']

        # wsSubDomainInfoDtoList中有5个key，分别是wsSubDomainInfoDtos、pageSize、totalCount、pageNo、pages。所有的域名信息都在wsSubDomainInfoDtos里面，包括子域名
        wsSubDomainInfoDtos = wsSubDomainInfoDtoList['wsSubDomainInfoDtos']  # 查询出的域名和子域，列表的形式出来的，所以下方使用下标
        i = 0
        try:
            while i < pageSize:  # 遍历出我们插到的信息
                # 判断域名的返回信息，是否为 Not Found
                if wsSubDomainInfoDtos[i]['subdomainTitle'] == 'Not Found':
                    print('无法访问\n'
                          '域名： %s' % wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,0, '无法访问')
                    ws.write(i,2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i,4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    wb.save(now_time + '.xls')
                    i += 1
                    print('\n\n')

                # 判断域名信息的返回信息，是否为None
                elif wsSubDomainInfoDtos[i]['subdomainTitle'] == None:
                    print('网站标题无法获取，但是存在，可手动查看是否能能够访问！\n'
                          '域名：%s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomain'],
                                                               wsSubDomainInfoDtos[i]['ipAdd'],
                                                                wsSubDomainInfoDtos[i]['subdomainBanner']
                                                              )
                          )
                    ws.write(i,0, '网站存在但无法获得title')
                    ws.write(i,2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i,4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    wb.save(now_time + '.xls')

                    if wsSubDomainInfoDtos[i]['subdomainBanner'] == None or wsSubDomainInfoDtos[i]['subdomainBanner'] == '':
                        print('该网站服务未找到')
                    else:
                        key_word = wsSubDomainInfoDtos[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]

                        knowledge_json = {
                            "pageNo": 1,
                            "pageSize": 12,
                            "platPostDto": {
                                "postTitle":new_word,
                            "categoryId": ""
                        }
                        }
                        knowledge_api_return = requests.post(knowledge_api_url,headers=header,json=knowledge_json)
                        knowledge_api_return_json = demjson.decode(knowledge_api_return.text)
                        knowledge_api_data = knowledge_api_return_json['data']
                        platPostSVos = knowledge_api_data['platPostSVos'] # 取的返回值的文章详情页面
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

                # 正常域名的判断
                else:
                    print('网站标题：%s\n域名: %s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomainTitle'],
                                                                 wsSubDomainInfoDtos[i]['subdomain'],
                                                                 wsSubDomainInfoDtos[i]['ipAdd'],
                                                                 wsSubDomainInfoDtos[i]['subdomainBanner']
                                                                 )
                          )
                    # 写入表格中
                    ws.write(i,0, wsSubDomainInfoDtos[i]['subdomainTitle'])
                    ws.write(i,2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i,4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    wb.save(now_time + '.xls')

                    # 将搜索出来的subdomainBanner值作为知识库搜索的参数传入。判断subdomainBanner是否为未查询到或者是为空
                    if wsSubDomainInfoDtos[i]['subdomainBanner'] == None or wsSubDomainInfoDtos[i]['subdomainBanner']=='':
                        print('该网站服务未找到')
                    # 进行知识库查询
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
                            print('相关文章链接: ''https://plat.wgpsec.org/knowledge/view/%s' %(knowledge_id))
                            n += 1
                        if n ==0 :
                            print('暂时没有相关文章！QAQ')
                print('\n\n')
                i += 1
        # 获取报错
        except IndexError: # 因为查询的条数目不一样，但是默认的pageSize是一样的，所以很多时候会存在一个问题就是没有那么多条，因为循环是和pageSize进行对比，会报错，就捕获这个错误
            print('当前库中只有%s条数据！' % i)
        finally:
            print('当前查询的城市为：%s 查询成功' % city)

    # 域名查询
    def host(self,host):
        search_api_url = 'https://plat.wgpsec.org/api/v1/ws/search' # 搜索模块api链接
        knowledge_api_url = 'https://plat.wgpsec.org/api/post/queryPlatPost' # 知识库api链接
        key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
               'subdomainTitle',
               'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "authorization":cookies_read
        }
        search_json = {
            "pageNo": 1,
            "pageSize": pageSize,
            "query": "ip=%s" %host,
            "type": "web"
                        }


        search_api_return = requests.post(search_api_url, headers=header, json=search_json)
        search_api_return_json = demjson.decode(search_api_return.text)
        search_api_data = search_api_return_json['data']  # json 返回值里面会有3个key分别是：code、msg、data提取返回中的data值
        wsSubDomainInfoDtoList = search_api_data['wsSubDomainInfoDtoList']# data下面有wsDomainInfoDto、wsSubDomainInfoDtoList、wsPortInfoDtoList、wsUrlsInfoDtoList 目前只有wsSubDomainInfoDtoList存在可用信息，其他返回值为null，所以其他的参数不写
        wsSubDomainInfoDtos = wsSubDomainInfoDtoList['wsSubDomainInfoDtos']  # 查询出的域名和子域，列表的形式出来的，所以下方使用下标， # wsSubDomainInfoDtoList中有5个key，分别是wsSubDomainInfoDtos、pageSize、totalCount、pageNo、pages。所有的域名信息都在wsSubDomainInfoDtos里面，包括子域名
        i = 0
        try:
            while i < pageSize:  # 遍历出我们插到的信息
                #
                if wsSubDomainInfoDtos[i]['subdomainTitle'] == 'Not Found':
                    print('无法访问\n'
                          '域名： %s' % wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,0, '无法访问')
                    ws.write(i,2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i,4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    wb.save(now_time + '.xls')
                    i += 1
                    print('\n\n')

                #
                elif wsSubDomainInfoDtos[i]['subdomainTitle'] == None:
                    print('网站标题无法获取，但是存在，可手动查看是否能能够访问！\n'
                          '域名：%s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomain'],
                                                               wsSubDomainInfoDtos[i]['ipAdd'],
                                                                wsSubDomainInfoDtos[i]['subdomainBanner']
                                                              )
                          )
                    ws.write(i,0, '网站存在但无法获得title')
                    ws.write(i,2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i,4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    wb.save(now_time + '.xls')

                    if wsSubDomainInfoDtos[i]['subdomainBanner'] == None:
                        print('该网站服务未找到')
                    else:
                        key_word = wsSubDomainInfoDtos[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]

                        knowledge_json = {
                            "pageNo": 1,
                            "pageSize": 12,
                            "platPostDto": {
                                "postTitle":new_word,
                            "categoryId": ""
                        }
                        }
                        knowledge_api_return = requests.post(knowledge_api_url,headers=header,json=knowledge_json)
                        knowledge_api_return_json = demjson.decode(knowledge_api_return.text)
                        knowledge_api_data = knowledge_api_return_json['data']
                        platPostSVos = knowledge_api_data['platPostSVos'] # 取的返回值的文章详情页面
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

                #
                else:
                    print('网站标题：%s\n域名: %s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomainTitle'],
                                                                 wsSubDomainInfoDtos[i]['subdomain'],
                                                                 wsSubDomainInfoDtos[i]['ipAdd'],
                                                                 wsSubDomainInfoDtos[i]['subdomainBanner']
                                                                 )
                          ) # 这里我用的是下标，可以优化一下
                    ws.write(i,0, wsSubDomainInfoDtos[i]['subdomainTitle'])
                    ws.write(i,2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i,4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    wb.save(now_time + '.xls')

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
                            print('相关文章链接： ''https://plat.wgpsec.org/knowledge/view/%s' %(knowledge_id))
                            n += 1
                        if n ==0 :
                            print('暂时没有相关文章！QAQ')
                print('\n\n')
                i += 1

        except IndexError:
            print('当前库中只有%s条数据！' %i)

        finally:
            print('ip：%s 查询成功'%host)

    # 标题查询
    def title(self,title):
        search_api_url = 'https://plat.wgpsec.org/api/v1/ws/search' # 搜索模块api链接
        knowledge_api_url = 'https://plat.wgpsec.org/api/post/queryPlatPost' # 知识库api链接
        key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
               'subdomainTitle',
               'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "authorization":cookies_read
        }
        search_json = {
            "pageNo": 1,
            "pageSize": pageSize,
            "query": "title=%s" %title,
            "type": "web"
                        }
        search_api_return = requests.post(search_api_url, headers=header, json=search_json)
        search_api_return_json = demjson.decode(search_api_return.text)
        search_api_data = search_api_return_json['data']  # json 返回值里面会有3个key分别是：code、msg、data，提取返回中的data值
        wsSubDomainInfoDtoList = search_api_data['wsSubDomainInfoDtoList'] # data下面有wsDomainInfoDto、wsSubDomainInfoDtoList、wsPortInfoDtoList、wsUrlsInfoDtoList 目前只有wsSubDomainInfoDtoList存在可用信息，其他返回值为null，所以其他的参数不写
        wsSubDomainInfoDtos = wsSubDomainInfoDtoList['wsSubDomainInfoDtos']  # wsSubDomainInfoDtoList中有5个key，分别是wsSubDomainInfoDtos、pageSize、totalCount、pageNo、pages。所有的域名信息都在wsSubDomainInfoDtos里面，包括子域名查询出的域名和子域，列表的形式出来的，所以下方使用下标

        i = 0
        try:
            while i < pageSize:  # 遍历出我们插到的信息
                if wsSubDomainInfoDtos[i]['subdomainTitle'] == 'Not Found':
                    print('无法访问\n'
                          '域名： %s' % wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,0, '无法访问')
                    ws.write(i,2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i,4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    wb.save(now_time + '.xls')
                    i += 1
                    print('\n\n')

                elif wsSubDomainInfoDtos[i]['subdomainTitle'] == None:
                    print('网站标题无法获取，但是存在，可手动查看是否能能够访问！\n'
                          '域名：%s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomain'],
                                                               wsSubDomainInfoDtos[i]['ipAdd'],
                                                                wsSubDomainInfoDtos[i]['subdomainBanner']
                                                              )
                          )
                    ws.write(i,0, '网站存在但无法获得title')
                    ws.write(i,2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i,4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    wb.save(now_time + '.xls')

                    if wsSubDomainInfoDtos[i]['subdomainBanner'] == None:
                        print('该网站服务未找到')
                    else:
                        key_word = wsSubDomainInfoDtos[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]

                        knowledge_json = {
                            "pageNo": 1,
                            "pageSize": 12,
                            "platPostDto": {
                                "postTitle":new_word,
                            "categoryId": ""
                        }
                        }
                        knowledge_api_return = requests.post(knowledge_api_url,headers=header,json=Knowledge_json)
                        knowledge_api_return_json = demjson.decode(knowledge_api_return.text)
                        knowledge_api_data = knowledge_api_return_json['data']
                        platPostSVos = knowledge_api_data['platPostSVos'] # 取的返回值的文章详情页面
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
                    ws.write(i,0, wsSubDomainInfoDtos[i]['subdomainTitle'])
                    ws.write(i,2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i,4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    wb.save(now_time + '.xls')

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
                            print('相关文章链接： ''https://plat.wgpsec.org/knowledge/view/%s' %(knowledge_id))
                            n += 1
                        if n ==0 :
                            print('暂时没有相关文章！QAQ')
                print('\n\n')
                i += 1

        except IndexError:
            print('当前库中只有%s条数据！' %i)

        finally:
            print('网站标题为：%s 查询成功'%title)

    # 端口查询
    def port(self,port):
        search_api_url = 'https://plat.wgpsec.org/api/v1/ws/search' # 搜索模块api链接
        knowledge_api_url = 'https://plat.wgpsec.org/api/post/queryPlatPost' # 知识库api链接
        key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
               'subdomainTitle',
               'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "authorization":cookies_read
        }
        search_json = {
            "pageNo": 1,
            "pageSize": pageSize,
            "query": "port=%s" %port,
            "type": "web"
                        }


        search_api_return = requests.post(search_api_url, headers=header, json=search_json)
        search_api_return_json = demjson.decode(search_api_return.text)
        search_api_data = search_api_return_json['data']  # json 返回值里面会有3个key分别是：code、msg、data提取返回中的data值
        wsSubDomainInfoDtoList = search_api_data['wsSubDomainInfoDtoList']# data下面有wsDomainInfoDto、wsSubDomainInfoDtoList、wsPortInfoDtoList、wsUrlsInfoDtoList 目前只有wsSubDomainInfoDtoList存在可用信息，其他返回值为null，所以其他的参数不写
        wsSubDomainInfoDtos = wsSubDomainInfoDtoList['wsSubDomainInfoDtos']  # 查询出的域名和子域，列表的形式出来的，所以下方使用下标，wsSubDomainInfoDtoList中有5个key，分别是wsSubDomainInfoDtos、pageSize、totalCount、pageNo、pages。所有的域名信息都在wsSubDomainInfoDtos里面，包括子域名
        i = 0
        try:
            while i < pageSize:  # 遍历出我们插到的信息
                #
                if wsSubDomainInfoDtos[i]['subdomainTitle'] == 'Not Found':
                    print('无法访问\n'
                          '域名： %s' % wsSubDomainInfoDtos[i]['subdomain']
                          )

                    ws.write(i,0, '无法访问')
                    ws.write(i,2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i,4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    wb.save(now_time + '.xls')
                    i += 1
                    print('\n\n')
                #
                elif wsSubDomainInfoDtos[i]['subdomainTitle'] == None:
                    print('网站标题无法获取，但是存在，可手动查看是否能能够访问！\n'
                          '域名：%s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomain'],
                                                               wsSubDomainInfoDtos[i]['ipAdd'],
                                                                wsSubDomainInfoDtos[i]['subdomainBanner']
                                                              )
                          )
                    ws.write(i,0, '网站存在但无法获得title')
                    ws.write(i,2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i,4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    wb.save(now_time + '.xls')
                    if wsSubDomainInfoDtos[i]['subdomainBanner'] == None:
                        print('该网站服务未找到')
                    else:
                        key_word = wsSubDomainInfoDtos[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]

                        knowledge_json = {
                            "pageNo": 1,
                            "pageSize": 12,
                            "platPostDto": {
                                "postTitle":new_word,
                            "categoryId": ""
                        }
                        }
                        knowledge_api_return = requests.post(knowledge_api_url,headers=header,json=knowledge_json)
                        knowledge_api_return_json = demjson.decode(knowledge_api_return.text)
                        knowledge_api_data = knowledge_api_return_json['data']
                        platPostSVos = knowledge_api_data['platPostSVos'] # 取的返回值的文章详情页面
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
                #
                else:
                    print('网站标题：%s\n域名: %s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomainTitle'],
                                                                 wsSubDomainInfoDtos[i]['subdomain'],
                                                                 wsSubDomainInfoDtos[i]['ipAdd'],
                                                                 wsSubDomainInfoDtos[i]['subdomainBanner']
                                                                 )
                          ) # 这里我用的是下标，可以优化一下
                    ws.write(i,0, wsSubDomainInfoDtos[i]['subdomainTitle'])
                    ws.write(i,2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i,4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    wb.save(now_time + '.xls')

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
                            print('相关文章链接： ''https://plat.wgpsec.org/knowledge/view/%s' %(knowledge_id))
                            n += 1
                        if n ==0 :
                            print('暂时没有相关文章！QAQ')
                print('\n\n')
                i += 1

        except IndexError:
            print('当前库中只有%s条数据！' %i)

        finally:
            print('端口为：%s 查询成功'%port)


    def ip_port(self,ip,port):
        search_api_url = 'https://plat.wgpsec.org/api/v1/ws/search' # 搜索模块api链接
        knowledge_api_url = 'https://plat.wgpsec.org/api/post/queryPlatPost' # 知识库api链接
        key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
               'subdomainTitle',
               'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "authorization":cookies_read
        }
        search_json = {
            "pageNo": 1,
            "pageSize": pageSize,
            "query": "ip=%s|port=%s" %(ip,port),
            "type": "web"
                        }


        search_api_return = requests.post(search_api_url, headers=header, json=search_json)
        search_api_return_json = demjson.decode(search_api_return.text)

        # json 返回值里面会有3个key分别是：code、msg、data
        search_api_data = search_api_return_json['data']  # 提取返回中的data值

        # data下面有wsDomainInfoDto、wsSubDomainInfoDtoList、wsPortInfoDtoList、wsUrlsInfoDtoList 目前只有wsSubDomainInfoDtoList存在可用信息，其他返回值为null，所以其他的参数不写

        # wsPortInfoDtoList = api_data['wsPortInfoDtoList']

        wsSubDomainInfoDtoList = search_api_data['wsSubDomainInfoDtoList']

        # wsSubDomainInfoDtoList中有5个key，分别是wsSubDomainInfoDtos、pageSize、totalCount、pageNo、pages。所有的域名信息都在wsSubDomainInfoDtos里面，包括子域名
        wsSubDomainInfoDtos = wsSubDomainInfoDtoList['wsSubDomainInfoDtos']  # 查询出的域名和子域，列表的形式出来的，所以下方使用下标
        i = 0
        try:
            while i < pageSize:  # 遍历出我们插到的信息
                if wsSubDomainInfoDtos[i]['subdomainTitle'] == 'Not Found':
                    print('无法访问\n'
                          '域名： %s' % wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,0, '无法访问')
                    ws.write(i,2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i,4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    wb.save(now_time + '.xls')
                    i += 1
                    print('\n\n')

                elif wsSubDomainInfoDtos[i]['subdomainTitle'] == None:
                    print('网站标题无法获取，但是存在，可手动查看是否能能够访问！\n'
                          '域名：%s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomain'],
                                                               wsSubDomainInfoDtos[i]['ipAdd'],
                                                                wsSubDomainInfoDtos[i]['subdomainBanner']
                                                              )
                          )
                    ws.write(i,0, '网站存在但无法获得title')
                    ws.write(i,2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i,4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    wb.save(now_time + '.xls')
                    if wsSubDomainInfoDtos[i]['subdomainBanner'] == None:
                        print('该网站服务未找到')
                    else:
                        key_word = wsSubDomainInfoDtos[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]

                        knowledge_json = {
                            "pageNo": 1,
                            "pageSize": 12,
                            "platPostDto": {
                                "postTitle":new_word,
                            "categoryId": ""
                        }
                        }
                        knowledge_api_return = requests.post(knowledge_api_url,headers=header,json=knowledge_json)
                        knowledge_api_return_json = demjson.decode(knowledge_api_return.text)
                        knowledge_api_data = knowledge_api_return_json['data']
                        platPostSVos = knowledge_api_data['platPostSVos'] # 取的返回值的文章详情页面
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
                    ws.write(i,0, wsSubDomainInfoDtos[i]['subdomainTitle'])
                    ws.write(i,2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i,3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i,4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    wb.save(now_time + '.xls')

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
                            print('相关文章链接： ''https://plat.wgpsec.org/knowledge/view/%s' %(knowledge_id))
                            n += 1
                        if n ==0 :
                            print('暂时没有相关文章！QAQ')
                print('\n\n')
                i += 1
        except IndexError:
            print('当前库中只有%s条数据！' % i)

        finally:
            print('查询的IP为：%s、端口为：%s 查询成功' % (ip,port))
            sys.exit()





if args.c:
    city_ = Search()
    city_.city(args.c)
elif args.h:
    if args.h == '127.0.0.1':
        print('输入的是局域网地址，无法查询')
    else:
        host_ = Search()
        host_.host(args.h)
elif args.t:
    title_ = Search()
    title_.title(args.t)
elif args.p:
    if int(args.p) > 65535 or int(args.p) < 0:
        print('输入的端口范围不正确')
    else:
        port_ = Search()
        port_.port(args.p)
elif args.h and args.p:
        ip_port = Search()
        ip_port.ip_port(args.h,args.p)