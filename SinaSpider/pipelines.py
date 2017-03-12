# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from .items import InfoItem,FollowsItem,WeiboItem



class SinaspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient("localhost", 27017)
        db = client['Sina']
        self.Info = db['Info']
        self.Follows = db['Follows']
        self.Contents = db['Contents']

    def process_item(self,item,spider):

        if isinstance(item, InfoItem):
            self.Info.insert(dict(item))

        if isinstance(item, FollowsItem):
            self.Follows.insert(dict(item))

        if isinstance(item, WeiboItem):
            self.Contents.insert(dict(item))

        return item
