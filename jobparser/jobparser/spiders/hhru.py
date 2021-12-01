import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


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
        """
        Пересмотрел урок несколько раз 5 и всё равно не могу понять этот момент.
        Не теряем ли мы здесь первую страницу с вакансиями.
        Почему мы не делаем так:
        links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.job_parse)
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        Можно прокомментировать прямо здесь в пулле.
        """

    def job_parse(self, response: HtmlResponse):
        print()
        name = response.xpath('//h1//text()').get()
        salary = response.xpath('//div[@class="vacancy-salary"]//text()').getall()
        job_link = response.url

        JobparserItem(name=name, salary=salary, job_link=job_link)

