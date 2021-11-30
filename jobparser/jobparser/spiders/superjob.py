import scrapy


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = [
        'https://www.superjob.ru/vacancy/search/?keywords=Python&remote_work_binary=2&noGeo=1&click_from=facet'
    ]

    def parse(self, response):
        pass
