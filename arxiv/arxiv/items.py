# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArxivItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    arxiv_id = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    abstract = scrapy.Field()
    subjects = scrapy.Field()
    url = scrapy.Field()
    pdf_url = scrapy.Field()
    comments = scrapy.Field()
    submission_his = scrapy.Field()
    crawl_time = scrapy.Field()

    pass
