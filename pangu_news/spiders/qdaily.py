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


class QdailyCreeper(scrapy.Spider):
    """docstring for QdailyCreeper"""
    name = "qdaily"
    allowed_domains = ["qdaily.com"]
    start_urls = ["http://www.qdaily.com/"]

    def parse_item(self, response):
        item = response.meta['item']
        news_list = response.xpath('//div[@class="detail"]').extract()
        if len(news_list) == 0:
            return
        content = news_list[0]
        item['content'] = content.replace("\r\n", "").replace("\n", "")
        file = open("out_file/qdaily.txt", "ab")
        try:
            file.write(
                ("\t".join([item['time_str'], item['url'], item['title'], item['content']]) + "\n").encode('utf-8'))
        finally:
            file.close()
        row_key = md5(item['url'].encode('utf-8')).hexdigest()
        one = {"time": item['time_str'], "url": item['url'], "title": item['title'], 'content': item['content']}
        with open("%s/%s" % (item["file_path"], row_key), "w") as f:
            f.write(json.dumps(one))

    def parse(self, response):
        file_path = "out_file/%s/%s" % (self.name, str(datetime.datetime.today().date()))
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        for line_a in response.xpath('//div[@class="packery-item article"]'):
            item = PanguNewsItem()
            item['time_str'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['url'] = line_a.xpath('./a/@href').extract()[0]
            if item['url'].startswith('/'):
                item['url'] = "http://www.qdaily.com" + item['url']
            item['title'] = line_a.xpath('./a//img/@alt').extract()[0]
            item['file_path'] = file_path
            yield Request(item['url'], meta={'item': item}, callback=self.parse_item)
