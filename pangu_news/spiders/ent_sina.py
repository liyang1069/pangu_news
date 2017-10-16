#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
import json
import scrapy
import datetime
from hashlib import md5
from pangu_news.items import PanguNewsItem
from scrapy.http import Request


class EntSinaSpider(scrapy.Spider):
    name = 'ent_sina'
    allowed_domains = ['sina.com.cn']
    OffsiteMiddleware = ['huati.weibo.com']
    start_urls = ['http://ent.sina.com.cn/']

    def parse_item(self, response):
        item = response.meta['item']
        news_list = response.xpath('//div[@id="artibody"]').extract()
        if len(news_list) == 0:
            return
        content = news_list[0]
        item['content'] = content.replace("\r\n", "").replace("\n", "")
        row_key = md5(item['url'].encode('utf-8')).hexdigest()
        one = {"time": item['time_str'], "url": item['url'], "title": item['title'], 'content': item['content']}
        with open("%s/%s" % (item["file_path"], row_key), "w") as f:
            f.write(one['content'])
            # f.write(json.dumps(one))

    def parse(self, response):
        file_path = "out_file/%s/%s" % (self.name, str(datetime.datetime.today().date()))
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        for line_a in response.xpath('//div[@id="ty-top-ent0"]//a') + response.xpath('//div[@id="j_cardlist"]//a'):
            item = PanguNewsItem()
            item['time_str'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['url'] = line_a.xpath('@href').extract()[0]
            if ".shtml" in item['url'] or ".html" in item['url'] or len(item['url']) > 500:
                continue
            item['title'] = line_a.xpath('text()').extract()[0]
            item['file_path'] = file_path
            yield Request(item['url'], meta={'item': item}, callback=self.parse_item)
