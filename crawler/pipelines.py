# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter

class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class AritcleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            image_file_path = value["path"]
        item["front_image_path"] = image_file_path
        return item


class JSonWithEncodingPipeline(object):
    #自定义Json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding="utf-8") #打开json文件
    def process_item(self,item,spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()


class JsonExportPipleline(object):
    def __init__(self):
        #调用scrapy提供的json export导出json文件
        self.file = open('articleexprot.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding="utf-8",ensure_ascii=False)
        self.exporter.start_exporting()
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

