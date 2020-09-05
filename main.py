import argparse
from Script.Welcome import Wgpbanner
from Controller.Controller import WgpIG


def main():

    parser = argparse.ArgumentParser()
    parser.description = ('嗨！你好！\n'
                          '当你看到这里的时候，很高兴你已经成为了我们的一员！\n')

    parser.add_argument('-l', '--login', help='登陆')
    parser.add_argument('-t', '--type', help='(web|host)', default='')
    # parser.add_argument('-s', '--search', default='')
    parser.add_argument('-q', '--query', help='(port|host|title|ip|city)', default='')
    parser.add_argument('-k', '--keyword', help='enable knowledge api', default='')
    args = parser.parse_args()
    username = args.login
    type = args.type
    query = args.query
    keyword = args.keyword
    print(Wgpbanner())
    WgpIG().Start(username, type, query, keyword)

if __name__ == '__main__':
    main()




