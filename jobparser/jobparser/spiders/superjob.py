import scrapy
from scrapy.http import HtmlResponse

class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = [
        'https://www.superjob.ru/vacancy/search/?keywords=Python&remote_work_binary=2&noGeo=1&click_from=facet'
    ]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[contains(@class, "f-test-link-Dalshe")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@target="_blank"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.job_parse())

    def job_parse(self, response: HtmlResponse):
        print()
