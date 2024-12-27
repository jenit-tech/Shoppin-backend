import scrapy
from urllib.parse import urljoin
import json
import re

class EcommerceProductURLSpider(scrapy.Spider):
    name = "ecommerce_product_url"

    custom_settings = {
        'FEEDS': {
            'data/%(name)s_%(time)s.json': {'format': 'json'}
        },
        'CONCURRENT_REQUESTS': 16,  
        'DOWNLOAD_DELAY': 0.5,  
    }

    def __init__(self, domains=None, *args, **kwargs):
        super(EcommerceProductURLSpider, self).__init__(*args, **kwargs)
        if domains:
            self.domains = domains.split(",")
        else:
            self.domains = ["example1.com", "example2.com"] 

    def start_requests(self):
        for domain in self.domains:
            start_url = f"https://{domain}"
            yield scrapy.Request(url=start_url, callback=self.discover_product_urls, meta={'domain': domain, 'depth': 0})

    def discover_product_urls(self, response):
        domain = response.meta['domain']
        depth = response.meta['depth']

       
        links = response.css("a::attr(href)").getall()
        product_urls = []
        for link in links:
            absolute_url = urljoin(response.url, link)
            if self.is_product_url(absolute_url, domain):
                product_urls.append(absolute_url)

        
        unique_product_urls = list(set(product_urls))
        for product_url in unique_product_urls:
            yield {"domain": domain, "product_url": product_url}

        
        if depth < 2:  
            next_links = [urljoin(response.url, link) for link in links if self.is_valid_link(link)]
            for next_link in next_links:
                yield scrapy.Request(url=next_link, callback=self.discover_product_urls, meta={'domain': domain, 'depth': depth + 1})

    def is_product_url(self, url, domain):
        
        product_patterns = [r"/product/", r"/item/", r"/p/"]
        if domain in url:
            for pattern in product_patterns:
                if re.search(pattern, url):
                    return True
        return False

    def is_valid_link(self, link):
       
        exclude_patterns = [r"/about", r"/contact", r"/terms", r"/privacy"]
        for pattern in exclude_patterns:
            if re.search(pattern, link):
                return False
        return True
