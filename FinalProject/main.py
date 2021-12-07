import json

from scrapy.crawler import CrawlerProcess
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from web_crawler.spiders.concordia_spider import firstSpider
from web_crawler.lib import remove_old_outputs


def run_crawler_process():
    remove_old_outputs()
    max_pages = int(input("Enter How many pages you want to scrap? [Upper Boud]:"))

    crawler_process = CrawlerProcess(settings={
        "CONCURRENT_REQUESTS": 1,
        "ROBOTSTXT_OBEY": True,
        "CLOSESPIDER_ITEMCOUNT": max_pages - 1,
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


def calculate_k_mean(true_k, documents):
    print("👉 Clustering with K as:", true_k)
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(documents)

    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=300, n_init=10, random_state=0)
    model.fit(X)

    # positive_cluster_center = model.cluster_centers_[0]
    # negative_cluster_center = model.cluster_centers_[2]

    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    for i in range(true_k):
        print("\n===> Cluster:" + str(i))
        for ind in order_centroids[i, :10]:
            print(terms[ind])


def k_meanse_process():
    data = None
    with open("Outputs/data.json") as f:
        data = json.load(f)
        documents = [doc['title'] + " " + doc['body'] for doc in data]

        # Clustering with K=3
        calculate_k_mean(true_k=3, documents=documents)
        print()
        # Clustering with K=6
        calculate_k_mean(true_k=6, documents=documents)

        # The Elbow Method (Extra)
        # wcss = []
        # for i in range(1, 11):
        #     model = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        #     model.fit(X)
        #     wcss.append(model.inertia_)
        #
        # plt.plot(range(1, 11), wcss)
        # plt.title('The Elbow Method')
        # plt.xlabel('Number of clusters')
        # plt.ylabel('WCSS')
        # plt.savefig('elbow.png')
        # plt.show()


def main():
    # run_crawler_process()
    k_meanse_process()


if __name__ == "__main__":
    main()
