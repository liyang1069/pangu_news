#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import time
import json
import scrapy
import datetime
from hashlib import md5
from pangu_news.items import PanguNewsItem
from scrapy.http import Request


class EntHuabianSpider(scrapy.Spider):
    name = 'ent_huabian'
    allowed_domains = ['huabian.com']
    start_urls = ['http://huabian.com/']

    def parse_item(self, response):
        item = response.meta['item']
        news_list = response.xpath('//div[@class="hb_content"]').extract()
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
        line_list = []
        for line_a in response.xpath('//div[@class="hb_block_mix"]//h3//a'):
            line_list.append(line_a)
        for line_a in response.xpath('//section[@id="hb_scroll"]//h3//a'):
            line_list.append(line_a)
        for line_a in line_list:
            item = PanguNewsItem()
            item['time_str'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['url'] = line_a.xpath('@href').extract()[0]
            if ".html" not in item['url']:
                continue
            item['url'] = "http:" + item['url']
            if len(line_a.xpath('text()').extract()) > 0:
                item['title'] = line_a.xpath('text()').extract()[0]
            else:
                print "================", line_a
            item['file_path'] = file_path
            yield Request(item['url'], meta={'item': item}, callback=self.parse_item)
