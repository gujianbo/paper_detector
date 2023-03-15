import requests


class PageExtraction:
    def __init__(self, head):
        self.head = head

    def get_html_text(self, url):
        html = requests.get(url, headers=self.head)
        return html.text
