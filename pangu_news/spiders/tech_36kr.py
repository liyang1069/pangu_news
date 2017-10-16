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


class Tech36krSpider(scrapy.Spider):

    name = 'tech_36kr'
    allowed_domains = ['36kr.com']
    start_urls = ['http://36kr.com/']

    def parse_item(self, response):
        print response.body
        item = response.meta['item']
        news_list = response.xpath('//section[class="textblock"]').extract()
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
        body = str(response.body)
        start_sign, end_sign = "var props=", ",locationnal="
        if start_sign not in body or end_sign not in body:
            return
        try:
            props = json.loads(body[body.index(start_sign) + len(start_sign):body.index(end_sign)])
            keys = ["hotLinks|hotLinks", "hotTags|hotTags", "highProjects|focus", "editorChoice|focus"]
            links = []
            for k in keys:
                links.extend(props.get(k, []))
                print len(links)
        except:
            return
        for line_a in links[:1]:
            if "title" not in line_a or "url" not in line_a:
                continue
            item = PanguNewsItem()
            item['time_str'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['url'] = line_a["url"]
            item['title'] = line_a["title"]
            item['file_path'] = file_path
            yield Request(item['url'], meta={'item': item}, callback=self.parse_item)

