import scrapy
from scrapy.http.response.html import HtmlResponse
from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = [
        'https://www.labirint.ru/search/python/?stype=0',
        'https://www.labirint.ru/search/English/?stype=0',
        'https://www.labirint.ru/search/Charlotte%20Bronte/?stype=0'
    ]

    def parse(self, response: HtmlResponse):
        print()
        next_page = response.xpath('//a[@class="pagination-next__text"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@class="product-title-link"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.book_parser)

    def book_parser(self, response: HtmlResponse):
        print()
        book_link = response.url
        name = response.xpath('//h1/text()').get()
        authors = response.xpath('//div[@class="authors"][1]//text()').getall()
        price = response.xpath('//span[contains(@class, "buying-price")]//text()').getall()
        rate = response.xpath('//div[@id="rate"]/text()').get()

        yield BookparserItem(
            book_link=book_link,
            name=name,
            authors=authors,
            price=price,
            rate=rate
        )


