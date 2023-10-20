## install  
conda create -n scrapy python=3.9  
conda activate scrapy  
conda install -c conda-forge scrapy  
conda install pandas  
conda install Pillow # 确保pillow >= 4.0.0 不然不会启动ImagePipeline

## tips
_csvspider_ 爬图只需要关注spiders、items、pipelines和settings  
>注意： spider中url是否正确？pipeline请求的url是否正确？(若设置)图像名称是否正确？setting是否设置pipeline？

## coding
1. spiders⭐⭐⭐
```
```python
class XXX(scrapy.Spider):
    name = 'xxx' # 爬虫的名字 与启动时保持一致

    def start_requests(self):
        ...
        return scrapy.Request(url=..., callback=self.parse)
    
    def parse(self, response, **kwargs) -> scrapy.Item:
        ...
        return xxx_item
```
2. items
```python
class XXX(scrapy.Item) -> None:
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
```
3. pipelines[若只爬文字输出csv/json, 可省略]⭐⭐⭐
```python
class XXXPipeline:
    def __init__(self):
        pass
    
    # hook before spider open
    def open_spider(self, spider):
        pass
    
    # hook after spider close
    def close_spider(self, spider):
        pass
    
    # 核心方法
    def process_item(self, item, spider):
        return item

# 针对图像爬虫 继承ImagesPipeline
class ImagePipeline(ImagesPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_media_requests(self, item, info):
        return scrapy.Request(url=item['img_url'])

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'crawled_images/{item["img_name"]}.jpg'

    def item_completed(self, results, item, info):
        # 没特殊需求时 用默认的方法就可以
        return super().item_completed(results, item, info)
```
4.  middlewares[若无拦截需求，可省略]
```python
class XXXDownloaderMiddleware: # 下载中间件 一般改写它会比较多 还有一个爬虫中间件XXXSpiderMiddleware
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
    
    # 拦截请求
    def process_request(self, request, spider):
        request.cookies = ... # 加cookies
        request.meta = {'proxy': '...'} # 加代理
        return None
    
    # 拦截响应
    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
```
5.  setting⭐⭐⭐
```python
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
   "Accept-Language": "en",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
ROBOTSTXT_OBEY=False
CONCURRENT_REQUESTS = 32 # 配置好的话可以设高点 default=16

# 仅爬文字 不需要设置ITEM_PIPELINES和DOWNLOADER_MIDDLEWARES
# 请求 数字越小优先级越高 响应 数字越大优先级越高

ITEM_PIPELINES = {
   "colorHub.pipelines.ImagePipeline": 300, 
} 
DOWNLOADER_MIDDLEWARES = {
   "colorHub.middlewares.ColorhubDownloaderMiddleware": 543,
}
# 图像保存路径
IMAGES_STORE = "crawled_images"
```

## scrapy-frame conclusion
_spider_ -> spider的start_request把请求yield出去 拿到response交给callback[也就是parse这个方法]解析 解析好了打包成item yield给pipeline  
_pipeline_ -> pipeline在spider启动前和启动后都有对应的hook可以做点事情 核心函数是process_item  处理spider解析好的item  
_middleware_ -> spider中间件和download中间件 download中间件用于请求拦截[process_request]和响应拦截[response_request] 比如请求拦截可以用于伪装请求 加代理或加cookie  

## run
```shell
scrapy crawl xxx -o xxx.csv/xxx.json
# 若不在setting里设置图像保存目录 也可以通过命令传送 -s表setting
# -s IMAGES_STORE=crawled_images 不需要先手动创建文件夹 若不存在会自动创建
scrapy crawl csvspider -s IMAGES_STORE=crawled_images 
```

## log
出现问题时 把log打出来
```shell
scrapy crawl XXXspider -s LOG_LEVEL=DEBUG -s LOG_FILE=log.txt
```

## performance
CONCURRENT_REQUESTS = 32, 下载 4965 张图( 3.83G | 2MB / Image ), 耗时 658 seconds
CONCURRENT_REQUESTS = 32, 下载 239w 张图( 131.0G | 0.1MB / Image ), 耗时 47949 seconds

## reference
https://docs.scrapy.org/en/latest/
