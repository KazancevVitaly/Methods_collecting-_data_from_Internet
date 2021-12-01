# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient as mcl

class BookparserPipeline:

    def __init__(self):
        client = mcl('localhost', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        print()
        if spider.name == 'labirint':
            item['authors'].pop(0)
            name = item['name'].split(': ')
            item['name'] = name[-1]
            final_price = self.process_price_labirint(item['price'])
            item['discount'] = final_price[0]
            item['old_price'] = final_price[1]
        else:
            name = item['name'].split(': ')
            item['name'] = name[-1]
            final_price = self.process_price_book24(item['price'])
            item['discount'] = final_price[0]
            item['old_price'] = final_price[1]
        del item['price']

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item

    def process_price_labirint(self, price):
        price_list = []
        for pr in price:
            try:
                pr = int(pr)
                price_list.append(pr)
            except ValueError:
                continue
        discount = min(price_list)    # цена со скидкой
        old_price = max(price_list)    # цена без скидки

        return discount, old_price

    def process_price_book24(self, price):
        price_list = []
        for pr in price:
            pr = pr.replace(u' ', u'')
            pr = pr.replace(u'₽', u'')
            pr = pr.replace(u'\xa0', u'')
            try:
                pr = int(pr)
                price_list.append(pr)
            except ValueError:
                continue

        discount = min(price_list)  # цена со скидкой
        old_price = max(price_list)  # цена без скидки

        return discount, old_price

