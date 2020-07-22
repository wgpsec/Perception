import requests
import xlwt
import datetime

class Search:

    def __init__(self, cookies_read, page_size):
        self.cookies_read = cookies_read
        self.page_size = page_size
        self.wb = xlwt.Workbook()
        self.ws = self.wb.add_sheet('查询结果')

        # no.
        self.now_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')

    # 城市查询
    def city(self, city):
        search_api_url = 'https://plat.wgpsec.org/api/v1/ws/search'  # 搜索模块api链接
        knowledge_api_url = 'https://plat.wgpsec.org/api/post/queryPlatPost'  # 知识库api链接
        # key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
        #       'subdomainTitle',
        #       'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "authorization": self.cookies_read,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
        }
        search_json = {
            "pageNo": 1,
            "pageSize": self.page_size,
            "query": "city=%s" % city,
            "type": "web"
        }

        search_api_return_json = requests.post(
            search_api_url, headers=header, json=search_json).json()
        
        # json 返回值里面会有3个key分别是：code、msg、data
        search_api_data = search_api_return_json['data']  # 提取返回中的data值

        # data下面有wsDomainInfoDto、wsSubDomainInfoDtoList、wsPortInfoDtoList、wsUrlsInfoDtoList 目前只有wsSubDomainInfoDtoList存在可用信息，其他返回值为null，所以其他的参数不写

        # wsPortInfoDtoList = api_data['wsPortInfoDtoList']

        subdomain_info_list = search_api_data['wsSubDomainInfoDtoList']

        # wsSubDomainInfoDtoList中有5个key，分别是wsSubDomainInfoDtos、pageSize、totalCount、pageNo、pages。所有的域名信息都在wsSubDomainInfoDtos里面，包括子域名
        # 查询出的域名和子域，列表的形式出来的，所以下方使用下标
        subdomain_info = subdomain_info_list['wsSubDomainInfoDtos']
        i = 0
        try:
            while i < self.page_size:  # 遍历出我们插到的信息
                # 判断域名的返回信息，是否为 Not Found
                if subdomain_info[i]['subdomainTitle'] == 'Not Found':
                    print('无法访问\n'
                          '域名： %s' % subdomain_info[i]['subdomain'])
                    self.ws.write(i, 0, '无法访问')
                    self.ws.write(i, 2, subdomain_info[i]['subdomain'])
                    self.ws.write(i, 3, subdomain_info[i]['ipAdd'])
                    self.ws.write(i, 4, subdomain_info[i]['subdomainBanner'])
                    self.wb.save(self.now_time + '.xls')
                    i += 1
                    print('\n\n')

                # 判断域名信息的返回信息，是否为None
                elif subdomain_info[i]['subdomainTitle'] is None:
                    print('网站标题无法获取，但是存在，可手动查看是否能能够访问！\n'
                          '域名：%s\nIP地址：%s\n网站服务：%s' % (subdomain_info[i]['subdomain'],
                                                       subdomain_info[i]['ipAdd'],
                                                       subdomain_info[i]['subdomainBanner']
                                                       )
                          )
                    self.ws.write(i, 0, '网站存在但无法获得title')
                    self.ws.write(i, 2, subdomain_info[i]['subdomain'])
                    self.ws.write(i, 3, subdomain_info[i]['ipAdd'])
                    self.ws.write(i, 4, subdomain_info[i]['subdomainBanner'])
                    self.wb.save(self.now_time + '.xls')

                    if subdomain_info[i]['subdomainBanner'] is None or subdomain_info[i]['subdomainBanner'] == '':
                        print('该网站服务未找到')
                    else:
                        key_word = subdomain_info[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]

                        knowledge_json = {
                            "pageNo": 1,
                            "pageSize": 12,
                            "platPostDto": {
                                "postTitle": new_word,
                                "categoryId": ""
                            }
                        }
                        knowledge_api_return_json = requests.post(
                            knowledge_api_url, headers=header, json=knowledge_json).json()
                        knowledge_api_data = knowledge_api_return_json['data']
                        # 取的返回值的文章详情页面
                        plat_posts = knowledge_api_data['platPostSVos']
                        for knowledge in plat_posts:
                            knowledge_id = knowledge['postId']
                            print(
                                '相关文章链接''https://plat.wgpsec.org/knowledge/view/%s' % (knowledge_id))
                        if len(plat_posts) == 0:
                            print('暂时没有相关文章！QAQ')
                        print('\n\n')
                        i += 1

                # 正常域名的判断
                else:
                    print('网站标题：%s\n域名: %s\nIP地址：%s\n网站服务：%s' % (subdomain_info[i]['subdomainTitle'],
                                                                 subdomain_info[i]['subdomain'],
                                                                 subdomain_info[i]['ipAdd'],
                                                                 subdomain_info[i]['subdomainBanner']
                                                                 )
                          )
                    # 写入表格中
                    self.ws.write(i, 0, subdomain_info[i]['subdomainTitle'])
                    self.ws.write(i, 2, subdomain_info[i]['subdomain'])
                    self.ws.write(i, 3, subdomain_info[i]['ipAdd'])
                    self.ws.write(i, 4, subdomain_info[i]['subdomainBanner'])
                    self.wb.save(self.now_time + '.xls')

                    # 将搜索出来的subdomainBanner值作为知识库搜索的参数传入。判断subdomainBanner是否为未查询到或者是为空
                    if subdomain_info[i]['subdomainBanner'] is None or subdomain_info[i]['subdomainBanner'] == '':
                        print('该网站服务未找到')
                    # 进行知识库查询
                    else:
                        key_word = subdomain_info[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]

                        knowledge_json = {
                            "pageNo": 1,
                            "pageSize": 12,
                            "platPostDto": {
                                "postTitle": new_word,
                                "categoryId": ""
                            }
                        }
                        knowledge_api_return_json = requests.post(
                            knowledge_api_url, headers=header, json=knowledge_json).json()
                        knowledge_api_data = knowledge_api_return_json['data']
                        # 取的返回值的文章详情页面
                        plat_posts = knowledge_api_data['platPostSVos']
                        knowledge_size = len(plat_posts)
                        n = 0
                        while n < knowledge_size:
                            knowledge_id = plat_posts[n]['postId']  # 取出文章ID
                            print(
                                '相关文章链接: ''https://plat.wgpsec.org/knowledge/view/%s' % (knowledge_id))
                            n += 1
                        if n == 0:
                            print('暂时没有相关文章！QAQ')
                print('\n\n')
                i += 1
        # 获取报错
        except IndexError:  # 因为查询的条数目不一样，但是默认的pageSize是一样的，所以很多时候会存在一个问题就是没有那么多条，因为循环是和pageSize进行对比，会报错，就捕获这个错误
            print('当前库中只有%s条数据！' % i)
        finally:
            print('当前查询的城市为：%s 查询成功' % city)

    # 域名查询
    def host(self, host):
        search_api_url = 'https://plat.wgpsec.org/api/v1/ws/search'  # 搜索模块api链接
        knowledge_api_url = 'https://plat.wgpsec.org/api/post/queryPlatPost'  # 知识库api链接
        # key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
        #       'subdomainTitle',
        #       'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "authorization": self.cookies_read
        }
        search_json = {
            "pageNo": 1,
            "pageSize": self.page_size,
            "query": "ip=%s" % host,
            "type": "web"
        }

        search_api_return_json = requests.post(
            search_api_url, headers=header, json=search_json).json()
        # json 返回值里面会有3个key分别是：code、msg、data提取返回中的data值
        search_api_data = search_api_return_json['data']
        # data下面有wsDomainInfoDto、wsSubDomainInfoDtoList、wsPortInfoDtoList、wsUrlsInfoDtoList 目前只有wsSubDomainInfoDtoList存在可用信息，其他返回值为null，所以其他的参数不写
        subdomain_info_list = search_api_data['wsSubDomainInfoDtoList']
        # 查询出的域名和子域，列表的形式出来的，所以下方使用下标， # wsSubDomainInfoDtoList中有5个key，分别是wsSubDomainInfoDtos、pageSize、totalCount、pageNo、pages。所有的域名信息都在wsSubDomainInfoDtos里面，包括子域名
        subdomain_info = subdomain_info_list['wsSubDomainInfoDtos']
        i = 0
        try:
            while i < self.page_size:  # 遍历出我们插到的信息
                #
                if subdomain_info[i]['subdomainTitle'] == 'Not Found':
                    print('无法访问\n'
                          '域名： %s' % subdomain_info[i]['subdomain'])
                    self.ws.write(i, 0, '无法访问')
                    self.ws.write(i, 2, subdomain_info[i]['subdomain'])
                    self.ws.write(i, 3, subdomain_info[i]['ipAdd'])
                    self.ws.write(i, 4, subdomain_info[i]['subdomainBanner'])
                    self.wb.save(self.now_time + '.xls')
                    i += 1
                    print('\n\n')

                #
                elif subdomain_info[i]['subdomainTitle'] == None:
                    print('网站标题无法获取，但是存在，可手动查看是否能能够访问！\n'
                          '域名：%s\nIP地址：%s\n网站服务：%s' % (subdomain_info[i]['subdomain'],
                                                       subdomain_info[i]['ipAdd'],
                                                       subdomain_info[i]['subdomainBanner']
                                                       )
                          )
                    self.ws.write(i, 0, '网站存在但无法获得title')
                    self.ws.write(i, 2, subdomain_info[i]['subdomain'])
                    self.ws.write(i, 3, subdomain_info[i]['ipAdd'])
                    self.ws.write(i, 4, subdomain_info[i]['subdomainBanner'])
                    self.wb.save(self.now_time + '.xls')

                    if subdomain_info[i]['subdomainBanner'] == None:
                        print('该网站服务未找到')
                    else:
                        key_word = subdomain_info[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]

                        knowledge_json = {
                            "pageNo": 1,
                            "pageSize": 12,
                            "platPostDto": {
                                "postTitle": new_word,
                                "categoryId": ""
                            }
                        }
                        knowledge_api_return_json = requests.post(
                            knowledge_api_url, headers=header, json=knowledge_json).json()
                        knowledge_api_data = knowledge_api_return_json['data']
                        # 取的返回值的文章详情页面
                        plat_post = knowledge_api_data['platPostSVos']
                        knowledge_size = len(plat_post)
                        n = 0
                        while n < knowledge_size:
                            knowledge_id = plat_post[n]['postId']  # 取出文章ID
                            print(
                                '相关文章链接''https://plat.wgpsec.org/knowledge/view/%s' % (knowledge_id))
                            n += 1
                        if n == 0:
                            print('暂时没有相关文章！QAQ')
                        print('\n\n')
                        i += 1

                #
                else:
                    print('网站标题：%s\n域名: %s\nIP地址：%s\n网站服务：%s' % (subdomain_info[i]['subdomainTitle'],
                                                                 subdomain_info[i]['subdomain'],
                                                                 subdomain_info[i]['ipAdd'],
                                                                 subdomain_info[i]['subdomainBanner']
                                                                 )
                          )  # 这里我用的是下标，可以优化一下
                    self.ws.write(i, 0, subdomain_info[i]['subdomainTitle'])
                    self.ws.write(i, 2, subdomain_info[i]['subdomain'])
                    self.ws.write(i, 3, subdomain_info[i]['ipAdd'])
                    self.ws.write(i, 4, subdomain_info[i]['subdomainBanner'])
                    self.wb.save(self.now_time + '.xls')

                    # 将搜索出来的subdomainBanner值作为知识库搜索的参数传入。
                    if subdomain_info[i]['subdomainBanner'] == None or subdomain_info[i]['subdomainBanner'] == '':
                        print('该网站服务未找到')
                    else:
                        key_word = subdomain_info[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]

                        knowledge_json = {
                            "pageNo": 1,
                            "pageSize": 12,
                            "platPostDto": {
                                "postTitle": new_word,
                                "categoryId": ""
                            }
                        }
                        knowledge_api_return_json = requests.post(
                            knowledge_api_url, headers=header, json=knowledge_json).json()
                        knowledge_api_data = knowledge_api_return_json['data']
                        # 取的返回值的文章详情页面
                        plat_post = knowledge_api_data['platPostSVos']
                        knowledge_size = len(plat_post)
                        n = 0
                        while n < knowledge_size:
                            knowledge_id = plat_post[n]['postId']  # 取出文章ID
                            print(
                                '相关文章链接： ''https://plat.wgpsec.org/knowledge/view/%s' % (knowledge_id))
                            n += 1
                        if n == 0:
                            print('暂时没有相关文章！QAQ')
                print('\n\n')
                i += 1

        except IndexError:
            print('当前库中只有%s条数据！' % i)

        finally:
            print('ip：%s 查询成功' % host)

    # 标题查询
    def title(self, title):
        search_api_url = 'https://plat.wgpsec.org/api/v1/ws/search'  # 搜索模块api链接
        knowledge_api_url = 'https://plat.wgpsec.org/api/post/queryPlatPost'  # 知识库api链接
        # key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
        #        'subdomainTitle',
        #       'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "authorization": self.cookies_read
        }
        search_json = {
            "pageNo": 1,
            "pageSize": self.page_size,
            "query": "title=%s" % title,
            "type": "web"
        }
        search_api_return_json = requests.post(
            search_api_url, headers=header, json=search_json).json()
        # json 返回值里面会有3个key分别是：code、msg、data，提取返回中的data值
        search_api_data = search_api_return_json['data']
        # data下面有wsDomainInfoDto、wsSubDomainInfoDtoList、wsPortInfoDtoList、wsUrlsInfoDtoList 目前只有wsSubDomainInfoDtoList存在可用信息，其他返回值为null，所以其他的参数不写
        subdomain_info_list = search_api_data['wsSubDomainInfoDtoList']
        # wsSubDomainInfoDtoList中有5个key，分别是wsSubDomainInfoDtos、pageSize、totalCount、pageNo、pages。所有的域名信息都在wsSubDomainInfoDtos里面，包括子域名查询出的域名和子域，列表的形式出来的，所以下方使用下标
        subdomain_info = subdomain_info_list['wsSubDomainInfoDtos']

        i = 0
        try:
            while i < self.page_size:  # 遍历出我们插到的信息
                if subdomain_info[i]['subdomainTitle'] == 'Not Found':
                    print('无法访问\n'
                          '域名： %s' % subdomain_info[i]['subdomain'])
                    self.ws.write(i, 0, '无法访问')
                    self.ws.write(i, 2, subdomain_info[i]['subdomain'])
                    self.ws.write(i, 3, subdomain_info[i]['ipAdd'])
                    self.ws.write(i, 4, subdomain_info[i]['subdomainBanner'])
                    self.wb.save(self.now_time + '.xls')
                    i += 1
                    print('\n\n')

                elif subdomain_info[i]['subdomainTitle'] is None:
                    print('网站标题无法获取，但是存在，可手动查看是否能能够访问！\n'
                          '域名：%s\nIP地址：%s\n网站服务：%s' % (subdomain_info[i]['subdomain'],
                                                       subdomain_info[i]['ipAdd'],
                                                       subdomain_info[i]['subdomainBanner']
                                                       )
                          )
                    self.ws.write(i, 0, '网站存在但无法获得title')
                    self.ws.write(i, 2, subdomain_info[i]['subdomain'])
                    self.ws.write(i, 3, subdomain_info[i]['ipAdd'])
                    self.ws.write(i, 4, subdomain_info[i]['subdomainBanner'])
                    self.wb.save(self.now_time + '.xls')

                    if subdomain_info[i]['subdomainBanner'] == None:
                        print('该网站服务未找到')
                    else:
                        key_word = subdomain_info[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]

                        knowledge_json = {
                            "pageNo": 1,
                            "pageSize": 12,
                            "platPostDto": {
                                "postTitle": new_word,
                                "categoryId": ""
                            }
                        }
                        knowledge_api_return_json = requests.post(
                            knowledge_api_url, headers=header, json=knowledge_json).json()
                        knowledge_api_data = knowledge_api_return_json['data']
                        # 取的返回值的文章详情页面
                        plat_post = knowledge_api_data['platPostSVos']
                        knowledge_size = len(plat_post)
                        n = 0
                        while n < knowledge_size:
                            knowledge_id = plat_post[n]['postId']  # 取出文章ID
                            print(
                                '相关文章链接''https://plat.wgpsec.org/knowledge/view/%s' % (knowledge_id))
                            n += 1
                            if n == 0:
                                print('暂时没有相关文章！QAQ')
                            print('\n\n')
                            i += 1

                else:
                    print('网站标题：%s\n域名: %s\nIP地址：%s\n网站服务：%s' % (subdomain_info[i]['subdomainTitle'],
                                                                 subdomain_info[i]['subdomain'],
                                                                 subdomain_info[i]['ipAdd'],
                                                                 subdomain_info[i]['subdomainBanner']
                                                                 )
                          )  # 这里我用的是下标，可以优化一下
                    self.ws.write(i, 0, subdomain_info[i]['subdomainTitle'])
                    self.ws.write(i, 2, subdomain_info[i]['subdomain'])
                    self.ws.write(i, 3, subdomain_info[i]['ipAdd'])
                    self.ws.write(i, 4, subdomain_info[i]['subdomainBanner'])
                    self.wb.save(self.now_time + '.xls')

                    # 将搜索出来的subdomainBanner值作为知识库搜索的参数传入。
                    if subdomain_info[i]['subdomainBanner'] is None or subdomain_info[i]['subdomainBanner'] == '':
                        print('该网站服务未找到')
                    else:
                        key_word = subdomain_info[i]['subdomainBanner']
                        del_word = key_word.find('/')
                        if del_word == -1:
                            new_word = key_word
                        else:
                            new_word = key_word[0:del_word]

                        Knowledge_json = {
                            "pageNo": 1,
                            "pageSize": 12,
                            "platPostDto": {
                                "postTitle": new_word,
                                "categoryId": ""
                            }
                        }
                        Knowledge_api_return_json = requests.post(
                            knowledge_api_url, headers=header, json=Knowledge_json).json()
                        Knowledge_api_data = Knowledge_api_return_json['data']
                        # 取的返回值的文章详情页面
                        plat_post = Knowledge_api_data['platPostSVos']
                        knowledge_size = len(plat_post)
                        n = 0
                        while n < knowledge_size:
                            knowledge_id = plat_post[n]['postId']  # 取出文章ID
                            print(
                                '相关文章链接： ''https://plat.wgpsec.org/knowledge/view/%s' % (knowledge_id))
                            n += 1
                        if n == 0:
                            print('暂时没有相关文章！QAQ')
                print('\n\n')
                i += 1

        except IndexError:
            print('当前库中只有%s条数据！' % i)

        finally:
            print('网站标题为："%s" 查询成功' % title)

    # 端口查询
    def port(self, port):
        search_api_url = 'https://plat.wgpsec.org/api/v1/ws/search'  # 搜索模块api链接
        knowledge_api_url = 'https://plat.wgpsec.org/api/post/queryPlatPost'  # 知识库api链接
        key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
               'subdomainTitle',
               'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "authorization": self.cookies_read
        }
        search_json = {
            "pageNo": 1,
            "pageSize": self.page_size,
            "query": "port=%s" % port,
            "type": "web"
        }

        search_api_return_json = requests.post(
            search_api_url, headers=header, json=search_json).json()
        # json 返回值里面会有3个key分别是：code、msg、data提取返回中的data值
        search_api_data = search_api_return_json['data']
        # data下面有wsDomainInfoDto、wsSubDomainInfoDtoList、wsPortInfoDtoList、wsUrlsInfoDtoList 目前只有wsSubDomainInfoDtoList存在可用信息，其他返回值为null，所以其他的参数不写
        wsSubDomainInfoDtoList = search_api_data['wsSubDomainInfoDtoList']
        # 查询出的域名和子域，列表的形式出来的，所以下方使用下标，wsSubDomainInfoDtoList中有5个key，分别是wsSubDomainInfoDtos、pageSize、totalCount、pageNo、pages。所有的域名信息都在wsSubDomainInfoDtos里面，包括子域名
        wsSubDomainInfoDtos = wsSubDomainInfoDtoList['wsSubDomainInfoDtos']
        i = 0
        try:
            while i < self.page_size:  # 遍历出我们插到的信息
                #
                if wsSubDomainInfoDtos[i]['subdomainTitle'] == 'Not Found':
                    print('无法访问\n'
                          '域名： %s' % wsSubDomainInfoDtos[i]['subdomain']
                          )

                    self.ws.write(i, 0, '无法访问')
                    self.ws.write(i, 2, wsSubDomainInfoDtos[i]['subdomain'])
                    self.ws.write(i, 3, wsSubDomainInfoDtos[i]['ipAdd'])
                    self.ws.write(i, 4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    self.wb.save(self.now_time + '.xls')
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
                    self.ws.write(i, 0, '网站存在但无法获得title')
                    self.ws.write(i, 2, wsSubDomainInfoDtos[i]['subdomain'])
                    self.ws.write(i, 3, wsSubDomainInfoDtos[i]['ipAdd'])
                    self.ws.write(i, 4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    self.wb.save(self.now_time + '.xls')
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
                                "postTitle": new_word,
                                "categoryId": ""
                            }
                        }
                        knowledge_api_return_json = requests.post(
                            knowledge_api_url, headers=header, json=knowledge_json).json()
                        knowledge_api_data = knowledge_api_return_json['data']
                        # 取的返回值的文章详情页面
                        platPostSVos = knowledge_api_data['platPostSVos']
                        knowledge_size = len(platPostSVos)
                        n = 0
                        while n < knowledge_size:
                            knowledge_id = platPostSVos[n]['postId']  # 取出文章ID
                            print(
                                '相关文章链接''https://plat.wgpsec.org/knowledge/view/%s' % (knowledge_id))
                            n += 1
                        if n == 0:
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
                          )  # 这里我用的是下标，可以优化一下
                    self.ws.write(i, 0, wsSubDomainInfoDtos[i]['subdomainTitle'])
                    self.ws.write(i, 2, wsSubDomainInfoDtos[i]['subdomain'])
                    self.ws.write(i, 3, wsSubDomainInfoDtos[i]['ipAdd'])
                    self.ws.write(i, 4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    self.wb.save(self.now_time + '.xls')

                    # 将搜索出来的subdomainBanner值作为知识库搜索的参数传入。
                    if wsSubDomainInfoDtos[i]['subdomainBanner'] == None or wsSubDomainInfoDtos[i]['subdomainBanner'] == '':
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
                                "postTitle": new_word,
                                "categoryId": ""
                            }
                        }
                        Knowledge_api_return_json = requests.post(
                            knowledge_api_url, headers=header, json=knowledge_json).json()
                        Knowledge_api_data = Knowledge_api_return_json['data']
                        # 取的返回值的文章详情页面
                        platPostSVos = Knowledge_api_data['platPostSVos']
                        knowledge_size = len(platPostSVos)
                        n = 0
                        while n < knowledge_size:
                            knowledge_id = platPostSVos[n]['postId']  # 取出文章ID
                            print(
                                '相关文章链接： ''https://plat.wgpsec.org/knowledge/view/%s' % (knowledge_id))
                            n += 1
                        if n == 0:
                            print('暂时没有相关文章！QAQ')
                print('\n\n')
                i += 1

        except IndexError:
            print('当前库中只有%s条数据！' % i)

        finally:
            print('端口为：%s 查询成功' % port)

    def ip_port(self, ip, port):
        search_api_url = 'https://plat.wgpsec.org/api/v1/ws/search'  # 搜索模块api链接
        knowledge_api_url = 'https://plat.wgpsec.org/api/post/queryPlatPost'  # 知识库api链接
        key = ['id', 'subdomain', 'ipAdd', 'host', 'cdn', 'city', 'status', 'dnsType', 'subdomainLevel',
               'subdomainTitle',
               'subdomainBanner', 'subdomainReason', 'subdomainStatus', 'addTime', 'wsUrlsInfoDto']
        header = {
            "authorization": cookies_read
        }
        search_json = {
            "pageNo": 1,
            "pageSize": pageSize,
            "query": "ip=%s|port=%s" % (ip, port),
            "type": "web"
        }

        search_api_return_json = requests.post(
            search_api_url, headers=header, json=search_json).json()

        # json 返回值里面会有3个key分别是：code、msg、data
        search_api_data = search_api_return_json['data']  # 提取返回中的data值

        # data下面有wsDomainInfoDto、wsSubDomainInfoDtoList、wsPortInfoDtoList、wsUrlsInfoDtoList 目前只有wsSubDomainInfoDtoList存在可用信息，其他返回值为null，所以其他的参数不写

        # wsPortInfoDtoList = api_data['wsPortInfoDtoList']

        wsSubDomainInfoDtoList = search_api_data['wsSubDomainInfoDtoList']

        # wsSubDomainInfoDtoList中有5个key，分别是wsSubDomainInfoDtos、pageSize、totalCount、pageNo、pages。所有的域名信息都在wsSubDomainInfoDtos里面，包括子域名
        # 查询出的域名和子域，列表的形式出来的，所以下方使用下标
        wsSubDomainInfoDtos = wsSubDomainInfoDtoList['wsSubDomainInfoDtos']
        i = 0
        try:
            while i < pageSize:  # 遍历出我们插到的信息
                if wsSubDomainInfoDtos[i]['subdomainTitle'] == 'Not Found':
                    print('无法访问\n'
                          '域名： %s' % wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i, 0, '无法访问')
                    ws.write(i, 2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i, 3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i, 4, wsSubDomainInfoDtos[i]['subdomainBanner'])
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
                    ws.write(i, 0, '网站存在但无法获得title')
                    ws.write(i, 2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i, 3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i, 4, wsSubDomainInfoDtos[i]['subdomainBanner'])
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
                                "postTitle": new_word,
                                "categoryId": ""
                            }
                        }
                        knowledge_api_return_json = requests.post(
                            knowledge_api_url, headers=header, json=knowledge_json).json()
                        knowledge_api_data = knowledge_api_return_json['data']
                        # 取的返回值的文章详情页面
                        platPostSVos = knowledge_api_data['platPostSVos']
                        knowledge_size = len(platPostSVos)
                        n = 0
                        while n < knowledge_size:
                            knowledge_id = platPostSVos[n]['postId']  # 取出文章ID
                            print(
                                '相关文章链接''https://plat.wgpsec.org/knowledge/view/%s' % (knowledge_id))
                            n += 1
                        if n == 0:
                            print('暂时没有相关文章！QAQ')
                        print('\n\n')
                        i += 1

                else:
                    print('网站标题：%s\n域名: %s\nIP地址：%s\n网站服务：%s' % (wsSubDomainInfoDtos[i]['subdomainTitle'],
                                                                 wsSubDomainInfoDtos[i]['subdomain'],
                                                                 wsSubDomainInfoDtos[i]['ipAdd'],
                                                                 wsSubDomainInfoDtos[i]['subdomainBanner']
                                                                 )
                          )  # 这里我用的是下标，可以优化一下
                    ws.write(i, 0, wsSubDomainInfoDtos[i]['subdomainTitle'])
                    ws.write(i, 2, wsSubDomainInfoDtos[i]['subdomain'])
                    ws.write(i, 3, wsSubDomainInfoDtos[i]['ipAdd'])
                    ws.write(i, 4, wsSubDomainInfoDtos[i]['subdomainBanner'])
                    wb.save(now_time + '.xls')

                    # 将搜索出来的subdomainBanner值作为知识库搜索的参数传入。
                    if wsSubDomainInfoDtos[i]['subdomainBanner'] == None or wsSubDomainInfoDtos[i]['subdomainBanner'] == '':
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
                                "postTitle": new_word,
                                "categoryId": ""
                            }
                        }
                        knowledge_api_return_json = requests.post(
                            knowledge_api_url, headers=header, json=knowledge_json).json()
                        Knowledge_api_data = Knowledge_api_return_json['data']
                        # 取的返回值的文章详情页面
                        platPostSVos = Knowledge_api_data['platPostSVos']
                        knowledge_size = len(platPostSVos)
                        n = 0
                        while n < knowledge_size:
                            knowledge_id = platPostSVos[n]['postId']  # 取出文章ID
                            print(
                                '相关文章链接： ''https://plat.wgpsec.org/knowledge/view/%s' % (knowledge_id))
                            n += 1
                        if n == 0:
                            print('暂时没有相关文章！QAQ')
                print('\n\n')
                i += 1
        except IndexError:
            print('当前库中只有%s条数据！' % i)

        finally:
            print('查询的IP为：%s、端口为：%s 查询成功' % (ip, port))
            sys.exit()