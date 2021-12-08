import json
import sys

from afinn import Afinn
from scrapy.crawler import CrawlerProcess
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from tabulate import tabulate

from web_crawler.spiders.concordia_spider import firstSpider
from web_crawler.lib import remove_old_outputs, exists


def run_crawler_process():
    print("\nTo Stop Crawler Click Stop Button once and wait...\n")
    remove_old_outputs()

    crawler_process = CrawlerProcess(settings={
        "CONCURRENT_REQUESTS": 1,
        "ROBOTSTXT_OBEY": True,
        "CLOSESPIDER_ITEMCOUNT": max_pages,
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

    model = KMeans(n_clusters=true_k, init='k-means++', random_state=0)
    model.fit(X)

    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    clusters = []
    for i in range(true_k):
        print("\n===> Cluster:" + str(i))
        cluster = []
        for index in order_centroids[i, :max_term_per_cluster]:
            cluster.append(terms[index])
        clusters.append(cluster)
        for index in order_centroids[i, :max_term_per_cluster]:
            print(terms[index])
    return clusters


def k_means_process():
    data = None
    with open(OUTPUT_FILE) as f:
        data = json.load(f)
        documents = [doc['title'] + " " + doc['body'] for doc in data]

        # Clustering with K=3
        word_clusters = calculate_k_mean(true_k=3, documents=documents)
        # Afinn on Clusters with K=3
        scores = afinn_process(word_clusters)
        print_as_table(scores)

        # New Line
        print()

        # Clustering with K=6
        word_clusters = calculate_k_mean(true_k=6, documents=documents)
        # Afinn on Clusters with K=6
        scores = afinn_process(word_clusters)
        print_as_table(scores)

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


def afinn_process(clusters):
    clusters_score = {}
    cluster_count = 0
    afinn = Afinn()
    for cluster in clusters:
        score = 0
        for word in cluster:
            score += afinn.score(word)
        clusters_score['Cluster ' + str(cluster_count)] = score
        cluster_count += 1
    return clusters_score


def print_as_table(clusters_scores):
    print("\n👉 # AFINN Sentiment Analysis\n")

    headers = ['#', 'Name', 'Score', 'Verdict']
    table = []
    count = 1

    for cluster, score in clusters_scores.items():
        if score > 0:
            verdict = "POSITIVE"
        elif score < 0:
            verdict = "NEGATIVE"
        else:  # score == 0
            verdict = "NEUTRAL"
        table.append([count, cluster, verdict, score])
        count += 1

    print(tabulate(table, headers, tablefmt="psql"))


def main():
    if run_crawler_flag:
        run_crawler_process()

    k_means_process()


if __name__ == "__main__":
    global max_pages, max_term_per_cluster, run_crawler_flag, OUTPUT_FILE
    OUTPUT_FILE = "Outputs/data.json"

    print("\n=> [If you want to use \"Default\" the just press Enter]")
    try:
        run_crawler_flag = bool(
            input("\nDo you want to run crawler? (otherwise, we will use data.json from previous ""run) [Default:No]:"))

        if not exists(OUTPUT_FILE):
            run_crawler_flag = True
    except:
        run_crawler_flag = False

    if run_crawler_flag:
        try:
            max_pages = int(input("\nEnter How many pages you want to scrap? [Lower Bound:10|Upper Bound (Default:100)]:"))
            if max_pages <= 10:
                max_pages = 10
        except:
            max_pages = 100

    try:
        max_term_per_cluster = int(input("\nEnter How many term you want to print per cluster? [Default:50]:"))
    except:
        max_term_per_cluster = 50

    print("\n")
    main()
