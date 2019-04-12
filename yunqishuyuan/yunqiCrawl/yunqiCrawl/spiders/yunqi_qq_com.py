# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from yunqiCrawl.items import YunqiBookListItem
from yunqiCrawl.items import YunqiBookDetailItem


class YunqiQqComSpider(CrawlSpider):
    name = 'yunqi.qq.com.Spider'
    allowed_domains = ['yunqi.qq.com']
    # 先查看书库：http://yunqi.qq.com/bk，然后向后面点几页，发现网址就是p后面的页码不同
    start_urls = ['http://yunqi.qq.com/bk/so2/n30p1']

    # 将书库网址规律加入到规则中，会自动爬取满足规律的所有网址，每个网址都调用parse_book_list方法进行解析
    rules = (
        Rule(LinkExtractor(allow=r'/bk/so2/n30p\d+'), callback='parse_book_list', follow=True),
    )

    def parse_book_list(self, response):
        # 详细解析参考ch00知识补充-网页解析-yunqishuyuan1_Spider.py
        # 下面的两种方法选取的结果一样
        # .从根节点开始选取，//不管在什么位置，div的class属性为book的所有div标签
        # books = response.xpath(".//div[@class='book']")
        # .从根节点开始选取，//不管在什么位置，*代表所有的class属性为book的所有标签
        # books = response.xpath(".//*[@class='book']")
        books = response.xpath(".//div[@class='book']")

        for book in books:

            novelImageUrl = book.xpath("./a/img/@src").extract_first()
            novelId = book.xpath("./div[@class='book_info']/h3/a/@id").extract_first()
            novelName = book.xpath("./div[@class='book_info']/h3/a/text()").extract_first()
            novelLink = book.xpath("./div[@class='book_info']/h3/a/@href").extract_first()
            # 注意网页中是dl标签（不是d1）,注意区分l和1
            # novelAuthor = book.xpath("./div[@class='book_info']/dl[1]/dd[1]/a/text()").extract_first()
            # 有些书籍的作者，状态信息等信息为空的，因此该处尝试使用if语句，信息都全的话，才提取信息
            # 下面两种方法的结果一样
            # novelInfos = book.xpath("./div[@class='book_info']//dl//dd[@class='w_auth']")
            novelInfos = book.xpath("./div[@class='book_info']/dl/dd[@class='w_auth']")

            if len(novelInfos) > 4:
                novelAuthor = novelInfos[0].xpath("./a/text()").extract_first()
                novelType = novelInfos[1].xpath("./a/text()").extract_first()
                novelStatus = novelInfos[2].xpath("./text()").extract_first()
                novelUpdateTime = novelInfos[3].xpath("./text()").extract_first()
                novelWords = novelInfos[4].xpath("./text()").extract_first()
            else:
                novelAuthor = ''
                novelType = ''
                novelStatus = ''
                novelUpdateTime = ''
                novelWords = 0
            bookListItem = YunqiBookListItem(
                novelId=novelId, novelName=novelName,
                novelLink=novelLink, novelAuthor=novelAuthor,
                novelType=novelType, novelStatus=novelStatus,
                novelUpdateTime=novelUpdateTime,
                novelWords=novelWords,
                novelImageUrl=novelImageUrl,
            )
            # 生成bookListItem，用于存放书单中每一本书的信息
            yield bookListItem

            # 进入一本书，解析一本书的详细信息
            request = scrapy.Request(url=novelLink, meta={'novelId': novelId}, callback=self.parse_book_detail)
            yield request

    def parse_book_detail(self, response):
        # 解析一本书的详细信息，参考ch00知识补充-网页解析-yunqishuyuan2_Spider.py
        novelId = response.meta['novelId']
        # .从根节点开始选取，//不管在什么位置，div的class属性为book的所有div标签
        novelLabel = response.xpath(".//div[@class='tags']/text()").extract_first()

        novelAllClick = response.xpath(".//div[@id='novelInfo']/table/tr[2]/td[1]/text()").extract_first()
        novelAllPopular = response.xpath(".//div[@id='novelInfo']/table/tr[2]/td[2]/text()").extract_first()
        novelAllComm = response.xpath(".//div[@id='novelInfo']/table/tr[2]/td[3]/text()").extract_first()

        novelMonthClick = response.xpath(".//div[@id='novelInfo']/table/tr[3]/td[1]/text()").extract_first()
        novelMonthPopular = response.xpath(".//div[@id='novelInfo']/table/tr[3]/td[2]/text()").extract_first()
        novelMonthComm = response.xpath(".//div[@id='novelInfo']/table/tr[3]/td[3]/text()").extract_first()

        novelWeekClick = response.xpath(".//div[@id='novelInfo']/table/tr[4]/td[1]/text()").extract_first()
        novelWeekPopular = response.xpath(".//div[@id='novelInfo']/table/tr[4]/td[2]/text()").extract_first()
        novelWeekComm = response.xpath(".//div[@id='novelInfo']/table/tr[4]/td[3]/text()").extract_first()

        novelCommentNum = response.xpath(".//*[@id='novelInfo_commentCount']/text()").extract_first()

        bookDetailItem = YunqiBookDetailItem(
            novelId=novelId, novelLabel=novelLabel,
            novelAllClick=novelAllClick, novelAllPopular=novelAllPopular,
            novelAllComm=novelAllComm, novelMonthClick=novelMonthClick,
            novelMonthPopular=novelMonthPopular, novelMonthComm=novelMonthComm,
            novelWeekClick=novelWeekClick, novelWeekPopular=novelWeekPopular,
            novelWeekComm=novelWeekComm, novelCommentNum=novelCommentNum,
        )
        yield bookDetailItem

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('yunqi.qq.com.Spider')
    process.start()





