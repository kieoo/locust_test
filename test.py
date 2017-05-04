# !/bin/env python

from locust import task, Locust, TaskSet, events
import imaplib
import queue


class UserBehavior(TaskSet):

    def on_start(self):
        self.login()

    def login(self):
        user = self.locust.user_data_queue.get().strip()
        self.server = imaplib.IMAP4_SSL('192.168.202.252')
        response = self.server.login(user, '123')
        print(response)
        self.locust.user_data_queue.put_nowait(user)

    @task
    def get_mail(self):
        response = self.server.select(mailbox='INBOX')
        print(response)
'''
    @task
    def log_out(self):
        self.interrupt()
'''


class ImapUser(Locust):
    host = '192.168.202.252'
    user_data_queue = queue.Queue()
    with open('D:/locust_test/userlist', 'r') as fq:
        for i in fq:
            user_data_queue.put_nowait(i)
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 10000
