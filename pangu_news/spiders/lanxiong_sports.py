#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
import json
import scrapy
import datetime
import urllib
import urllib2
from hashlib import md5
from pangu_news.items import PanguNewsItem
from scrapy.http import Request


class LanxiongSportsSpider(scrapy.Spider):

    name = 'lanxiong_sports'
    allowed_domains = ['lanxiongsports.com']
    start_urls = ['http://www.lanxiongsports.com/']
    # cid: category id, page: page id
    api_url = "http://www.lanxiongsports.com/mservice/?c=news&a=index&format=json&cid=%d&page=%d"
    cids = [0, 12]
    page_ids = [1, 2]

    def _get_str_by_url(self, url_str):
        try:
            req = urllib2.Request(url_str)
            res_data = urllib2.urlopen(req)
            return res_data.read()
        except:
            pass
        return ""

    def parse(self, response):
        file_path = "out_file/%s/%s" % (self.name, str(datetime.datetime.today().date()))
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        for c in self.cids:
            for p in self.page_ids:
                r = self._get_str_by_url(self.api_url % (c, p))
                items = json.loads(r).get("items", [])
                print len(r), len(items)
                for news in items:
                    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    news_id = news.get("id", "")
                    title = news.get("title", "")
                    url = news.get("url", "")
                    if len(url) < 1:
                        url = "http://www.lanxiongsports.com/?c=posts&a=view&id=%s" % news_id
                    content = self._get_str_by_url(url)
                    try:
                        start_index = content.index('<div class="top or  imagecontent"')
                        end_index = content.index('<div class="bottom or">')
                    except:
                        start_index, end_index = 0, 0
                    if 0 < start_index < end_index:
                        content = content[start_index:end_index]
                    else:
                        continue
                    one = {"time": time_str, "url": url, "title": title, "content": content}
                    row_key = md5(url.encode('utf-8')).hexdigest()
                    with open("%s/%s" % (file_path, row_key), "w") as f:
                        f.write(json.dumps(one))
