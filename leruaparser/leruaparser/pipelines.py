# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes
from pymongo import MongoClient as mcl
from hashlib import sha1


class LeruaparserPipeline:

    def process_item(self, item, spider):
        print()
        final_specifications = self.process_specifications(item['specifications'])
        item['specifications'] = final_specifications
        return item

    def process_specifications(self, specifications):
        data_spec = {}
        for spec in specifications:
            key = spec.xpath('.//dt/text()').get()
            value = spec.xpath('.//dd/text()').get()
            value = value.replace(u'\n', u'')
            value = value.replace(u'  ', u'')
            data_spec[key] = value

        return data_spec


class LeruaPhotosPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        print()
        if item['photos']:
            for image in item['photos']:
                try:
                    yield scrapy.Request(image)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        print()
        item['photos'] = [el[1] for el in results if el[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=True):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        dir_name = item['name']
        return f'{dir_name}/{image_guid}.jpg'
