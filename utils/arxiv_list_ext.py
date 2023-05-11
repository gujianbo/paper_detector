import requests
from lxml import etree


class ArxivListExtraction:
    def __init__(self, head={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                           ' Chrome/43.0.2357.130 Safari/537.36'}):
        self.head = head

    def get_html_text(self, url):
        html = requests.get(url, headers=self.head)
        return html.content.decode("utf-8")

    def get_arxiv_url(self, url):
        html_text = self.get_html_text(url)
