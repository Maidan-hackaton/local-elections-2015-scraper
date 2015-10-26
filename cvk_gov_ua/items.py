# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Party(scrapy.Item):
    name = scrapy.Field()

class CityCandidate(scrapy.Item):
    full_name = scrapy.Field()
    party = scrapy.Field()
    city_council = scrapy.Field()
    region = scrapy.Field()
    county_number = scrapy.Field()

class RegionCandidate(scrapy.Item):
    full_name = scrapy.Field()
    party = scrapy.Field()
    region = scrapy.Field()
    county_number = scrapy.Field()

class CityCouncilCandidate(scrapy.Item):
    full_name = scrapy.Field()
    party = scrapy.Field()
    region = scrapy.Field()
    council = scrapy.Field()
    county_number = scrapy.Field()
    info = scrapy.Field()
    first_candidate = scrapy.Field()

class MayorCandidate(scrapy.Item):
    full_name = scrapy.Field()
    party = scrapy.Field()
    city_council = scrapy.Field()
    region = scrapy.Field()

class County(scrapy.Item):
    council = scrapy.Field()
    number = scrapy.Field()

class RegionCounty(County):
    boundaries = scrapy.Field()

class CityCounty(County):
    boundaries = scrapy.Field()
    region = scrapy.Field()

class CityCouncil(scrapy.Item):
    name = scrapy.Field()
    region = scrapy.Field()
