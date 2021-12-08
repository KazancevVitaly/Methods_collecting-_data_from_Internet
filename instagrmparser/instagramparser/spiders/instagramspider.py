import scrapy
from scrapy.http.response.html import HtmlResponse
import json


class InstagramspiderSpider(scrapy.Spider):
    name = 'instagramspider'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']

    def parse(self, response: HtmlResponse):
        pass
