#---------------------------该脚本通过python启动爬虫-------------------------#

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import SettingsAttribute
from common.spiders.csvSpider import CSVSpider

# read setting
setting = get_project_settings()
setting.attributes['IMAGES_STORE'] = SettingsAttribute('images', 300)
# init project
process = CrawlerProcess(setting)
# init spider
process.crawl(CSVSpider)
# do crawl
process.start()