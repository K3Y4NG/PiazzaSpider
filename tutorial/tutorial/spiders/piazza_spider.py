#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
Python crawler for scratching information from Piazza

Author: Keyang Ru
Data: 2018-09-12
"""

import scrapy
from scrapy.utils.response import open_in_browser

class PiazzaSpider(scrapy.Spider):
    name = "piazza"
    allowed_domains = ["www.piazza.com"]
    start_urls = ["https://piazza.com/class/isccqbm3kzy7kq"]
    headers = {
        'Host': 'piazza.com',
        'Connection' : 'keep-alive',
        'Content-Length': '70',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Origin': 'https://piazza.com',
        'Referer': 'https://piazza.com/'
    }

    def start_requests(self):
        return [scrapy.Request("https://piazza.com/class/isccqbm3kzy7kq",
                               meta={'cookiejar': 1},
                               callback=self.post_login)]

    def post_login(self, response):
        print('Preparing Login')
        return [scrapy.FormRequest.from_response(response,
                                                 meta = {'cookiejar' : response.meta['cookiejar']},
                                                 headers  = self.headers,
                                                 formdata = {
                                                     'from' : '/signup',
                                                     'email' : 'keyangru@usc.edu',
                                                     'password' : 'r12345678',
                                                     'remember' : 'on',
                                                 },
                                                 callback = self.after_login,
                                                 dont_filter = True
                                                 )]

    def after_login(self, response):
      open_in_browser(response)


