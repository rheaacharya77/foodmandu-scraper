# Scrapy settings for foodmandu project
BOT_NAME = "foodmandu"

SPIDER_MODULES = ["foodmandu.spiders"]
NEWSPIDER_MODULE = "foodmandu.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

#Download Handlers
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

LOG_LEVEL = 'INFO'

# Configure item pipelines
ITEM_PIPELINES = {
   "foodmandu.pipelines.FoodmanduPipeline": 300,
    "foodmandu.pipelines.DuplicatesPipeline": 400,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
