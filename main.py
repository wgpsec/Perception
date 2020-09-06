import argparse
from Script.Welcome import Wgpbanner
from Controller.Controller import WgpIG


def main():

    parser = argparse.ArgumentParser()
    parser.description = ('嗨！你好！\n'
                          '当你看到这里的时候，很高兴你已经成为了我们的一员！\n')

    parser.add_argument('-l', '--login', help='登陆')
    parser.add_argument('-t', '--type', help='(web|host)', default='')
    parser.add_argument('-u', '--url', help='需要添加扫描的域名')
    parser.add_argument('-q', '--query', help='(port|host|title|ip|city)', default='')
    parser.add_argument('-k', '--keyword', help='enable knowledge api', default='')
    parser.add_argument('-e', '--export', help='查询结果保存的文件路径', default='')
    args = parser.parse_args()
    username = args.login
    type = args.type
    url = args.url
    query = args.query
    keyword = args.keyword
    export = args.export
    print(Wgpbanner())
    WgpIG().Start(username, url, type, query, keyword, export)

if __name__ == '__main__':
    main()




