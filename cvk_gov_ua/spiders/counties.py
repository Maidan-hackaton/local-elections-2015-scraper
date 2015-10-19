# -*- coding: utf-8 -*-
from cvk_gov_ua.items import MayorCandidate, CityCouncil
from base import BaseSpider


class RegionCountiesSpider(BaseSpider):
    name = "region_counties"

    def start_requests(self):
      initial_urls = [
        'PVM050?PT001F01=100&PT00_T001F01=100'
      ]
      for url in initial_urls:
        yield self.build_request(url, self.find_region_urls)

    def find_region_urls(self, response):
      for row in response.css("#result table.t2")[1].css("tr"):
        region_counties = row.css("td")[2].xpath("a@href").extract()
        yield self._build_request(region_counties, self.parse_counties_and_get_candidates)

    def parse_counties_and_get_candidates(self, response):
      for url in response.css(".a1small").xpath('@href').extract():
        yield self._build_request(url, self.parseMayorList)
      for row in response.css("#result table.t2")[1].css("tr"):
        county_number = row.css("td a::text").extract()
        yield RegionCounty(council=council, number=county)

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
