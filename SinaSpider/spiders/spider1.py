# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import datetime
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from ..items import InfoItem, WeiboItem, FansItem, FollowsItem
import re
from datetime import datetime


class Spider1Spider(CrawlSpider):
    name = "spider1"
    host = "http://weibo.cn"
    # start_urls = [2257706691,1756807885,872974635,2590078853，2694918490]
    'http://weibo.cn/u/872974635/'
    start_urls = [2694918490,]

    crawl_ID = set(start_urls)
    finish_ID = set()

    def start_requests(self):
        while len(self.crawl_ID):
            ID = self.crawl_ID.pop()  # 取出一个ID
            self.finish_ID.add(ID)    # 添加一个ID
            ID = str(ID)
            follow = []
            followsItem = FollowsItem()
            followsItem['_id'] = ID
            followsItem['follows'] = follow
            fansItem = FansItem()
            fans = []
            fansItem['_id'] = ID
            fansItem['fans'] = fans

            url_follows = "http://weibo.cn/%s/follow" % (ID,)  # 关注连接
            url_fans = "http://weibo.cn/%s/fans" % (ID,)        # 粉丝连接
            url_info = "http://weibo.cn/%s" % (ID,)     # 个人主页

            yield Request(url=url_info, meta={'ID': ID}, callback=self.parse_info_1,)
            # yield Request(url=url_info, meta={'ID': ID, 'n': 2}, callback=self.parse_weibo,)
            yield Request(url=url_follows, meta={'Item': followsItem, 'list': follow, 'n':1}, callback=self.parse_follow_or_fans)

    def parse_info_1(self, response):
        """
    _id = Field()
    Nick = Field()
    Gender = Field()
    Province = Field()
    City = Field()
    Signature = Field()
    Birthday = Field()
    Num_weibo = Field()
    Num_fllows = Field()
    Num_fans = Field()
    Home_url = Field()
        """
        infoItem = InfoItem()
        infoItem['_id'] = response.meta['ID']

        Num_weibo = response.xpath('//span[@class="tc"]/text()').extract()[0].split('[')[-1][:-1]
        Num_follows = response.xpath('//div[@class="tip2"]/a[1]/text()').extract()[0].split('[')[-1][:-1]
        Num_fans = response.xpath('//div[@class="tip2"]/a[2]/text()').extract()[0].split('[')[-1][:-1]

        info_url = self.host + '/' + response.meta['ID'] + '/info'

        infoItem['Num_follows'] = int(Num_follows)
        infoItem['Num_fans'] = int(Num_fans)
        infoItem['Num_weibo'] = int(Num_weibo)
        print('关注数:' + Num_follows)
        print('粉丝数:' + Num_fans)
        print('微博数:' + Num_weibo)
        '/html/body/div[2]/table/tr/td[2]/div/a[2]/@href'
        # info2_url = self.host + response.xpath('/html/body/div[2]/table/tr/td[2]/div/a[2]/@href').extract_first()
        yield Request(url=info_url, meta={"item": infoItem}, callback=self.parse_info_2)


    def parse_info_2(self,response):
        """进一步抓取个人信息"""
        try:
            infoItem = response.meta['item']
            text1 = ";".join(response.xpath('body/div[@class="c"]/text()').extract())
            Nickname = re.findall(r'昵称:(.*?);', text1)
            gender = re.findall(r'性别:(.*?);', text1)
            addr = re.findall(r'地区:(.*?);', text1)[0].split(' ')
            birth = re.findall(r'生日:(.*?);',text1)
            Signature = re.findall(r'简介:(.*?);',text1)
            Home_url = re.findall(r'互联网:(.*?);',text1)
        except Exception as e:
            print(e)
        if Nickname:
            infoItem['Nick'] = Nickname[0]
        if gender:
            infoItem['Gender'] = gender[0]
        if birth:
            infoItem['Birthday'] = birth[0]
        if Signature:
            infoItem['Signature'] = Signature[0]
        if len(addr) == 2:
            infoItem['Province'] = addr[0]
            infoItem['City'] = addr[1]
        if len(addr) == 1:
            infoItem['Province'] = addr[0]
            infoItem['City'] = addr[0]
        if Home_url:
            infoItem['Home_url'] = Home_url[0]
        yield infoItem


    def parse_weibo(self, response):
        """微博内容
         _id = Field()
    User_id = Field()
    Content = Field()
    Pubtime = Field()
    Pubaddr = Field()
    Tool = Field()
    Like = Field()
    Comment = Field()
    Transfer = Field()
        """
        weiboItem = WeiboItem()
        weiboItem['User_id'] = response.meta['ID']
        contents = response.xpath('//div[@class="c" and @id]')
        print('爬取微博内容！！！！！！！！！！！！')
        if len(contents) == 0:
            print('没有更多微博了')
            raise StopIteration

        print('Contents:%d' % len(contents))
        for item in contents:
            id = item.xpath('@id').extract_first()
            content = item.xpath('div/span[@class="ctt"]/text()').extract_first()
            text = item.extract()
            like = re.findall(r'赞\[(\d+)\]</a>', string=text)
            comment = re.findall(r'>评论\[(\d+)\]</a>', string=text)
            transfer = re.findall(r'转发\[(\d+)\]</a>', string=text)
            time_tool = re.findall(r'class="ct">(.*?)来自(.*?)</span>',string=text)
            tool = time_tool[0][1]
            if '今天' in time_tool[0][0]:
                time = datetime.now().strftime('%M月%d日') + time_tool[0][0][2:-1]
            else:
                time = time_tool[0][0][:-1]
            weiboItem['_id'] = response.meta['ID'] + '_' + id
            weiboItem['Content'] = content
            weiboItem['Like'] = like[0]
            weiboItem['Comment'] = comment[0]
            weiboItem['Transfer'] = transfer[0]
            weiboItem['Tool'] = tool
            weiboItem['Pubtime'] = time
            print('打印单条微博信息！！！！！！！！！！！！！！！！')
            yield weiboItem
        n = response.meta['n']
        if not response.meta['n']:
            n = 2
        if n <= 5:
            yield Request(url=self.host + '/' + response.meta['ID']+"/profile?page=%d" % n,
                      meta={'ID': response.meta['ID'],
                            'n':n+1
                            }, callback=self.parse_weibo)

    def parse_follow_or_fans(self, response):
        """"/html/body/table[1]
            _id = Field()
        follows = Field()
        """
        target_List = response.meta['list']
        target_Item = response.meta['Item']
        results = response.xpath('//table')
        for item in results:
            # 某位用户的id
            target_id = item.xpath('tr/td[1]/a/@href').extract_first().split('/')[-1]
            target_List.append(target_id)

        text = response.xpath('//div[@id="pagelist"]').extract()[0]

        next_url = re.findall(r'<a href="(.+?)">下页</a>', text)

        if response.meta['n']:
            n = response.meta['n']
        if n >= 5:
            if isinstance(target_Item,FollowsItem):
                target_Item['follows'] = target_List
                yield target_Item

            if isinstance(target_Item,FansItem):
                target_Item['fans'] = target_List
                yield target_Item


        if len(next_url) != 0 and n < 5:

            yield Request(url=self.host+next_url[0], meta={'Item': target_Item, 'list': target_List, 'n':n+1},
                          callback=self.parse_follow_or_fans)
        # else:
        #     if isinstance(target_Item,FollowsItem):
        #         target_Item['follows'] = target_List
        #         yield target_Item
        #
        #     if isinstance(target_Item,FansItem):
        #         target_Item['fans'] = target_List
        #         yield target_Item
























