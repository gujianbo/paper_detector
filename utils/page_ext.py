import requests
from lxml import etree


class PageExtraction:
    def __init__(self, head={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'}):
        self.head = head

    def get_html_text(self, url):
        html = requests.get(url, headers=self.head)
        return html.text

    def get_info(self, url):
        html_text = self.get_html_text(url)
        selector = etree.HTML(html_text)
        title = selector.xpath("//h1[@class='citation__title']/text()")
        author = selector.xpath("//span[@class='loa__author-name']/span/text()")
        conference = selector.xpath("//span[@class='epub-section__title']/text()")
        date = selector.xpath("//span[@class='epub-section__date']/text()")
        page = selector.xpath("//span[@class='epub-section__pagerange']/text()")
        doi = selector.xpath("//a[@class='issue-item__doi']/text()")
        pub_data = selector.xpath("//span[@class='CitationCoverDate']/text()")
        abstract = selector.xpath("//div[contains(@class,'abstractSection')]/p/text()")

        ref = selector.xpath("//span[@class='references__note']/text()")

        info = {
            "title": title[0],
            "author": author,
            "conference": conference[0],
            "date": date[0],
            "page": page[0],
            "doi": doi[0],
            "pub_data": pub_data[0],
            "abstract": abstract,
            "ref": ref[:3]
        }
        print(info)

