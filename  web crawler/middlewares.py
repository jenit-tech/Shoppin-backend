from scrapy_playwright.page import PageCoroutine

class PlaywrightMiddleware:
    async def process_request(self, request, spider):
       
        return PageCoroutine("wait_for_selector", "div.product")
