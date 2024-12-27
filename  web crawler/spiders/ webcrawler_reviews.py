import scrapy
from urllib.parse import urljoin

class GenericReviewsSpider(scrapy.Spider):
    name = "generic_reviews"

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv'}}
    }

    def __init__(self, urls=None, review_selectors=None, *args, **kwargs):
        """
        Initialize the spider with URLs and review selectors.
        :param urls: Comma-separated string of URLs to start crawling.
        :param review_selectors: Dictionary of CSS selectors for extracting reviews.
        """
        super(GenericReviewsSpider, self).__init__(*args, **kwargs)
        self.start_urls = urls.split(',') if urls else []
        try:
            self.review_selectors = eval(review_selectors) if review_selectors else {}
        except Exception as e:
            self.logger.error(f"Error parsing review selectors: {e}")
            self.review_selectors = {}

    def parse(self, response):
        """
        Parse the review page dynamically based on the provided selectors.
        """
        if not self.review_selectors:
            self.logger.error("No review selectors provided. Please provide valid CSS selectors.")
            return

       
        review_selector = self.review_selectors.get("review_elements")
        if not review_selector:
            self.logger.error("Missing 'review_elements' selector in review_selectors.")
            return

        review_elements = response.css(review_selector)
        if not review_elements:
            self.logger.warning(f"No reviews found on page: {response.url}")

        for review_element in review_elements:
           
            yield {
                "url": response.url,
                "title": review_element.css(self.review_selectors.get("title", "")).get(default="").strip(),
                "text": " ".join(review_element.css(self.review_selectors.get("text", "")).getall()).strip(),
                "rating": review_element.css(self.review_selectors.get("rating", "")).re_first(r"(\d+\.?\d*)") or "",
                "date": review_element.css(self.review_selectors.get("date", "")).get(default="").strip(),
                "verified": bool(review_element.css(self.review_selectors.get("verified", ""))),
            }

       
        next_page_selector = self.review_selectors.get("next_page")
        if next_page_selector:
            next_page_relative_url = response.css(next_page_selector).get()
            if next_page_relative_url:
                next_page = urljoin(response.url, next_page_relative_url)
                self.logger.info(f"Following next page: {next_page}")
                yield scrapy.Request(url=next_page, callback=self.parse)
            else:
                self.logger.info(f"No next page found on: {response.url}")
