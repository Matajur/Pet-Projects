import time
from news.scrap_news import articles_scraped

def start_timer():
    while True:
        articles_scraped()
        time.sleep(3600)