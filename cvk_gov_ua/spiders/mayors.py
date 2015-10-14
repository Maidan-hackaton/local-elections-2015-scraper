# -*- coding: utf-8 -*-
from scrapy import Spider, Item, Field, Selector, Request
from cvk_gov_ua.items import MayorCandidate, CityCouncil

class MayorsSpider(Spider):
    name = "mayors"
    host = "cvk.gov.ua"
    base = "/pls/vm2015/"
    allowed_domains = [host]

    def start_requests(self):
      initial_urls = [
        'PVM117?PT001F01=100'
      ]
      for url in initial_urls:
        yield self._build_request(url, self.findRegionUrls)

    def findRegionUrls(self, response):
      for url in response.css(".a1small").xpath('@href').extract():
        yield self._build_request(url, self.findMayorListUrls)

    def findMayorListUrls(self, response):
      for url in response.css(".a1small").xpath('@href').extract():
        yield self._build_request(url, self.parseMayorList)

    def _build_request(self, url, parse):
        return Request(url='http://' + MayorsSpider.host + MayorsSpider.base + url, callback=parse)

    def parseMayorList(self, response):
        region = response.css("#result p::text")[0].extract()
        council = response.css("#result p::text")[1].extract()
        for row in response.css("#result table.t2")[1].css("tr")[1:]:
          full_name = row.css("td::text")[0].extract()
          party = row.css("td::text")[2].extract()
          yield MayorCandidate(full_name=full_name,
                               party=party,
                               city_council=council,
                               region=region)
        yield CityCouncil(name=council, region=region)
