from html.parser import HTMLParser
from urllib import parse

class LinkFinder(HTMLParser):

    def __init__(self, base_site, page_url):
        super().__init__()
        self.base_site = base_site
        self.page_url = page_url
        self.links = set()

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attribute, value in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_site, value)
                    self.links.add(url)

    def page_links(self):
        return self.links

