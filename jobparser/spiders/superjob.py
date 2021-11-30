import scrapy


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = [
        'https://www.superjob.ru/vacancy/search/?keywords=python&remote_work_binary=2&geo%5Br%5D%5B0%5D=3',
        'https://www.superjob.ru/vacancy/search/?keywords=python&remote_work_binary=2&geo%5Br%5D%5B0%5D=7'
    ]

    def parse(self, response):
        pass
