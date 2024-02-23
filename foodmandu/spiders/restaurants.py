import scrapy


class RestaurantsSpider(scrapy.Spider):
    name = "restaurants"
    allowed_domains = ["foodmandu.com"]
    start_urls = ["https://foodmandu.com"]

    def parse(self, response):
        pass
