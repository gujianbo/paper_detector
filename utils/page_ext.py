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
        print(title)

