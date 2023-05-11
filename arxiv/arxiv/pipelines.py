# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class ArxivPipeline(object):
    # 爬虫开始之前执行的逻辑
    def open_spider(self, spider):
        url = "mongodb://jianbogu:123456@10.101.104.24:27017/"
        self.client = pymongo.MongoClient(url)
        self.paper = self.client['arxiv']['paper']

    # 爬虫执行完之后跑的逻辑
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item_json = dict(item)
        id = item_json["_id"]
        if self.paper.find_one({"_id": id}):
            self.paper.update_one({"_id": "id"}, {"$set": item_json})
        else:
            self.paper.insert_one(item_json)

        return item
