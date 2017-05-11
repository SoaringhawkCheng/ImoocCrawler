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

