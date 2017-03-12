# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class SinaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class InfoItem(scrapy.Item):
    """个人信息"""
    _id = Field()
    Nick = Field()
    Gender = Field()
    Province = Field()
    City = Field()
    Signature = Field()
    Birthday = Field()
    Num_weibo = Field()
    Num_follows = Field()
    Num_fans = Field()
    Home_url = Field()


class WeiboItem(scrapy.Item):
    """ 微博信息"""
    _id = Field()
    User_id = Field()
    Content = Field()
    Pubtime = Field()
    Pubaddr = Field()
    Tool = Field()
    Like = Field()
    Comment = Field()
    Transfer = Field()

class FollowsItem(scrapy.Item):
    """关注的人"""
    _id = Field()
    follows = Field()


class FansItem(scrapy.Item):
    """粉丝"""
    _id = Field()
    fans = Field()