# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HnScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class HnArticleItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    id = scrapy.Field()
    author = scrapy.Field()
    pass

class SeedItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    language = scrapy.Field()
    response_code = scrapy.Field()
    num_links = scrapy.Field()
    domain = scrapy.Field()
    query_path = scrapy.Field()
    score = scrapy.Field()
    pass