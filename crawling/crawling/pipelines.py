# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import CrawlingItem
from scrapy.exceptions import DropItem
from datetime import datetime

class CrawlingPipeline:

    def open_spider(self, spider):
        # self.file_content = open('output/content.json', 'w')
        # # Initial content
        # self.file_content.write("[")
        pass

    def close_spider(self, spider):
        # Content
        # self.file_content.seek(self.file_content.tell() - 3, os.SEEK_SET)
        # self.file_content.write("]")
        # self.file_content.close()
        pass

    def process_item(self, item, spider):
        # self.write_content(item)
        return item
