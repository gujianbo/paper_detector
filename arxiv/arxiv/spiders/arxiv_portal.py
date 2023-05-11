import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import time
# import sys
# sys.path.append("..")
from arxiv.items import ArxivItem
import logging


class ArxivPortalSpider(CrawlSpider):
    name = "arxiv_portal"
    allowed_domains = ["arxiv.org"]
    start_urls = ["https://arxiv.org/list/cs.AI/recent",  # Artificial Intelligence
                  "https://arxiv.org/list/cs.CV/recent",  # Computer Vision and Pattern Recognition
                  "https://arxiv.org/list/cs.LG/recent",  # machine learning
                  "https://arxiv.org/list/cs.MM/recent",  # Multimedia
                  "https://arxiv.org/list/cs.DC/recent",  # Distributed, Parallel, and Cluster Computing
                  "https://arxiv.org/list/cs.HC/recent",  # Human-Computer Interaction
                  "https://arxiv.org/list/cs.SD/recent",  # Sound
                  "https://arxiv.org/list/cs.RO/recent",  # Robotics
                  "https://arxiv.org/list/cs.NE/recent",  # Neural and Evolutionary Computing
                  "https://arxiv.org/list/stat.ML/recent"  # machine learning
                  ]

    rules = (
        Rule(LinkExtractor(allow=r"https\://arxiv\.org/list/(cs|stat)\.(AI|CV|LG|MM|DC|HC|SD|RO|NE|ML)/pastweek\?skip=\d+&show=25*"), follow=True),
        Rule(LinkExtractor(allow=r"https\://arxiv\.org/list/(cs|stat)\.(AI|CV|LG|MM|DC|HC|SD|RO|NE|ML)/recent"), follow=True),
        Rule(LinkExtractor(allow=r"https\://arxiv\.org/abs/\d+\.\d+"), callback="parse_item", follow=True)
    )

    def parse_item(self, response):
        title = response.xpath('//div[@id="abs"]/h1[contains(@class, "title")]/text()').extract_first().strip()
        authors = response.xpath('//div[@id="abs"]/div[contains(@class, "authors")]/a/text()').extract().strip()
        abstract = response.xpath('//div[@id="abs"]/blockquote[contains(@class, "abstract")]/text()').extract().strip()
        abstract = " ".join(abstract).replace("\n", " ").strip()
        comments = response.xpath('//div[@class="metatable"]//td[contains(@class, "comments")]/text()').extract_first().strip()
        subjects = response.xpath('//div[@class="metatable"]//td[contains(@class, "subjects")]')
        subjects = subjects.xpath("string(.)").extract()[0].replace("\n", "").strip()
        submission_his = response.xpath('//div[@class="submission-history"]/text()').extract()
        submission_his = [item.replace("\n", "").strip() for item in submission_his if item.replace("\n", "").strip() != ""]
        submission_his = [item for item in submission_his if re.match(r".*20\d{2}.*", item)]
        url = response.url
        pdf_url = "https://arxiv.org" + response.xpath('//div[@class="full-text"]//a[contains(@class, "download-pdf")]/@href').extract_first().strip()
        crawl_time = int(time.time())
        reg = r"https\://arxiv\.org/abs/(\d+\.\d+)"
        id_match = re.match(reg, url)
        if not id_match:
            logging.error(f"url {url} reg error!")
        else:
            id = id_match.groups()[0]
            yield ArxivItem(
                _id=id,
                title=title,
                authors=authors,
                abstract=abstract,
                comments=comments,
                submission_his=submission_his,
                url=url,
                pdf_url=pdf_url,
                subjects=subjects,
                crawl_time=crawl_time
            )


if __name__ == "__main__":
    # reg = r"https\://arxiv\.org/list/(cs|stat)\.(AI|CV|LG|MM|DC|HC|SD|RO|NE|ML)/pastweek\?skip=\d+&show=25*"
    # match = re.match(reg, "https://arxiv.org/list/stat.ML/pastweek?skip=25&show=25")
    # print(match.group())

    reg = r"https\://arxiv\.org/abs/(\d+\.\d+)"
    match = re.match(reg, "https://arxiv.org/abs/2305.05642")
    print(match.groups()[0])

    # reg = r".*20\d{2}.*"
    # match = re.match(reg, "Wed, 21 Jun 2017 16:05:17 UTC (8,172 KB)")
    # print(match.group())
    # match = re.match(reg, "repalce")
    # print(match)
