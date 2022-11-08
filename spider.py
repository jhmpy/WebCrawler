
from urllib.request import urlopen
from link_finder import LinkFinder
import webcrawler, domain

class Spider:

    directory = ''
    base_site = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, directory, base_site, domain_name):
        Spider.directory = directory
        Spider.base_site = base_site
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.directory + '/queue.txt'
        Spider.crawled_file = Spider.directory + '/crawled_site.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_site)

    @staticmethod
    def boot():
        webcrawler.create_dir(Spider.directory)
        webcrawler.create_file(Spider.directory, Spider.base_site)
        Spider.queue = webcrawler.file_to_set(Spider.queue_file)
        Spider.crawled = webcrawler.file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print("{} crawling '{}' in progress...".format(thread_name, page_url))
            print("Queue - {} | Crawled - {}".format(len(Spider.queue), len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode('utf-8')
            finder = LinkFinder(Spider.base_site, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()
    

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue or url in Spider.crawled:
                continue
            if Spider.domain_name != domain.get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        webcrawler.set_to_file(Spider.queue, Spider.queue_file)
        webcrawler.set_to_file(Spider.crawled, Spider.crawled_file)
