import re

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from web_crawler.items import WebCrawlerItem
from web_crawler.lib import create_folder


class firstSpider(scrapy.Spider):
    name = "concordia"
    folder_name = "Outputs/HTML_Pages"
    base_url = "https://www.concordia.ca"
    allowed_domains = ["concordia.ca"]
    start_urls = [base_url]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")

        yield from self.scrape(response, soup)

        for link in soup.find_all('a', href=True):
            if link['href'].startswith('/') and link['href'].endswith('.html') and len(link['href']) > 2:
                # print(self.base_url + link['href'])
                yield Request(self.base_url + link['href'], callback=self.parse)
            elif link['href'].startswith('http') and link['href'].endswith('.html'):
                # print(link['href'])
                yield Request(link['href'], callback=self.parse)

    def scrape(self, response, soup):
        # Save Page as HTML
        # filename = response.url.split("/")[-2] + '.html'
        filename = str(response.url).replace("http://", "").replace("https://", "").replace("/","--")+".html"
        # Create a Folder if it doesn't exist
        create_folder(self.folder_name)
        # Write Down the HTML File
        with open(self.folder_name + "/" + filename, 'wb') as f:
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
