# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient as msl


class InstagramparserPipeline:

    def __init__(self):
        client = msl('localhost', 27017)
        self.mongo_base = client.vacancies

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        if item.get('subscriber_id'):
            collection.create_index('subscriber_id', unique=True)
        else:
            collection.create_index('subscriber_on_id', unique=True)
        collection.insert_one(item)
        return item
