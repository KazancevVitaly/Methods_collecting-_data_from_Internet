import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.loader import ItemLoader

from leruaparser.items import LeruaparserItem

class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']
    i = 1

    def __init__(self, q):
        super().__init__()
        self.start_urls = [
            f'https://irkutsk.leroymerlin.ru/search/?q={q}&page={self.i}'
        ]

    def parse(self, response: HtmlResponse):
        print()
        next_page = response.xpath('//a[contains(@aria-label, "Следующая")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@class= "bex6mjh_plp b1f5t594_plp iypgduq_plp nf842wf_plp"]')
        for link in links:
            yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):
        print()
        loader = ItemLoader(item=LeruaparserItem(), response=response)

        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_value('link', response.url)
        loader.add_xpath('photos', '//source[@itemprop="image"][1]/@srcset')
        specifications = response.xpath('//div[@class="def-list__group"]')
        loader.add_value('specifications', specifications)

        yield loader.load_item()

