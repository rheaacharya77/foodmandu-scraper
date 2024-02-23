
import scrapy
class FoodmanduItem(scrapy.Item):
    # fields for the items:
    url = scrapy.Field()
    image = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    cuisine = scrapy.Field()

