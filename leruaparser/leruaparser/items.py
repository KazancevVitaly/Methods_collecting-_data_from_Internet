# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from platform import processor
from itemloaders.processors import TakeFirst, MapCompose


def process_price(price):
    try:
        price = price.replace(u' ', u'')
        price = int(price)
    except Exception as e:
        print(e)
    return price


class LeruaparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(process_price))
    link = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    specifications = scrapy.Field()


