import scrapy
from scrapy.http.response.html import HtmlResponse
from bookparser.items import BookparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = [
        'https://book24.ru/catalog/estestvennye-nauki-1347/',
        'https://book24.ru/search/?q=%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F',
        'https://book24.ru/search/?q=python'
    ]

    i = 1

    def parse(self, response: HtmlResponse):
        print()
        """
        //a[@class="pagination__item _link _button _next smartLink"]/@href 
        в ChroPath получается ссылка на следующую страницу, а здесь
        response.xpath('//a[@class="pagination__item _link _button _next smartLink"]/@href')
        []
        """
        if response.status == 200:
            self.i += 1
            if 'catalog' in response.url:
                next_page = f'https://book24.ru/catalog/estestvennye-nauki-1347/page-{self.i}'
            elif 'python' in response.url:
                next_page = f'https://book24.ru/search/page-{self.i}/?q=python'
            else:
                next_page = f'https://book24.ru/search/page-{self.i}?/q=%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F'
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[contains(@class, "product-card__image-link")]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.book_parser)

    def book_parser(self, response: HtmlResponse):
        book_link = response.url
        name = response.xpath('//h1/text()').get()
        authors = response.xpath('//a[@class="product-characteristic-link smartLink"]/text()').get()
        price = response.xpath('//div[@class="product-sidebar-price product-sidebar__price-holder"]//text()').getall()
        rate = response.xpath('//span[@class="rating-widget__main-text"]//text()').get()

        yield BookparserItem(
            book_link=book_link,
            name=name,
            authors=authors,
            price=price,
            rate=rate
        )


