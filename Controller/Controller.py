import sys
from Core.Login import Login
from Core.Search import Search
from Core.CheckRealLogin import Check

class WgpIG(object):
    def __init__(self):
        self.login = Login()
        self.search = Search()
        self.check = Check()

    def _login(self, username):
        self.login.verify(username)

    def _search(self, type, query, keyword):
        search = self.search
        if type != '' and query != '':
            search.requests_search_api(type, query)
        if keyword != '':
            search.requests_kownledge_search_api(keyword)

    def Start(self, username, type, query, keyword):
        if not self.check.run():
            self._login(username)
        self._search(type, query, keyword='')
        if keyword != '':
            self._search(type='', query='', keyword=keyword)


