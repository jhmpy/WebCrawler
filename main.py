import threading
from queue import Queue
from spider import Spider
import webcrawler, domain

PROJECT_NAME = 'websites'
BASE_URL = ''  #Enter website url to be crawled here (e.g https://www.website.com)
DOMAIN_NAME = domain.get_domain_name(BASE_URL)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled_site.txt'
NO_OF_THREADS = 8
queue  = Queue()
Spider(PROJECT_NAME, BASE_URL, DOMAIN_NAME)


def crawl():
    queued_links = webcrawler.file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print("{} links in the queue".format(len(queued_links)))
        create_jobs()

def create_jobs():
    for link in webcrawler.file_to_set(QUEUE_FILE):
        queue.put(link)
        queue.join()
        crawl()

def create_workers():
    for _ in range(NO_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

create_workers()
crawl()