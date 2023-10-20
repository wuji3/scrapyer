# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

"""
继承scrapy.Item 注册class.attr 然后在spider中yield出去 属性名要一一对应
"""
class CommonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    img_name: str = scrapy.Field()
    img_url: str = scrapy.Field()