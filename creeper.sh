#!/bin/bash

cd /opt/creeperpy/

source venv/bin/activate

scrapy crawl qqnews

scrapy crawl qdaily

scrapy crawl sina_news

scrapy crawl ent_huabian

scrapy crawl ent_sina

scrapy crawl finance_caijingnet

scrapy crawl finance_hexun

scrapy crawl lanxiong_sports

scrapy crawl qq_sports

scrapy crawl tech_36kr

