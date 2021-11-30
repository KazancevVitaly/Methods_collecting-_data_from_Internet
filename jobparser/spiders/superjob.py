import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = [
        'https://russia.superjob.ru/vacancy/search/?keywords=python&click_from=facet'
    ]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[contains(@data-qa, "pager-next")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@target="_blank"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1//text()').getall()
        salary = response.xpath('//span[@class="_1OuF_ ZON4b"]//text()').getall()
        url = response.url

        yield JobparserItem(name=name, salary=salary, url=url)


