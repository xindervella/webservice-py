# -*- coding: utf-8 -*-
# @Date    : 2014-06-25 21:23:32
# @Author  : xindervella@gamil.com
from BeautifulSoup import BeautifulSoup
from config import CURR_URL, TIME_OUT
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import tornado.web
import tornado.gen
import json
import urllib
import re


class SidebarHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        cardnum = self.get_argument('cardnum', default=None)
        term = self.get_argument('term', default=None)
        if not (cardnum or term):
            self.write('params lack')
        else:
            params = urllib.urlencode(
                {'queryStudentId': cardnum,
                 'queryAcademicYear': term}
            )
            client = AsyncHTTPClient()
            request = HTTPRequest(CURR_URL, body=params, method='POST',
                                  request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            body = response.body
            if not body:
                self.write('time out')
            else:
                pat = re.compile(ur'没有找到该学生信息', re.U)
                match = pat.search(body)
                if match:
                    self.write('card number not exist')
                else:
                    self.write(self.parser(body))
        self.finish()

    def parser(self, html):
        soup = BeautifulSoup(html)
        items = soup.findAll('td', height='34', width='35%')[:-1]
        items = [item for item in items if item.text != u'&nbsp;']
        sidebar = []
        for item in items:
            sidebar.append(
                {'course': item.text,
                 'lecturer': self.next_n_sibling(item, 2).text[6:],
                 'credit': self.next_n_sibling(item, 4).text[6:],
                 'week': self.next_n_sibling(item, 6).text[6:]
                 })
        return json.dumps(sidebar, ensure_ascii=False, indent=2)

    def next_n_sibling(self, item, n):
        for i in xrange(n):
            item = item.nextSibling
        return item
