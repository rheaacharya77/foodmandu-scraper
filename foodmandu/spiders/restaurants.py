import scrapy
from ..items import FoodmanduItem
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector

class RestaurantscrapperSpider(scrapy.Spider):
    name = "restaurants"

    def start_requests(self):
        url = "https://foodmandu.com/Restaurant/Index"
        yield scrapy.Request(url, meta={
            "playwright": True,  # Enable Playwright middleware
            "playwright_include_page": True,  # Include Playwright page in the response
            "playwright_page_methods": [
               PageMethod('wait_for_selector', 'div.col-md-4.col-lg-4.spinner.ng-scope:nth-child(6)'),  # Wait for initial set of restaurant items to load
            ],
        }, errback=self.errback)


    # Parse the response
    async def parse(self, response):
        
        page = response.meta["playwright_page"]
        #initial scroll height
        last_height = await page.evaluate("() => document.body.scrollHeight")

        while True:
            await page.evaluate('window.scrollTo(0,document.body.scrollHeight)')
            await page.wait_for_timeout(2000)

            new_height = await page.evaluate("() => document.body.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height

            selector = Selector(text=await page.content())

        # Extract and yield each restaurant's details
        for restaurant in selector.css('.col-md-4.col-lg-4.spinner.ng-scope'):
            partial_url = restaurant.css('.listing__photo > a::attr(href)').get()
            full_url = "https://foodmandu.com" + partial_url if not partial_url.startswith('http') else partial_url
            yield FoodmanduItem(
                url= full_url,
                image=restaurant.css('.listing__photo img::attr(src)').get(),
                name=restaurant.css('.title20.mt-2 > a::text').get().strip(),
                address=restaurant.css('.subtitle > div > span.ng-binding::text').get().strip(),
                cuisine=restaurant.css('.subtitle > div:nth-child(2) > span.ng-binding::text').get().strip()
           )
        #close playwright page
        await page.close()  
        

    # Error handling
    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()
    
