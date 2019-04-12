# -*- coding:utf-8 -*-
# 这个类主要用于产生随机的UserAgent

import random

class RandomUserAgent(object):

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        # 返回的是本类的实例cls == RandomUserAgent
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))

