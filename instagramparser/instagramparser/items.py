# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramparserItem(scrapy.Item):
    user_id = scrapy.Field()
    username = scrapy.Field()
    subscriber_id = scrapy.Field()
    subscriber_on_id = scrapy.Field()
    subscriber_name = scrapy.Field()
    subscriber_login = scrapy.Field()
    subscriber_avatar_link = scrapy.Field()
    subscriber_link = scrapy.Field()
    _id = scrapy.Field()
