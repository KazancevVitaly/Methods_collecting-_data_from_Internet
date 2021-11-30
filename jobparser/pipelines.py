# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient as mcl


class JobparserPipeline:

    def __init__(self):
        client = mcl('localhost', 27017)
        self.mongo_db = client.vacansies


    def process_item(self, item, spider):
        final_salary = self.process_salary(item['salary'])

        del item['salary']

        collection = self.mongo_db[spider.name]
        collection.insert_one(item)
        return item

    # def process_salary(self, salary):
    #     min_salary = None
    #     max_salary = None
    #     return min_salary, max_salary
