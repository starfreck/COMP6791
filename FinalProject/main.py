from scrapy.crawler import CrawlerProcess

from web_crawler.spiders.concordia_spider import firstSpider
from web_crawler.lib import remove_old_outputs


def run_crawler_process():
    remove_old_outputs()
    max_pages = int(input("Enter How many pages you want to scrap? [Upper Boud]:"))

    crawler_process = CrawlerProcess(settings={
        "CONCURRENT_REQUESTS": 1,
        "ROBOTSTXT_OBEY": True,
        "CLOSESPIDER_ITEMCOUNT": max_pages-1,
        "LOG_LEVEL": "INFO",
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en",
        },
        "ITEM_PIPELINES": {
            'web_crawler.pipelines.WebCrawlerPipeline': 300,
        }
    })

    crawler_process.crawl(firstSpider)
    crawler_process.start()


def main():
    run_crawler_process()


if __name__ == "__main__":
    main()
