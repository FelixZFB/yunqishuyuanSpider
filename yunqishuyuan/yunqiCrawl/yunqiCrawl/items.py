# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YunqicrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class YunqiBookListItem(scrapy.Item):
    # 小说ID
    novelId = scrapy.Field()
    # 小说名称
    novelName = scrapy.Field()
    # 小说连接
    novelLink = scrapy.Field()
    # 小说作者
    novelAuthor = scrapy.Field()
    # 小说类型
    novelType = scrapy.Field()
    # 小说状态
    novelStatus = scrapy.Field()
    # 小说更新时间
    novelUpdateTime = scrapy.Field()
    # 小说字数
    novelWords = scrapy.Field()
    # 小说封面
    novelImageUrl = scrapy.Field()

class YunqiBookDetailItem(scrapy.Item):
    # 小说ID
    novelId = scrapy.Field()
    # 小说标签
    novelLabel = scrapy.Field()
    # 小说总点击量
    novelAllClick = scrapy.Field()
    # 月点击量
    novelMonthClick = scrapy.Field()
    # 周点击量
    novelWeekClick = scrapy.Field()
    # 总人气
    novelAllPopular = scrapy.Field()
    # 月人气
    novelMonthPopular = scrapy.Field()
    # 周人气
    novelWeekPopular = scrapy.Field()
    # 评论数
    novelCommentNum = scrapy.Field()
    # 小说总推荐
    novelAllComm = scrapy.Field()
    # 小说月推荐
    novelMonthComm = scrapy.Field()
    # 小说周推荐
    novelWeekComm = scrapy.Field()

