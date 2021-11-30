import scrapy


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://irkutsk.hh.ru/search/vacancy?schedule=remote&search_field=name&search_field=company_name&search_field=description&experience=between1And3&fromSearchLine=true&text=Python&from=suggest_post&items_on_page=20',
    ]

    def parse(self, response):
        pass
