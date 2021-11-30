import scrapy
from scrapy.http import HtmlResponse


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://irkutsk.hh.ru/search/vacancy?schedule=remote&search_field=name&search_field=company_name&search_field=description&fromSearchLine=true&text=Python'
    ]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.job_parse)

    def job_parse(self, response: HtmlResponse):
        print()
