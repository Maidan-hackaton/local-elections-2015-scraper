# -*- coding: utf-8 -*-
from cvk_gov_ua.items import RegionCounty, Candidate
from base import BaseSpider


class RegionCountiesSpider(BaseSpider):
    name = "region_counties"

    def start_requests(self):
      initial_urls = [
        'PVM050?PT001F01=100&PT00_T001F01=100',
        'PVM050?PT001F01=101&PT00_T001F01=100'
      ]
      for url in initial_urls:
        yield self.build_request(url, self.find_region_urls)

    def find_region_urls(self, response):
      for row in response.css("#result table.t2")[0].css("tr")[1:]:
        region_urls = row.css("td")[1].css("a").xpath("@href").extract()
        for region_url in region_urls:
          yield self.build_request(region_url, self.parse_counties_and_get_candidates)

    def parse_counties_and_get_candidates(self, response):
      region = response.css("#result p.p1::text").extract()[0]
      for row in response.css("#result table.t2")[0].css("tr")[1:]:
        county_number = row.css("td a::text").extract()[0]
        boundaries = row.css("td")[3].css("::text").extract()[0]
        yield RegionCounty(council=region + u", обласна рада", number=county_number, boundaries=boundaries)
        county_number = row.css("td a::text").extract()[0]
        url = row.css("td a").xpath("@href").extract()[0]
        yield self.build_request(url, self.parseCandidateList,
                                 {"region":region, "county_number":county_number})

    def parseCandidateList(self, response):
        for row in response.css("#result table.t2")[0].css("tr")[1:]:
          full_name = row.css("td")[1].css("::text").extract()
          if full_name:
              full_name = full_name[0]
          else:
              # TODO first_candidate
              continue
          info = row.css("td::text").extract()[2]
          party = row.css("td b::text").extract()[0]
          first_candidate = row.css("td")[0].css("::text").extract()[1]
          yield Candidate(full_name=full_name,
                               party=party,
                               county_number=response.meta["county_number"],
                               region=response.meta["region"])
