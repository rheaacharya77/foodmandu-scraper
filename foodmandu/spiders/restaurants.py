import scrapy
from ..items import FoodmanduItem
from scrapy_playwright.page import PageMethod


class RestaurantscrapperSpider(scrapy.Spider):
    name = "restaurants"

    def start_requests(self):
        url = "https://foodmandu.com/Restaurant/Index"
        yield scrapy.Request(url, meta={
            "playwright": True,  # Enable Playwright middleware
            "playwright_include_page": True,  # Include Playwright page in the response
            "playwright_page_methods": [
                PageMethod('wait_for_selector', 'div.wrapper-listing'),  # Wait for the main content to load
                PageMethod('evaluate', 'window.scrollBy(0,document.body.scrollHeight)'),  # Scroll to the bottom of the page
                PageMethod('wait_for_selector', 'div.col-md-4.col-lg-4.spinner.ng-scope:nth-child(11)'),  # Wait for specific elements to ensure page has loaded
            ],
        }, errback=self.errback)


    # Parse the response
    async def parse(self, response):
        
        page = response.meta["playwright_page"]
        last_height = await page.evaluate("() => document.body.scrollHeight")


        while True:
            await page.evaluate('window.scrollTo(0,document.body.scrollHeight)')  # Scroll to the bottom of the page
            await page.wait_for_timeout(2000)  # Wait for dynamic content to load


            new_height = await page.evaluate("() => document.body.scrollHeight")
            if new_height == last_height: 
                break
            last_height = new_height


            # Extract data from the page
            data = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('.col-md-4.col-lg-4.spinner.ng-scope')).map(restaurant => {
                    return {
                        url: restaurant.querySelector('.listing__photo a').getAttribute('href'),
                        image: restaurant.querySelector('.listing__photo img').getAttribute('src'),
                        name: restaurant.querySelector('.title20.mt-2 a').textContent.trim(),
                        address: restaurant.querySelector('.subtitle > div > span.ng-binding').textContent.trim(),
                        cuisine: restaurant.querySelector('.subtitle > div:nth-child(2) > span.ng-binding').textContent.trim()
                    };
                });
            }''')
 
        # Process extracted data and yield items
        for item_data in data:
                full_url = "https://foodmandu.com" + item_data['url'] if not item_data['url'].startswith('http') else item_data['url']
                item = FoodmanduItem()
                item['url'] = full_url
                item['image'] = item_data['image']
                item['name'] = item_data['name']
                item['address'] = item_data['address']
                item['cuisine'] = item_data['cuisine']
                yield item
                    
        await page.close()

    # Error handling
    async def errback(self, failure):
        self.logger.error(repr(failure))
    
