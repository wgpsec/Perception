import os

from Core.Login import Login
from Core.Search import Search
from Core.CheckRealLogin import Check
from Core.CreateWolfScan import WolfScan

class WgpIG(object):
    def __init__(self):
        self.login = Login()
        self.search = Search()
        self.check = Check()
        self.wolfscan = WolfScan()

    def _login(self, username):
        self.login.verify(username)

    def _search(self, type, query, keyword, export):
        search = self.search
        if type != '' and query != '':
            search.requests_search_api(type, query, export)
        if keyword != '':
            search.requests_kownledge_search_api(keyword)

    def _createwolfscan(self, url):
        wolfscan = self.wolfscan
        if url != None or url != '':
            wolfscan.requests_create_wolfscan_api(url)

    def Start(self, username, url, type, query, keyword, export):
        if not os.path.exists('Output/'):
            os.mkdir('Output/')
        if not self.check.run():
            self._login(username)
        self._search(type, query, keyword='', export=export)
        if keyword != '':
            self._search(type='', query='', keyword=keyword, export=export)
        if url != None and url != '':
            self._createwolfscan(url)


