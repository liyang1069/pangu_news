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


class QQSportsCreeper(scrapy.Spider):
    """docstring for QQCreeper"""
    name = "qq_sports"
    allowed_domains = ["qq.com"]
    start_urls = ["http://sports.qq.com/"]

    def parse_item(self, response):
        item = response.meta['item']
        news_list = response.xpath('//div[@id="Cnt-Main-Article-QQ"]').extract()
        if len(news_list) == 0:
            return
        content = news_list[0]
        item['content'] = content.replace("\r\n", "").replace("\n", "")
        row_key = md5(item['url'].encode('utf-8')).hexdigest()
        one = {"time": item['time_str'], "url": item['url'], "title": item['title'], 'content': item['content']}
        with open("%s/%s" % (item["file_path"], row_key), "w") as f:
            f.write(json.dumps(one))

    def parse(self, response):
        file_path = "out_file/%s/%s" % (self.name, str(datetime.datetime.today().date()))
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        for line_a in response.xpath('//div[@class="scr-news"]//a[@class="newsv"]'):
            item = PanguNewsItem()
            item['time_str'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['url'] = line_a.xpath('@href').extract()[0]
            item['title'] = line_a.xpath('text()').extract()[0]
            item['file_path'] = file_path
            yield Request(item['url'], meta={'item': item}, callback=self.parse_item)
