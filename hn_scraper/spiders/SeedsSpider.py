# -*- coding: utf-8 -*-
import scrapy
import lxml

from scrapy.spiders import Spider
from scrapy import signals
from hn_scraper.items import SeedItem
from polyglot.detect import Detector
from bs4 import BeautifulSoup
from urlparse import urlparse

class SeedsSpider(Spider):
    name = "SeedsSpider"
    allowed_domains = ["wikipedia.org"]

    def __init__(self):
        ## In VC:  java -jar impl/task/lambda/target/vericite-task.jar seedslist /opt/seeds.txt
        import os
        print os.getcwd()
        seedsfile = os.getcwd()+"/seeds.txt"
        with open(seedsfile, 'r') as f:
            #self.start_urls = f.read(10)
            # self.start_urls = f.readlines()
            self.start_urls = f.read().splitlines()

        ##subset
        self.start_urls = self.start_urls[0:10]
        print "STARTING URLS:"
        print self.start_urls

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(SeedsSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.item_dropped, signal=signals.item_dropped)
        crawler.signals.connect(spider.request_dropped, signal=signals.request_dropped)
        return spider

    def item_dropped(self, item, response, exception, spider):
        spider.logger.info('Spider item dropped: ' + str(item) + ' - ' + response.url)

    def request_dropped(self, request, spider):
        spider.logger.info('request_dropped: ' + request.url)


    def extract_one(self, selector, xpath, default=None):
        extracted = selector.xpath(xpath).extract()
        if extracted:
            return extracted[0]
        return default

    def parse(self, response):
        response_type = type(response)

        if response_type is scrapy.http.HtmlResponse:
            for item in self.parse_HtmlResponse(response):
                yield item
        elif response_type is scrapy.http.XmlResponse:
            for item in self.parse_XmlResponse(response):
                yield item
        elif response_type is scrapy.http.TextResponse:
            #TODO text
            for item in self.parse_Response(response):
                yield item
        else:
            for item in self.parse_Response(response):
                yield item

    ## non-text, binary/PDF
    def parse_Response(self, response):
        print "NotImplemented Binary response:" + response.url

        item = SeedItem()
        item['url'] = response.url
        item['response_code'] = response.status
        item['title'] = "NotImplementedBinary"
        #item['num_links'] = -1
        #item['language']
        #item['docType']
        yield item

    # text, xml/rdf
    def parse_XmlResponse(self, response):
        print "NotImplemented xml response:" + response.url

        item = SeedItem()
        item['url'] = response.url
        item['response_code'] = response.status
        item['title'] = "NotImplementedXML"
        yield item

    def parse_HtmlResponse(self, response):
        item = SeedItem()
        item['url'] = response.url
        item['response_code'] = response.status

        soup = BeautifulSoup(response.text, "lxml")
        title = "NoTitle"
        if soup.find('title'):
            title = soup.find('title').string
        item['title'] = title

        lang = "unknown"
        if soup.html.has_attr('lang'):
            lang = soup.html['lang']
        else:
            stripped_text = lxml.html.fromstring(response.body).text_content()
            Detector(stripped_text, True)
            language = Detector(stripped_text)

            if language.reliable:
                lang = language.language.code
                print "detected language: " + language.language.code + " confidence:" + language.language.confidence
        item['language'] = lang

        #accepted_languages = {'en'}
        # lang could be en-US
        #language_code = lang.split('-')[0]
        # Only care about processing EN documents
        #if language_code not in accepted_languages:
        #    print "Passing, we don't accept language: " + lang
        #    pass

        item['domain'] = urlparse(response.url).hostname
        item['query_path'] = urlparse(response.url).query
        score = 0
        accepted_language = {'en'}
        if lang.split('-')[0] in accepted_language:
            score = 1
        item['score'] = score


        num_links = 0
        for href in response.css('a::attr(href)').extract():
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse
            )
            num_links += 1
        item['num_links'] = num_links

        yield item
