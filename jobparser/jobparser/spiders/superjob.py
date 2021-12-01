import scrapy
from scrapy.http import HtmlResponse

class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = [
        'https://www.superjob.ru/vacancy/search/?keywords=python&remote_work_binary=2&noGeo=1&click_from=facet'
    ]

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[contains(@class, "icMQ_ _6AfZ9")]/@href').getall()
        for link in links:
            # link = f'https://www.superjob.ru{link}'
            yield response.follow(link, callback=self.job_parse)
        next_page = response.xpath('//a[contains(@class, "f-test-link-Dalshe")]/@href').get()
        # next_page = f'https://www.superjob.ru{next_page}'
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def job_parse(self, response: HtmlResponse):
        print()
        name = response.xpath('//h1/text()').get()
        salary = response.xpath('//span[@class="_2Wp8I _1e6dO _1XzYb _3Jn4o"]/text()').getall()
        job_link = response.url

