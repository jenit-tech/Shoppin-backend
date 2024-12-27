
import json

class SaveProductURLsPipeline:
    def open_spider(self, spider):
        self.file = open("product_urls.json", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.file.write(json.dumps(item) + "\n")
        return item
