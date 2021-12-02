from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leruaparser.spiders.leroymerlinru import LeroymerlinruSpider as ls
from leruaparser import settings

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    crawler_process = CrawlerProcess(settings=crawler_settings)
    # q = input('Укажите необходимый товар:\n')
    q = 'Ель+искусственная'
    crawler_process.crawl(ls, q=q)
    crawler_process.start()
