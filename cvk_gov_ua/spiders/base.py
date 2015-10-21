from scrapy import Spider, Request

class BaseSpider(Spider):
    host = "cvk.gov.ua"
    base = "/pls/vm2015/"
    allowed_domains = [host]

    def getBaseUrl(self):
        return BaseSpider.host + BaseSpider.base

    def build_request(self, url, parse, meta=None):
        return Request(url='http://' + self.getBaseUrl() + url, callback=parse, meta=meta)
