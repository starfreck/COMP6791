import re

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request
from urllib.parse import urlparse
from web_crawler.items import WebCrawlerItem
from web_crawler.lib import create_folder


class firstSpider(scrapy.Spider):
    counter = 1
    name = "concordia"
    folder_name = "Outputs/HTML_Pages"
    base_url = "https://www.concordia.ca"
    # Login Page URL (We do not want to Scarp this!)
    avoid_keyword = "wsignin1"
    allowed_domains = ["concordia.ca"]
    start_urls = [base_url]
    visited_urls = [base_url]

    def parse(self, response):

        soup = BeautifulSoup(response.body, "lxml")

        yield from self.scrape(response, soup)

        for link in soup.find_all('a', href=True):
            new_url = None
            if link['href'].startswith('/') and link['href'].endswith('.html') and len(link['href']) > 2:
                new_url = self.base_url + link['href']
                # print(new_url)
                if new_url not in self.visited_urls and not new_url.startswith(self.avoid_keyword):
                    yield Request(new_url, callback=self.parse)
            elif link['href'].startswith('http') and link['href'].endswith('.html'):
                new_url = link['href']
                # print(new_url)
                if new_url not in self.visited_urls and not new_url.startswith(self.avoid_keyword):
                    yield Request(new_url, callback=self.parse)

    def scrape(self, response, soup):
        # Save Page as HTML
        url = urlparse(response.url)
        page_name = str(url.path.split("/")[-1])

        if not page_name.endswith(".html"):
            if not page_name:
                page_name = url.netloc + ".html"
            else:
                page_name = page_name + ".html"
        filename = str(self.counter) + "-" + page_name

        # Create a Folder if it doesn't exist
        create_folder(self.folder_name)
        # Write Down the HTML File
        with open(self.folder_name + "/" + filename, 'wb') as f:
            print("Processing File No. ->", self.counter, "URL->", response.url)
            self.counter += 1
            f.write(response.body)

        # Extract Data & Creating a new Item object
        item = WebCrawlerItem()
        item['url'] = response.url
        item['title'] = soup.title.text
        item['body'] = text_cleaner(soup.get_text())

        yield item


def text_cleaner(string):
    # string = string.replace(".", "")
    string = re.sub('[^a-zA-Z0-9 \.]', ' ', string)
    string = re.sub(' +', ' ', string)
    return string
