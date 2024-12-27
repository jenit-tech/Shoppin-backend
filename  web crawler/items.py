import scrapy

class ProductUrlItem(scrapy.Item):
    domain = scrapy.Field()  # The domain the product belongs to
    product_url = scrapy.Field()  # The direct product URL
