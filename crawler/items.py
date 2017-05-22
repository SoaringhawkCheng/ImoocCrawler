# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import datetime
import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst,Join
from scrapy.loader import ItemLoader
import re
from w3lib.html import remove_tags
from settings import SQL_DATETIME_FORMAT,SQL_DATE_FORMAT


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobble(value):
    return value + "-jobbole"


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value,"%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def get_nums(value):
    match_re = re.match(".*(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


# def remove_comment_tags(value):
#     if("评论" in value):
#         return ""
#     else:
#         value

def return_value(value):
    return value


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        input_processor = MapCompose(add_jobble)
    )
    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert),

    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor = MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor = MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor =MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor = MapCompose(get_nums)
    )
    tags = scrapy.Field(
       # input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    content = scrapy.Field()


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def remove_splash(value):
    #去掉城市的斜线
    return value.replace("/","")


# def handle_jobaddr(value):
#     addr_list = value.split("\\n")
#     addr_list = [item.strip() for item in addr_list if item.strip() != u'查看地图']
#     return "".join(addr_list)


class LagouJobItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class LagouJobItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    work_years = scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field(
        input_processor = Join(",")
    )
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO lagou_job(url, url_object_id, salary, job_city, work_years, degree_need, job_type, publish_time, tags, job_advantage, job_desc, company_url, company_name, crawl_time )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
          
        """
        params = (
            self["url"], self["url_object_id"], self["salary"],
            self["job_city"], self["work_years"], self["degree_need"],
            self["job_type"], self["publish_time"], self["tags"],
            self["job_advantage"],  self["job_desc"], self["company_url"],
            self["company_name"], self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )
        return insert_sql, params
