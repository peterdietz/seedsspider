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
    declared_language = scrapy.Field()
    detected_language = scrapy.Field()
    response_code = scrapy.Field()
    num_links = scrapy.Field()
    response_type = scrapy.Field()
    num_words = scrapy.Field()
    fk_grade = scrapy.Field()
    pass