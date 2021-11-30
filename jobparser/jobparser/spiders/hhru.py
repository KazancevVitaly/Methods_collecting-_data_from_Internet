import scrapy


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://irkutsk.hh.ru/search/vacancy?schedule=remote&search_field=name&search_field=company_name&search_field=description&fromSearchLine=true&text=Python'
    ]

    def parse(self, response):
        pass
