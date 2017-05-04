# !/bin/env python

from locust import task, Locust, TaskSet, events
from locust import HttpLocust
from urllib import request, parse
import re
import queue


class UserBehavior(TaskSet):
    sid = ''

    def on_start(self):
        self.login()

    def login(self):
        data = {'uid': 'admin', 'password': '1', 'action:login': ''}
        data_en = parse.urlencode(data)

        with self.client.post('/coremail/index.jsp?cus=1', data, catch_response=True, name='login') as r:
            respons_header = r.headers['Set-Cookie']
            print('>>>>>>>>>>%s' % respons_header)
            self.sid = re.compile(r'sid=(\w+);').search(respons_header).groups()[0]
            print('%s', self.sid)

    @task
    def get_folders(self):
        data = {'stats': 'true', 'threads': 'true'}
        with self.client.post('/coremail/XT5/jsp/mail.jsp?func=getAllFolders&sid='+self.sid,
                              data, catch_response=True, name='getFolder') as r:
            respons_content = r.content.decode('utf-8')
            print('%s', respons_content)
            r.success()


class CoremailUser(HttpLocust):
    host = 'http://192.168.202.252'
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 10000
    stop_timeout = 60


