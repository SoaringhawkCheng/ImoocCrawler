# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
import urlparse
from crawler.items import JobBoleArticleItem
class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
            1.获取文章列表页中的所有文章url并交给SCRAPY处理
            2.获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        """
        #解析列表页中所有的文章url
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url = urlparse.urljoin(response.url,post_url),meta = {"front_image_url":image_url}, callback=self.parse_detail)
        next_urls =  response.css(".next.page-numbers::attr(href)").extract_first()
        if next_urls:
            yield Request(url = urlparse.urljoin(response.url,post_url),callback=self.parse)
    def parse_detail(self,response):
        #提取文章的具体字段
        article_item = JobBoleArticleItem()
        titlestr = response.css(".entry-header h1::text").extract()[0]
        create_date = response.css(".entry-meta-hide-on-mobile::text").extract()[0].strip().replace(u'·'," ").strip()
        praise_nums = response.css(".vote-post-up h10::text").extract()[0]
        fav_nums = response.css(".bookmark-btn::text").extract()[0]
        match_re = re.match(".*(\d+).*",fav_nums)
        front_image_url = response.meta.get("front_image_url","") #文章封面图
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0
        comment_nums =response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(".*(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        content = response.css("div.entry").extract()[0]
        tags = response.css(".entry-meta-hide-on-mobile a::text").extract()[0]
        article_item["title"] = titlestr
        article_item["url"]   = response.url
        article_item["create_date"] = create_date
        article_item["front_image_url"] = [front_image_url]
        article_item["praise_nums"] = praise_nums
        article_item["comment_nums"] = comment_nums
        article_item["fav_nums"] = fav_nums
        article_item["tags"] = tags
        article_item["content"] = content
        yield article_item
        pass
