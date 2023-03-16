import requests
from lxml import etree


class PageExtraction:
    def __init__(self, head={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'}):
        self.head = head

    def get_html_text(self, url):
        html = requests.get(url, headers=self.head)
        return html.content.decode("utf-8")

    def get_acm_info(self, url):
        html_text = self.get_html_text(url)
        selector = etree.HTML(html_text.encode("utf-8"))
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
            "title": title[0] if len(title) > 0 else "",
            "author": author,
            "conference": conference[0] if len(conference) > 0 else "",
            "date": date[0] if len(date) > 0 else "",
            "page": page[0] if len(page) > 0 else "",
            "doi": doi[0] if len(doi) > 0 else "",
            "pub_data": pub_data[0] if len(pub_data) > 0 else "",
            "abstract": "\n".join(abstract),
            "ref": ref
        }
        print(info)

    def get_arxiv_info(self, url):
        html_text = self.get_html_text(url)
        selector = etree.HTML(html_text.encode("utf-8"))
        title = selector.xpath("//h1[contains(@class,'title')]/text()")
        author = selector.xpath("//div[@class='authors']/a/text()")
        comments = selector.xpath("//td[@class='comments']/text()")
        last_sub_data = selector.xpath("//div[@class='submission-history']/text()[last()]]")
        abstract = selector.xpath("//blockquote[contains(@class,'abstract')]/text()")
        ref = selector.xpath("//span[@class='references__note']/text()")
        subjects_arr = selector.xpath("//td[@class='subjects']/text()")
        subjects = []
        for sub in subjects_arr:
            subjects += sub.strip().strip(";").split(";")
        primary_subject = selector.xpath("//span[@class='primary-subject']/text()")

        info = {
            "title": title[0] if len(title) > 0 else "",
            "author": author,
            "comments": comments[0] if len(comments) > 0 else "",
            "last_sub_data": last_sub_data[0] if len(last_sub_data) > 0 else "",
            "abstract": "\n".join(abstract),
            "ref": ref,
            "primary_subject": primary_subject[0] if len(primary_subject) > 0 else "",
            "subjects": subjects,
        }
        print(info)


