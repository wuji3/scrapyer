import scrapy
from colorHub.items import ColorhubItem

"""
这个爬虫->读本地csv->包装成item再yield给ImagesPipeline下载图片
"""

class CSVSpider(scrapy.Spider):
    # download form xxx.cvs
    name = 'csvspider'

    csv = 'output.csv'

    def __init__(self):
        super().__init__()
        import pandas as pd
        self.df = pd.read_csv(CSVSpider.csv)

    def start_requests(self):
        # 随便请求一个url反正也不用 回调函数处理csv csv里的内容包装成item吐给pipeline下载就可以了
        for _ in range(1): yield scrapy.Request('https://www.colorhub.me', callback=self.parse)

    def parse(self, response, **kwargs):
        for idx in range(self.df.shape[0]):
            item = ColorhubItem()
            item['img_name'] = self.df.loc[idx, 'img_name']
            item['img_url'] = self.df.loc[idx, 'img_url']
            yield item