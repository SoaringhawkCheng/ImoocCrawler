# -*- coding: utf-8 -*-
import scrapy
import re

class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/111016/']

    def parse(self, response):
        """
        #通过CSS选择器提取字段
        :param response: 
        :return: 
        """
        titlestr = response.css(".entry-header h1::text").extract()[0]
        create_date = response.css(".entry-meta-hide-on-mobile::text").extract()[0].strip()
        praise_nums = response.css(".vote-post-up h10::text").extract()[0]
        fav_nums = response.css(".bookmark-btn::text").extract()[0]
        match_re = re.match(".*(\d+).*",fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        comment_nums =response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(".*(\d+).*", comment_nums)
        if match_re:
            comment_nums = match_re.group(1)
        content = response.css("div.entry").extract()[0]
        tags = response.css(".entry-meta-hide-on-mobile a::text").extract()[0]
        pass
