import scrapy
from colorHub.items import ColorhubItem

"""
    这个爬虫->只爬文本->输出csv

    module.__name__和class.__name__都不重要
    重要的是class.name 通过命令行启动时 scrapy crawl xxx 其中xxx指的是class.name
    
    site-packages\scrapy\spiderloader.py SpiderLoader会根据setting里填写的SPIDER_MODULES在内存里刷一遍
    找到所有继承了Spider的class 再匹配class.name
"""
class URLSpider(scrapy.Spider):
    name = 'textspider'

    #-----默认爬colorhub tag即类型 pages即爬多少页----#
    tag = '兔子'
    pages = 2
    #---------------------------------------------#

    def start_requests(self):
        # 返回的是scrapy.Request对象
        for page in range(1, URLSpider.pages+1):
            yield scrapy.Request(url = f'https://www.colorhub.me/search?tag={URLSpider.tag}&page={str(page)}',
                                 callback=self.parse)

    def parse(self, response, **kwargs):
        # response的类型是<class 'scrapy.http.response.html.HtmlResponse'> 继承的是scrapy.http.response.Response
        # 这里有个坑 chrome在检查时会优化代码 不是网页源码 因此在网页可以抓到的可能是经过浏览器修改过的 若出现抓不到的情况 看网页源码
        for item_block in response.xpath('//div[@class="loader"]/img[@class="card-img-top invisible lazy"]'):
            item = ColorhubItem()
            # scrapy.Item的__setattr__只允许单下划线_开头的属性调用 其余属性只能通过__setitem__调用
            item['img_name'] = item_block.xpath('./@title').get()
            item['img_url'] = 'https:' + item_block.xpath('./@data-src').get()
            yield item

            # 直接yield字典出去也是可以的 item-style也包括字典
            # yield {
            #     'img_name': item_block.xpath('./@title').get(),
            #     'img_url': 'https:' + item_block.xpath('./@data-src').get()
            # }