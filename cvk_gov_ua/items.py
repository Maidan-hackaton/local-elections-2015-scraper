# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Party(scrapy.Item):
    name = scrapy.Field()

class Candidate(scrapy.Item):
    full_name = scrapy.Field()
    party = scrapy.Field()
    council = scrapy.Field()
    county = scrapy.Field()

class MayorCandidate(scrapy.Item):
    full_name = scrapy.Field()
    party = scrapy.Field()
    city_council = scrapy.Field()
    region = scrapy.Field()

class County(scrapy.Item):
    council = scrapy.Field()
    number = scrapy.Field()

class CityCouncil(scrapy.Item):
    name = scrapy.Field()
    region = scrapy.Field()
