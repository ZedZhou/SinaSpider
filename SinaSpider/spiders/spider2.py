# -*- coding: utf-8 -*-
import scrapy


class Spider2Spider(scrapy.Spider):
    name = "spider2"
    allowed_domains = ["www.douban.com"]
    start_urls = ['http://www.douban.com/']

    def parse(self, response):
        pass
