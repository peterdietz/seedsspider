# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import scrapy

from hn_scraper.items import SeedItem
from polyglot.detect import Detector
from bs4 import BeautifulSoup
from language_train import LanguageTrain


class SeedsSpider(RedisSpider):
    name = "SeedsSpider"
    #allowed_domains = ["wikipedia.org", 'twitter.com']
    language_train = None

    def __init__(self):
        #
        #seedsfile = os.getcwd()+"/seeds.txt"
        #with open(seedsfile, 'r') as f:
        #    self.start_urls = f.read().splitlines()
        #
        #self.start_urls = self.start_urls[0:10]
        #
        #print "STARTING URLS:"
        #print self.start_urls
        #self.start_urls = ['https://www.x.com']
        self.language_train = LanguageTrain()

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

    # non-text, binary/PDF
    def parse_Response(self, response):
        print "NotImplemented Binary response:" + response.url

        item = SeedItem()
        item['url'] = response.url
        item['response_code'] = response.status
        item['response_type'] = "Binary"
        yield item

    # text, xml/rdf
    def parse_XmlResponse(self, response):
        print "NotImplemented xml response:" + response.url

        item = SeedItem()
        item['url'] = response.url
        item['response_code'] = response.status
        item['response_type'] = "XML"
        yield item

    def parse_HtmlResponse(self, response):
        item = SeedItem()
        item['url'] = response.url
        item['response_code'] = response.status
        item['response_type'] = 'HTML'

        soup = BeautifulSoup(response.body, "lxml")
        if soup.html.has_attr('lang'):
            lang = soup.html['lang']
            item['declared_language'] = lang

        stripped_text = soup.get_text()
        Detector(stripped_text, True)
        language = Detector(stripped_text)

        if language.reliable:
            lang = language.language.code
            #print "detected language: " + language.language.code + " confidence:" + str(language.language.confidence)
            item['detected_language'] = lang

        num_links = 0
        for href in response.css('a::attr(href)').extract():
            url = response.urljoin(href)
            if self.language_train.is_url_predicted_in_accepted_lang(url):
                #print "link is predicted to be acceptable, keeping: " + url
                yield scrapy.Request(
                    url=response.urljoin(href),
                    callback=self.parse
                )
            else:
                print "Skipping url because of predicted language:" + url
            num_links += 1
        item['num_links'] = num_links

        yield item
