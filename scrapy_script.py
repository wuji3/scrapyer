#---------------------------该脚本通过python启动爬虫-------------------------#

"""
文件树:
--project
    --scrapyer
        --common
        --scrapy_script.py <++++++++
        --scrapy.cfg
        --xpath.txt
        --README.md
    --xxx
    --xxx
scrapy作为一个module放在project里 project路径下的脚本导入ScrapyDownloader类使用
"""

#--------------------若作为module, 则添加环境变量----------------------#
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
#-------------------------------------------------------------------#
from typing import Union
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import SettingsAttribute
from common.spiders.csvSpider import CSVSpider

#-------若作为module, 则设置scrapy的环境变量 让scrapy读到自己的settings-------#
os.environ['SCRAPY_SETTINGS_MODULE'] = 'scrapyer.common.settings'
#-----------------------------------------------------------------------#

class ScrapyDownloader:
    def __init__(self, image_src: str, spider: Union[Spider, str], logtxt: str): # CSVSpider / "csvspider"
        self.image_src = image_src

        setting = get_project_settings()
        setting.attributes['IMAGES_STORE'] = SettingsAttribute(image_src, 300)
        setting.attributes['LOG_FILE'] = SettingsAttribute(logtxt, 300)

        process = CrawlerProcess(setting)

        # init spider
        process.crawl(spider)

        self.process = process

    def crawl(self):
        self.process.start()

if __name__ == '__main__':
    # # read setting
    # setting = get_project_settings()
    # setting.attributes['IMAGES_STORE'] = SettingsAttribute('/home/xxx/xxx/{date}/images'.format(date = datetime.datetime.now().strftime("%Y-%m-%d")), 300)
    # # init project
    # process = CrawlerProcess(setting)
    # # init spider
    # process.crawl(CSVSpider)
    # # do crawl
    # process.start()

    from setting import Setting
    spider = ScrapyDownloader(Setting.images_dir)
    spider.crawl()