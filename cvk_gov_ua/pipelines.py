# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import sys

#class CvkGovUaPipeline(object):
#    def process_item(self, item, spider):
#        return item


from scrapy import signals
from scrapy.exporters import JsonItemExporter
from cvk_gov_ua.items import MayorCandidate, CityCouncil

class JsonExportPipeline(object):

    def __init__(self):
        self.files = []

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        mayor_file = open('data/mayor_candidates.json', 'w+b')
        council_file = open('data/city_counsils.json', 'w+b')
        self.files.append(mayor_file)
        self.files.append(council_file)
        self.mayor_exporter = JsonItemExporter(mayor_file)
        self.council_exporter = JsonItemExporter(council_file)
        self.mayor_exporter.start_exporting()
        self.council_exporter.start_exporting()

    def spider_closed(self, spider):
        self.mayor_exporter.finish_exporting()
        self.council_exporter.finish_exporting()
        for file in self.files:
            file.close()

    def process_item(self, item, spider):
        if item.__class__ == CityCouncil:
            self.council_exporter.export_item(item)
        elif item.__class__ == MayorCandidate:
            self.mayor_exporter.export_item(item)
        return item


class StripperPipeline(object):
    def process_item(self, item, spider):
        for key, value in item.iteritems():
          item[key] = value.strip()
        return item

#from scrapy.exceptions import DropItem

#class DuplicatesPipeline(object):
#
#    def __init__(self):
#        self.ids_seen = set()
#
#    def process_item(self, item, spider):
#        if False and item['name'] in self.ids_seen:
#            raise DropItem("Duplicate item found: %s" % item)
#        else:
#            self.ids_seen.add(item['name'])
#            return item
