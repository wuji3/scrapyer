# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy

class ImagePipeline(ImagesPipeline):
    """
    ImagePipeline逻辑
        get_media_requests接收spider刚刚yield出来的item 拿到url return这个url的request
        ImagesPipeline内部会对request有解析、下载等动作 若对下载路径有需求 需要通过file_path写好路径 ImagesPipeline内部会调
        下载完成(或失败) 内部会把results通过item_completed传过来 若有需求可以在这个函数内改

        一共只需要重写的方法有
            def get_media_requests(self, item, info):
            def file_path(self, request, response=None, info=None, *, item=None):
            def item_completed(self, results, item, info):
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_media_requests(self, item, info):
        return scrapy.Request(url=item['img_url'])

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'crawled_images/{item["img_name"]}.jpg'

    def item_completed(self, results, item, info):
        """
        每个item下好会调用这个方法 results存以下变量
        Arguments:
            result: (success, file_info_or_error)
                success: bool
                file_info_or_error: dict
                    url
                    path
                    checksum
                    status: It can be one of [downloaded, uptodate, cached]
            eg:
            (
                True, <- success
                {
                    "checksum": "2b00042f7481c7b056c4b410d28f33cf",
                    "path": "full/0a79c461a4062ac383dc4fade7bc09f1384a3910.jpg",            <- file_info_or_error
                    "url": "http://www.example.com/files/product1.pdf",
                    "status": "downloaded",
                },
            ),
        """
        #-------------------------------------------若有缩放图像的需求----------------------------------------------------#
        # import os
        # from PIL import Image
        # # xxx 即图像文件夹存储文件夹 即scrapy crawl spider -s IMAGES_STORE=xxx
        # img_path = os.path.join('xxx', results[0][1]['path'])
        # if os.path.isfile(img_path):
        #     image = Image.open(img_path).convert('RGB')
        #     image = image.resize(size=(1280, 1280), resample=1)
        #     image.save(img_path)
        #--------------------------------------------------------------------------------------------------------------#

        # 没特殊需求时 用默认的方法就可以
        return super().item_completed(results, item, info)