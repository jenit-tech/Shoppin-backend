import scrapy
from urllib.parse import urljoin

class ProductURLCrawler(scrapy.Spider):
    name = "product_url_crawler"

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.json': {'format': 'json', 'indent': 4}},
        'CONCURRENT_REQUESTS': 16, 
        'DOWNLOAD_DELAY': 0.25,  
    }

    def __init__(self, domains=None, *args, **kwargs):
        super(ProductURLCrawler, self).__init__(*args, **kwargs)
        if not domains:
            raise ValueError("You must provide a comma-separated list of domains using the 'domains' argument.")
        self.start_domains = domains.split(',')

    def start_requests(self):
        """
        Initiates crawling by visiting the homepage of each domain.
        """
        for domain in self.start_domains:
            start_url = f'https://{domain.strip()}'
            yield scrapy.Request(url=start_url, callback=self.parse_homepage, meta={'domain': domain.strip()})

    def parse_homepage(self, response):
        """
        Parses the homepage and extracts potential product links and category links for deeper crawling.
        """
        domain = response.meta['domain']

       
        for link in self.extract_product_links(response):
            yield {
                'domain': domain,
                'product_url': link
            }

        
        category_links = response.css('a::attr(href)').getall()
        for link in category_links:
            absolute_url = urljoin(response.url, link)
            if self.is_valid_url(absolute_url, domain):
                yield scrapy.Request(url=absolute_url, callback=self.parse_category_page, meta={'domain': domain})

    def parse_category_page(self, response):
        """
        Parses category pages and extracts product links.
        """
        domain = response.meta['domain']

       
        for link in self.extract_product_links(response):
            yield {
                'domain': domain,
                'product_url': link
            }

        
        pagination_links = response.css('a::attr(href)').getall()
        for link in pagination_links:
            absolute_url = urljoin(response.url, link)
            if self.is_valid_url(absolute_url, domain):
                yield scrapy.Request(url=absolute_url, callback=self.parse_category_page, meta={'domain': domain})

    def extract_product_links(self, response):
        """
        Extracts product links using common URL patterns for e-commerce websites.
        """
        product_links = []
        for link in response.css('a::attr(href)').getall():
            absolute_url = urljoin(response.url, link)
            if any(pattern in absolute_url for pattern in ['/product/', '/item/', '/p/']):
                product_links.append(absolute_url)
        return list(set(product_links))  

    def is_valid_url(self, url, domain):
        """
        Validates if the URL belongs to the same domain and is not an unwanted link (e.g., login, help).
        """
        return domain in url and not any(unwanted in url for unwanted in ['login', 'help', 'customer'])

