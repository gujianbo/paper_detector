import requests
from lxml import etree


class PageExtraction:
    def __init__(self, head):
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
        abstract = selector.xpath("//span[@class='abstractSection']/text()")

        info = {
            "title": title,
            "author": author,
            "conference": conference,
            "date": date,
            "page": page,
            "doi": doi,
            "pub_data": pub_data,
            "abstract": abstract,
        }
        print(info)

