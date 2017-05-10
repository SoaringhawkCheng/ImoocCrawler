# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

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


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('172.29.103.5','root','cetc315B01','Jobbole_db',charset="utf8",use_unicode=True)
        self.cursor = self.conn.cursor()
    def process_item(self,item,spider):
        insert_sql = """
        insert into jobbole_info(title, create_date, url, url_object_id, front_image_url, comment_nums, fav_nums, praise_nums, tags, content,front_image_path)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item["title"],item["create_date"],item["url"],item["url_object_id"],item["front_image_url"],item["comment_nums"],item["fav_nums"],item["praise_nums"],item["tags"],item["content"],item["front_image_path"]))
        self.conn.commit()
class MysqlTwistedPipline(object):
        def __init__(self,dbpool):
            self.dbpool = dbpool
        @classmethod
        def from_settings(cls,settings):
           dbparms = dict(
                host = settings["MYSQL_HOST"],
                db = settings["MYSQL_DBNAME"],
                user = settings["MYSQL_USER"],
                passwd = settings["MYSQL_PASSWORD"],
                charset = 'utf8',
                cursorclass = MySQLdb.cursors.DictCursor,
                use_unicode = True
            )
           dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)
           return cls(dbpool)
        def process_item(self,item,spider):
            #使用twisted将MYSQL插入编程异步执行
            query = self.dbpool.runInteraction(self.do_insert,item,)
            query.addErrback(self.handle_error,item,spider)#处理异常
        def handle_error(self,failure,item,spider):
            print failure #处理异步插入的异常
        def do_insert(self,cursor,item):
            #执行具体的插入
            insert_sql = """
            insert into jobbole_info(title, create_date, url, url_object_id, front_image_url, comment_nums, fav_nums, praise_nums, tags, content,front_image_path)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            cursor.execute(insert_sql, (
            item["title"], item["create_date"], item["url"], item["url_object_id"], item["front_image_url"],
            item["comment_nums"], item["fav_nums"], item["praise_nums"], item["tags"], item["content"],
            item["front_image_path"]))