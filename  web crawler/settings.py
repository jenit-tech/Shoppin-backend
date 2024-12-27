BOT_NAME = 'ecommerce_crawler'

SPIDER_MODULES = ['ecommerce_crawler.spiders']
NEWSPIDER_MODULE = 'ecommerce_crawler.spiders'


ROBOTSTXT_OBEY = False


SCRAPEOPS_API_KEY = 'YOUR_API_KEY' 


SCRAPEOPS_PROXY_ENABLED = True


EXTENSIONS = {
    'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
}


LOG_LEVEL = 'INFO'


DOWNLOADER_MIDDLEWARES = {
   
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,  


    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}


CONCURRENT_REQUESTS = 10


CONCURRENT_REQUESTS_PER_DOMAIN = 5
CONCURRENT_REQUESTS_PER_IP = 5


DOWNLOAD_DELAY = 1  

DOWNLOAD_TIMEOUT = 15  


FEED_FORMAT = 'json' 
FEED_URI = 'product_urls.json'  

